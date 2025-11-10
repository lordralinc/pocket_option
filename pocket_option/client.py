import asyncio
import collections.abc
import functools
import logging
import typing
from inspect import isclass

import aiohttp
import pydantic
import socketio

from pocket_option.constants import DEFAULT_ORIGIN, DEFAULT_USER_AGENT
from pocket_option.middleware import Middleware
from pocket_option.middlewares import FixTypesOnMiddleware, MakeJsonOnMiddleware
from pocket_option.types import JsonValue
from pocket_option.utils import get_function_full_name, get_json_function

if typing.TYPE_CHECKING:
    from pocket_option import models
    from pocket_option.types import EmitCallback, JsonFunction, SIOEventListener

__all__ = ("BasePocketOptionClient",)

logger = logging.getLogger("pocket_option")


class _Handler[T](typing.TypedDict):
    name: str
    model: type[pydantic.BaseModel] | pydantic.TypeAdapter | None
    callback: T


class BasePocketOptionClient:
    def __init__(
        self,
        middlewares: "list[Middleware] | None" = None,
        *,
        reconnection: bool = True,
        reconnection_attempts: int = 0,
        reconnection_delay: float = 1.0,
        reconnection_delay_max: float = 5.0,
        randomization_factor: float = 0.5,
        logger: bool = False,
        engineio_logger: bool = False,
        json: "JsonFunction | None" = None,
        handle_sigint: bool = True,
        request_timeout: float = 5,
        http_session: aiohttp.ClientSession | None = None,
        ssl_verify: bool = True,
        websocket_extra_options: dict | None = None,
        timestamp_requests: bool = False,
    ) -> None:
        """Initializes the Socket.IO client wrapper with middleware and connection options.

        :param on_middlewares:
            A list of middlewares executed on incoming Socket.IO events.
            Each middleware can modify or intercept event data before the callback is called.
            By default, the following middlewares are applied:
            - `MakeJsonOnMiddleware()` — parses JSON data into Python objects.
            - `FixTypesOnMiddleware()` — normalizes data types for consistency.

        :param emit_middlewares:
            A list of middlewares executed before emitting events to the server.
            Each middleware can modify the outgoing payload.
            Defaults to an empty list.

        :param reconnection:
            Enables or disables automatic reconnection when the connection is lost.
            Defaults to `True`.

        :param reconnection_attempts:
            The maximum number of reconnection attempts.
            A value of `0` means unlimited retries.

        :param reconnection_delay:
            Initial delay (in seconds) before attempting to reconnect.
            Defaults to `1.0`.

        :param reconnection_delay_max:
            Maximum delay (in seconds) between reconnection attempts.
            Defaults to `5.0`.

        :param randomization_factor:
            A factor between 0 and 1 used to randomize the reconnection delay to prevent
            simultaneous reconnects.
            Defaults to `0.5`.

        :param logger:
            Enables logging for the Socket.IO client.
            Defaults to `False`.

        :param engineio_logger:
            Enables logging for the underlying Engine.IO layer.
            Defaults to `False`.

        :param json:
            Custom JSON serialization/deserialization functions.
            If not provided, a default implementation will be used.

        :param handle_sigint:
            If `True`, the client will handle SIGINT (Ctrl+C) for clean shutdown.
            Defaults to `True`.

        :param request_timeout:
            The timeout (in seconds) for HTTP requests during the Socket.IO handshake.
            Defaults to `5`.

        :param http_session:
            Optional existing `aiohttp.ClientSession` instance to reuse for HTTP requests.
            If `None`, a new session is created internally.

        :param ssl_verify:
            Whether to verify SSL certificates for secure connections.
            Defaults to `True`.

        :param websocket_extra_options:
            Optional dictionary of additional parameters for the WebSocket connection.
            Useful for setting headers or specific connection parameters.

        :param timestamp_requests:
            Whether to append a timestamp to each request for caching avoidance.
            Defaults to `False`.
        """
        self.authorization_data: "models.AuthorizationData | None" = None
        self.middlewares = middlewares or [MakeJsonOnMiddleware(), FixTypesOnMiddleware()]
        self.json = json or get_json_function()
        self.sio = socketio.AsyncClient(
            reconnection=reconnection,
            reconnection_attempts=reconnection_attempts,
            reconnection_delay=reconnection_delay,  # pyright: ignore[reportArgumentType]
            reconnection_delay_max=reconnection_delay_max,  # pyright: ignore[reportArgumentType]
            randomization_factor=randomization_factor,
            logger=logger,
            serializer="default",
            json=self.json,
            handle_sigint=handle_sigint,
            request_timeout=request_timeout,
            http_session=http_session,
            ssl_verify=ssl_verify,
            websocket_extra_options=websocket_extra_options,
            timestamp_requests=timestamp_requests,
            engineio_logger=engineio_logger,
        )
        self.handlers: list[
            _Handler[
                typing.Callable[
                    ...,
                    typing.Awaitable[JsonValue | pydantic.BaseModel | list[pydantic.BaseModel] | None],
                ]
            ]
        ] = []
        self.sio.on("connect", handler=self.handle_connect_event)
        self.sio.on("disconnect", handler=self.handle_disconnect_event)
        self.sio.on("*", handler=self.handle_new_event)

    def get_auth_from_packet(self, packet: str) -> "models.AuthorizationData":
        packet = packet.removeprefix("42")
        json_packet = self.json.loads(packet)
        return typing.cast("models.AuthorizationData", json_packet)

    def add_middleware(self, middleware: Middleware) -> None:
        self.middlewares.append(middleware)

    async def _get_real_value[T](
        self,
        value: T
        | None
        | collections.abc.Callable[[], T]
        | collections.abc.Callable[[], collections.abc.Coroutine[None, None, T]],
    ) -> T | None:
        if callable(value):
            result = value()
            if asyncio.iscoroutine(result):
                return await result
            return result  # type: ignore
        return value

    async def wait(self):
        return await self.sio.wait()

    async def disconnect(self) -> None:
        return await self.sio.disconnect()

    async def shutdown(self) -> None:
        return await self.sio.shutdown()

    async def sleep(self, seconds: float = 0) -> None:
        return await self.sio.sleep(seconds=seconds)  # type: ignore

    async def connect(
        self,
        url: str,
        headers: dict[str, str] | collections.abc.Callable[[], dict[str, str]] | None = None,
        auth: "models.AuthorizationData | None" = None,
        wait: bool = True,
        wait_timeout: float = 1,
        retry: bool = False,
    ):
        headers = await self._get_real_value(headers) or {}
        headers.setdefault("Origin", DEFAULT_ORIGIN)
        headers.setdefault("User-Agent", DEFAULT_USER_AGENT)
        return await self.sio.connect(
            url,
            headers=headers,
            auth=auth,
            transports=["websocket"],
            namespaces=["/"],
            socketio_path="socket.io",
            wait=wait,
            wait_timeout=wait_timeout,  # type: ignore
            retry=retry,
        )

    async def handle_new_event(
        self,
        event_name: str,
        data: "bytes | None" = None,
    ) -> "JsonValue | None":
        return await self._handle_event(event_name, data)

    async def handle_connect_event(self) -> None:
        await self._handle_event("connect")

    async def handle_disconnect_event(self) -> None:
        await self._handle_event("connect")

    async def _handle_event(self, event_name: str, data: bytes | None = None) -> "JsonValue | None":
        results = []
        logger.debug("New event '%s' with data %r", event_name, data)
        for handler in filter(lambda x: x["name"] == event_name, self.handlers):
            try:
                result = await handler["callback"](data)
                results.append(result)
            except Exception:
                logger.exception(
                    "Error on handler %s, %s",
                    handler["name"],
                    get_function_full_name(handler["callback"]),
                )
            else:
                logger.debug(
                    "Handled by '%s' with result %r",
                    get_function_full_name(handler["callback"]),
                    result,
                )

        for result in results:
            if result is not None:
                return result

    @typing.overload
    def add_on(
        self,
        event: str,
        handler: None = ...,
        *,
        model: type[pydantic.BaseModel] | pydantic.TypeAdapter | None = ...,
    ) -> "typing.Callable[[SIOEventListener], None]": ...
    @typing.overload
    def add_on(
        self,
        event: str,
        handler: "SIOEventListener",
        *,
        model: type[pydantic.BaseModel] | pydantic.TypeAdapter | None = ...,
    ) -> None: ...

    def add_on(
        self,
        event: str,
        handler: "SIOEventListener | None" = None,
        *,
        model: type[pydantic.BaseModel] | pydantic.TypeAdapter | None = None,
    ) -> "None | typing.Callable[[SIOEventListener], None]":
        def _get_data(d: "JsonValue | bytes | None"):
            if isinstance(d, bytes):
                d = self.json.loads(d)
            if d and isinstance(d, dict) and model and isclass(model) and issubclass(model, pydantic.BaseModel):
                return model.model_validate(d)
            if d and isinstance(model, pydantic.TypeAdapter):
                return model.validate_python(d)
            return d

        def _get_result(result: typing.Any):
            if isinstance(result, pydantic.BaseModel):
                return result.model_dump(mode="json")
            if isinstance(result, list):
                return [_get_result(it) for it in result]
            if isinstance(result, dict):
                return {k: _get_result(it) for k, it in result.items()}
            return result

        def set_handler(_handler: "SIOEventListener"):
            @functools.wraps(_handler)
            async def wrapper(data: JsonValue | bytes | None):
                if isinstance(data, bytes):
                    data = self.json.loads(data)
                for middleware in self.middlewares:
                    data = await middleware.on(event, data)
                new_data = _get_data(data)
                result = _handler(new_data)
                if asyncio.iscoroutine(result):
                    result = await result
                return _get_result(result)

            self.handlers.append({"name": event, "callback": wrapper, "model": model})  # type: ignore

        if handler:
            return set_handler(handler)
        return set_handler

    async def send(
        self,
        event: str,
        data: "JsonValue | pydantic.BaseModel | None" = None,
        callback: "EmitCallback[JsonValue] | None" = None,
    ) -> None:
        if event == "auth":
            self.authorization_data = typing.cast("models.AuthorizationData", data)
        if isinstance(data, pydantic.BaseModel):
            data = data.model_dump(mode="json", by_alias=True)
        if isinstance(data, list):
            data = [
                it.model_dump(mode="json", by_alias=True) if isinstance(it, pydantic.BaseModel) else it for it in data
            ]
        for middleware in self.middlewares:
            event, data, callback = await middleware.emit(event, data=data, callback=callback)
        logger.debug(
            "Emitting event '%s' with data %r",
            event,
            data if event != "auth" else {**typing.cast("dict[str, JsonValue]", data), "session": "***"},
        )
        return await self.sio.emit(event=event, data=data, callback=callback)
