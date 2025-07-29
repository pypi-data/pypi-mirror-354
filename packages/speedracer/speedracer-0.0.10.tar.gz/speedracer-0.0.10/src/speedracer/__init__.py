r'''

.. include:: ../../README.md

'''

import asyncio
import datetime
from enum import Enum
import errno
import hashlib
import logging
import os
from pathlib import Path
from random import shuffle
import ssl
import sys
import time
from typing import Union, Optional, Callable, Tuple, List, Dict, Iterable
from urllib.parse import urlparse, urlunparse

import jwt
import requests

try:
    import aiohttp
except ImportError:
    aiohttp = None # type: ignore[assignment]

import nats
from nats import errors
from nats.errors import TimeoutError as NatsTimeoutError
from nats.protocol import command as prot_command
from nats.aio.client import Client

logging.getLogger(__name__).setLevel(logging.INFO)

# Monkey patch aiohttp. Aiohttp only uses *_PROXY environment variables if a
# session is created with trust_env=True.
def _monkey_patched_init(self):
    # pylint: disable=protected-access
    if not aiohttp:
        raise ImportError(
            "Could not import aiohttp transport, please install it with `pip install aiohttp`"
        )
    self._ws: Optional[aiohttp.ClientWebSocketResponse] = None
    self._client: aiohttp.ClientSession = aiohttp.ClientSession(trust_env=True)
    self._pending = asyncio.Queue()
    self._close_task = asyncio.Future()
    self._using_tls: Optional[bool] = None

nats.aio.transport.WebSocketTransport.__init__ = _monkey_patched_init

# Monkey patch nats. This is for version 2.10.0 of the nats library.
# Once this is fixed, change the dependency to not be the exact version.
async def _monkey_patch_process_err(self, err_msg: str) -> None:
    """
    Processes the raw error message sent by the server
    and close connection with current server.
    """
    # pylint: disable=protected-access
    if nats.protocol.parser.STALE_CONNECTION in err_msg:
        await self._process_op_err(nats.errors.StaleConnectionError())
        return
    if nats.protocol.parser.AUTHORIZATION_VIOLATION in err_msg:
        self._err = nats.errors.AuthorizationError()
    else:
        prot_err = err_msg.strip("'")
        message = f"nats: {prot_err}"
        err = nats.errors.Error(message)
        self._err = err

        if nats.protocol.parser.PERMISSIONS_ERR in message:
            await self._error_cb(err)
            return
    do_cbs = False
    if not self.is_connecting:
        do_cbs = True
    if err_msg == "'user authentication expired'":
        await self._process_op_err(self._err)
    else:
        asyncio.create_task(self._close(nats.aio.client.Client.CLOSED, do_cbs))

Client._process_err = _monkey_patch_process_err # pylint: disable=protected-access

async def _monkey_patch_attempt_reconnect(self) -> None:
    """
    Monkey patch _attempt_reconnect because it does not handle all of the
    necessary exceptions.
    """
    # pylint: disable=protected-access,too-many-branches,too-many-statements
    assert self._current_server, "Client.connect must be called first"
    if self._reading_task is not None and not self._reading_task.cancelled(
    ):
        self._reading_task.cancel()

    if (self._ping_interval_task is not None
            and not self._ping_interval_task.cancelled()):
        self._ping_interval_task.cancel()

    if self._flusher_task is not None and not self._flusher_task.cancelled(
    ):
        self._flusher_task.cancel()

    if self._transport is not None:
        self._transport.close()
        try:
            await self._transport.wait_closed()
        except Exception as e: # pylint: disable=broad-exception-caught
            await self._error_cb(e)

    self._err = None
    if self._disconnected_cb is not None:
        await self._disconnected_cb()

    if self.is_closed:
        return

    if "dont_randomize" not in self.options or not self.options[
            "dont_randomize"]:
        shuffle(self._server_pool)

    # Create a future that the client can use to control waiting
    # on the reconnection attempts.
    self._reconnection_task_future = asyncio.Future()
    while True:
        try:
            # Try to establish a TCP connection to a server in
            # the cluster then send CONNECT command to it.
            await self._select_next_server()
            assert self._transport, "_select_next_server must've set _transport"
            await self._process_connect_init()

            # Consider a reconnect to be done once CONNECT was
            # processed by the server successfully.
            self.stats["reconnects"] += 1

            # Reset reconnect attempts for this server
            # since have successfully connected.
            self._current_server.did_connect = True
            self._current_server.reconnects = 0

            # Replay all the subscriptions in case there were some.
            subs_to_remove = []
            for sid, sub in self._subs.items():
                max_msgs = 0
                if sub._max_msgs > 0:
                    # If we already hit the message limit, remove the subscription and don't
                    # resubscribe.
                    if sub._received >= sub._max_msgs:
                        subs_to_remove.append(sid)
                        continue
                    # auto unsubscribe the number of messages we have left
                    max_msgs = sub._max_msgs - sub._received

                sub_cmd = prot_command.sub_cmd(
                    sub._subject, sub._queue, sid
                )
                self._transport.write(sub_cmd)

                if max_msgs > 0:
                    unsub_cmd = prot_command.unsub_cmd(sid, max_msgs)
                    self._transport.write(unsub_cmd)

            for sid in subs_to_remove:
                self._subs.pop(sid)

            await self._transport.drain()

            # pylint: disable=fixme
            # Flush pending data before continuing in connected status.
            # FIXME: Could use future here and wait for an error result
            # to bail earlier in case there are errors in the connection.
            # await self._flush_pending(force_flush=True)
            await self._flush_pending()
            self._status = Client.CONNECTED
            await self.flush()
            if self._reconnected_cb is not None:
                await self._reconnected_cb()
            self._reconnection_task_future = None
            break
        except errors.NoServersError as e:
            self._err = e
            await self.close()
            break
        except (OSError, errors.Error, asyncio.TimeoutError) as e:
            self._err = e
            await self._error_cb(e)
            self._status = Client.RECONNECTING
            self._current_server.last_attempt = time.monotonic()
            self._current_server.reconnects += 1
        except asyncio.CancelledError:
            break
        # This is the patch.
        except Exception as e: # pylint: disable=broad-exception-caught
            # This is mostly a copy of an above branch
            better_err = errors.Error("reconnection attempt failed")
            self._err = better_err
            await self._error_cb(better_err)
            self._status = Client.RECONNECTING
            self._current_server.last_attempt = time.monotonic()
            self._current_server.reconnects += 1

    if (self._reconnection_task_future is not None
            and not self._reconnection_task_future.cancelled()):
        self._reconnection_task_future.set_result(True)

Client._attempt_reconnect = _monkey_patch_attempt_reconnect # pylint: disable=protected-access

class JWTManager:
    """A class for conveniently working with JSON Web Tokens (JWTs)
    Example:
        ```python
        manager = JWTManager('https://gateway.com/getjwt')

        # get a JWT
        token = manager.get()

        # get HTTP headers dictionary with an Authorization header set
        headers = manager.get_headers()

        # get your Common Name
        name = manager.get_cn()
        ```
    """
    def __init__(self, url:str, cert:Tuple[str, str]=(Path.home().joinpath('.ssh/cert.crt'),
            Path.home().joinpath('.ssh/cert.key')),
            verify:Union[str, bool]=True) -> None:
        '''Create a JWT Manager

        Arguments:
            url: The URL of the API Gateway to fetch JWTs from
            cert: A Tuple containing the paths to the certificate and
                key to use with the API Gateway. By default, looks in the
                user's home directory for the files cert.crt and cert.key
            verify: A bool or a path to a Certificate Authority. Passed to the requests library
        '''

        if not os.path.isfile(cert[0]):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), cert[0])

        if not os.path.isfile(cert[1]):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), cert[1])

        if not isinstance(verify, bool) and not os.path.isfile(verify):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), verify)

        self.token:Optional[Union[str, None]] = None
        '''The most recently fetched JWT. Use the `get` method instead of accessing this directly'''
        self.url:str = url
        '''The URL of the API Gateway to fetch JWTs from'''
        self.cert:Tuple[str, str] = cert
        '''A Tuple containing the paths to the certificate and key to use with the API Gateway'''
        self.verify:Union[str, bool] = verify
        '''A bool or a path to a Certificate Authority. Passed to the requests library'''

    def __is_expired(self) -> None:
        in_five_minutes = time.mktime(
            (datetime.datetime.utcnow() + datetime.timedelta(minutes=5)).timetuple())
        claims = jwt.decode(self.token, options={'verify_signature': False})
        if 'exp' in claims:
            return claims['exp'] < in_five_minutes
        return False

    def __get_jwt(self) -> None:
        try:
            resp = requests.get(self.url, cert=self.cert, verify=self.verify, timeout=10)
            resp.raise_for_status()
            self.token = resp.text.strip()
        except requests.exceptions.RequestException as err:
            logging.getLogger(__name__).exception("fetching JWT")
            if self.token is None:
                # pylint: disable=broad-exception-raised
                raise Exception('Unable to get initial JWT') from err

    def get(self) -> str:
        '''Returns a cached JWT or a new one if the cached JWT is close to expiration

        Example:
            ```python
            token = manager.get()
            ```

        Returns:
            str: JWT
        '''
        if self.token is None or self.__is_expired():
            self.__get_jwt()
        return self.token

    def get_headers(self) -> Dict:
        '''Returns a Dict containing an Authorization HTTP header for use with Autobahn APIs

        Example:

            ```python
            headers = manager.get_headers()
            ```

        Returns:
            Dict: contains Authorization header

                {
                    'Authorization': 'Bearer <jwt-here>'
                }
        '''
        return {
            'Authorization': 'Bearer ' + self.get()
        }

    def get_cn(self) -> str:
        '''Extracts the CN claim from a JSON Web Token

        Example:
            ```python
            name = manager.get_cn()
            ```

        Returns:
            str: common name extracted from the JWT
        '''
        return jwt.decode(self.get(), options={'verify_signature': False})['CN']

class Offset(str, Enum):
    '''The offset to start consuming messages from'''
    BEGIN = 'begin'
    NOW = 'now'

class Connection:
    '''Connect to Autobahn'''
    def __init__(self, url:str, cert:Tuple[str, str]=(Path.home().joinpath('.ssh/cert.crt'),
                Path.home().joinpath('.ssh/cert.key')),
            ca_bundle:Optional[str]=None,
            websocket:bool=True) -> None:
        '''
        Example:
            ```python
            conn = Connection('https://mdb-account-server/')
            ```

        Arguments:
          url: URL of the Autobahn MDB account server
          cert: Paths to a PEM formated X.509 certificate and key file
            Defaults to ('$HOME/.ssh/cert.crt', '$HOME/.ssh/cert.key')
          ca_bundle: A path to a PEM encoded certificate authority file
          websocket: Whether to connect using WebSocket. Defaults to True.
        '''

        if not os.path.isfile(cert[0]):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), cert[0])

        if not os.path.isfile(cert[1]):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), cert[1])

        if ca_bundle and not os.path.isfile(ca_bundle):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), ca_bundle)

        def get_urls():
            config_url = urlparse(url)
            config_url = urlunparse(config_url._replace(path='/api/v1/config'))
            try:
                resp = requests.get(config_url, verify=self.verify, timeout=10)
                resp.raise_for_status()
                return resp.json()
            except requests.exceptions.SSLError as ssl_error:
                logging.getLogger(__name__).exception('''SSLError getting
service urls. Commonly caused by not providing client certificates or by
not specifying a ca_bundle''')
                raise ssl_error
            except requests.exceptions.RequestException as err:
                logging.getLogger(__name__).exception('getting service urls')
                raise err

        self.cert: Tuple[str, str] = cert
        '''Client certificate. Invalid certificates result in `SSLError`'''
        self.ca_bundle: Optional[str] = ca_bundle
        '''Certificate Authority used to verify server SSL certificates'''
        self.verify: Union[str, bool] = ca_bundle if ca_bundle else True
        '''Verify server SSL certificates. Set to false if a valid ca_bundle is not available.'''
        self.websocket= websocket
        '''Whether to connect using WebSocket'''
        self.urls: Dict = get_urls()
        '''URLs to Autobahn services (read-only)'''
        self.jwt_manager: JWTManager = JWTManager(self.urls['api_gateway_url'],
                cert=cert, verify=self.verify)
        '''A `JWTManager` for authenticating to Autobahn'''
        self.subscriptions: List = []
        '''An array of all Subscriptions associated with this Connection'''

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
        return False

    async def subscribe(self, dataset:str, offset:Offset=Offset.NOW, batch:int=10,
            callback:Optional[Callable]=None) -> Iterable:
        '''Subscribe to a dataset.

        Example:
            ```python
            sub = await conn.subscribe('mydataset')
            async for msg in sub:
                print(msg.data.decode())
            ```

        Arguments:
            dataset: The slug of the dataset
            offset: The offset to start consuming messages from
            batch: The number of messages retrieved at a time
        '''
        sub = self.Subscription(self.urls, self.jwt_manager, self.ca_bundle,
                dataset, offset, batch, callback, self.websocket)
        await sub.start()
        self.subscriptions.append(sub)
        logging.getLogger(__name__).info("Subscribed to dataset: %s", dataset)
        return sub

    async def close(self):
        '''Close all subscriptions associated with this Connection'''

        # pylint: disable=broad-exception-caught
        # Try closing each subscription

        for sub in self.subscriptions:
            try:
                await sub.close()
            except Exception as ex:
                print('exception closing subscription:', ex)
            self.subscriptions = []


    class Subscription:
        '''A subscription to a dataset. Iterable'''

        # pylint: disable=too-many-instance-attributes

        # pylint: disable=too-many-arguments
        # Only called internally so it is fine

        def __init__(self, # pylint: disable=too-many-positional-arguments
                urls:Dict,
                jwt_manager:JWTManager,
                ca_bundle:Optional[str],
                dataset:str,
                offset:Offset,
                batch:int,
                callback:Optional[Callable],
                websocket:bool=True) -> None:
            '''Create a subscription. Use a Connection's `subscribe` method instead

            Arguments:
                urls: A Dict containing URLs to services
                jwt_manager: A `JWTManager` for authenticating to Autobahn
                ca_bundle: Path to a Certificate Authority
                dataset: The slug of the dataset to subscribe to
                offset: The offset to start consuming messages from
                batch: The number of messages the client will pull at a time
                callback: A Callable that takes a NATS message as an
                    argument. Called for each messages received
                websocket: Whether to use WebSocket to subscribe. Defaults to True.
            '''
            self.verify:Union[str, bool] = ca_bundle if ca_bundle else True
            '''Verify server SSL certificates. Set to false if a valid 
            ca_bundle is not available.'''
            self.urls:Dict = urls
            '''URLs to Autobahn services (read-only)'''
            self.jwt_manager:JWTManager = jwt_manager
            '''A JWTManager for authenticating to Autobahn'''
            self.dataset:str = dataset
            '''The dataset slug for this subscription'''
            self.offset:Offset = offset
            '''The offset to start consuming messages from'''
            self.batch:int = batch
            '''Number of messages the subscription will pull at a time'''
            self.callback:Optional[Callable] = callback
            '''Optional callback that takes a NATS message as an argument'''
            self.websocket = websocket
            '''Whether to use WebSocket to subscribe'''
            self.__ssl_context:ssl.SSLContext = ssl.create_default_context()
            '''SSL context used by aiohttp'''
            if ca_bundle:
                self.__ssl_context.load_verify_locations(ca_bundle)
            self.__nats_conn = None
            '''NATS Connection'''
            self.__js_ctx = None
            '''NATS JetStream Context'''
            self.__psub = None
            '''NATS Pull Subscription'''
            self.__consumer_name:str = None
            '''NATS Consumer name'''
            self.__cb_task = None
            '''Asyncio Task for message callback'''

            def get_subject() -> str:
                return self.dataset.lower()

            self.subject: str = get_subject()
            '''NATS Subject'''

        async def __aiter__(self):
            while True:
                try:
                    msgs = await self.__psub.fetch(self.batch, timeout=10)
                    for msg in msgs:
                        await msg.ack()
                    for msg in msgs:
                        yield msg
                except NatsTimeoutError: # no messages to return yet
                    pass
                except KeyboardInterrupt:
                    break

        async def __call_callback(self):
            async for msg in self:
                self.callback(msg)

        async def start(self):
            '''Start receiving data from the dataset. This is called automatically
            when using `Connection.subscribe()`'''
            def signature(_):
                return bytes('', 'UTF-8')

            def get_mas_jwt() -> bytearray:
                resp = requests.get(f"{self.urls['mas_url']}/api/v1/user/jwt/{self.dataset}",
                        headers=self.jwt_manager.get_headers(), verify=self.verify, timeout=10)
                resp.raise_for_status()
                encoded_token = resp.text.encode()
                return bytearray(encoded_token)

            def get_consumer_name() -> str:
                cn_hash = hashlib.md5(self.jwt_manager.get_cn().encode(), usedforsecurity=False)
                return cn_hash.hexdigest()[:-1] + '0'


            async def create_conn() -> None:
                async def disconnected_cb():
                    logging.getLogger(__name__).warning('Disconnected from NATS')

                async def reconnected_cb():
                    logging.getLogger(__name__).warning('Reconnected to NATS')

                async def error_cb(err):
                    if isinstance(err, asyncio.exceptions.TimeoutError):
                        logging.getLogger(__name__).error('Error: asyncio.exceptions.TimeoutError.'
                                ' This may be due to the client reconnecting')
                    else:
                        logging.getLogger(__name__).error("Error: %s", err)

                async def closed_cb():
                    logging.getLogger(__name__).warning('Connection to NATS closed')

                self.__nats_conn = await nats.connect(
                        self.urls['nats_websocket_url'] if self.websocket else
                            self.urls['nats_url'],
                        name=f"{self.jwt_manager.get_cn()} ({self.dataset})",
                        signature_cb=signature,
                        user_jwt_cb=get_mas_jwt,
                        tls=self.__ssl_context,
                        max_reconnect_attempts=-1,
                        pending_size=8*1024*1024,
                        disconnected_cb=disconnected_cb,
                        reconnected_cb=reconnected_cb,
                        error_cb=error_cb,
                        closed_cb=closed_cb)
                self.__js_ctx = self.__nats_conn.jetstream()
                self.__consumer_name = get_consumer_name()

            await create_conn()
            await self.__create_sub()

        async def __create_sub(self, start_sequence:Union[int, None]=None,
                start_datetime:Union[datetime.datetime, None]=None) -> None:

            cfg=nats.js.api.ConsumerConfig(
                description=(
                    f"Consumer created by Python speedracer for {self.jwt_manager.get_cn()}"
                    f" on Python {sys.version}"
                ),
                inactive_threshold=60.0*60.0*24.0*7.0, # seconds
            )

            if start_sequence is not None:
                cfg.deliver_policy = (
                    nats.js.api.DeliverPolicy.BY_START_SEQUENCE)
                cfg.opt_start_seq = start_sequence
            elif start_datetime is not None:
                cfg.deliver_policy = (
                    nats.js.api.DeliverPolicy.BY_START_TIME)
                cfg.opt_start_time =  start_datetime.replace(
                        tzinfo=datetime.timezone.utc).isoformat()
            elif self.offset == Offset.NOW:
                cfg.deliver_policy = nats.js.api.DeliverPolicy.NEW
            else:
                cfg.deliver_policy = nats.js.api.DeliverPolicy.ALL

            self.__psub = await self.__js_ctx.pull_subscribe(
                    subject=self.subject,
                    durable=self.__consumer_name,
                    config=cfg)

            if self.callback and not self.__cb_task:
                self.__cb_task = asyncio.create_task(self.__call_callback())

        async def seek(self, seq_or_datetime: Union[int, datetime.datetime]) -> None:
            '''Move cursor to specified sequence number or datetime

            Example:
                ```python
                await sub.seek(1)
                await sub.seek(datetime.datetime.utcnow() -
                    datetime.timedelta(minutes=5))
                ```

            Arguments:
                seq_or_datetime: Sequence number or datetime to seek to
            '''
            start_sequence = None
            start_datetime = None
            if isinstance(seq_or_datetime, int):
                start_sequence = seq_or_datetime
            elif isinstance(seq_or_datetime, datetime.datetime):
                start_datetime = seq_or_datetime
            else:
                raise TypeError("seek to argument must be int or datetime")
            logging.getLogger(__name__).info('Seeking')
            await self.__psub.unsubscribe()
            await self.__delete_consumer()
            await self.__create_sub(start_sequence, start_datetime)
            logging.getLogger(__name__).info('Finished seeking')

        async def __delete_consumer(self) -> bool:
            stream_name = self.subject.replace('.', '_')
            return await self.__js_ctx.delete_consumer(stream_name, self.__consumer_name)

        async def wait(self, messages:Union[int, None]=None,
                timeout:Union[int, datetime.datetime, datetime.timedelta, None]=None) -> None:
            '''Block until specified number of messages are consumed or specified
            amount of time has elapsed

            Example:
                ```python
                await sub.wait(messages=15)
                await sub.wait(timeout=5)
                ```

            Arguments:
                messages: The number of messages to wait for
                timeout: The number of seconds to wait for, the
                    datetime to wait until, or the timedelta to
                    wait for
            '''
            if messages:
                msgs_target = self.__psub.delivered + messages
                while self.__psub.delivered < msgs_target:
                    await asyncio.sleep(1)
            if timeout:
                if isinstance(timeout, datetime.datetime):
                    await asyncio.sleep((timeout - datetime.datetime.utcnow()).total_seconds())
                elif isinstance(timeout, datetime.timedelta):
                    await asyncio.sleep(timeout.total_seconds())
                else:
                    await asyncio.sleep(timeout)

        async def close(self) -> None:
            '''Close this Subscription'''
            if self.__cb_task:
                self.__cb_task.cancel()
                await asyncio.sleep(0.1)
            await self.__nats_conn.close()
