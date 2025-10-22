import asyncio
import collections.abc
import typing

import aiohttp
import socketio

from pocket_option.constants import DEFAULT_ORIGIN, DEFAULT_USER_AGENT
from pocket_option.middleware import EmitMiddleware
from pocket_option.utils import get_json_function

if typing.TYPE_CHECKING:
    from pocket_option import models
    from pocket_option.types import EmitCallback, JsonFunction, JsonValue, SIOEventListener

__all__ = ("BasePocketOptionClient",)


class BasePocketOptionClient:
    def __init__(
        self,
        emit_middlewares: "list[EmitMiddleware] | None" = None,
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
        self.emit_middlewares = emit_middlewares or []
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

    def get_auth_from_packet(self, packet: str) -> "models.AuthorizationData":
        packet = packet.removeprefix("42")
        json_packet = self.json.loads(packet)
        return typing.cast("models.AuthorizationData", json_packet)

    def add_emit_middleware(self, middleware: EmitMiddleware) -> None:
        self.emit_middlewares.append(middleware)

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

    @typing.overload
    def on(self, event: str, handler: None = ...) -> "typing.Callable[[SIOEventListener], None]": ...
    @typing.overload
    def on(self, event: str, handler: "SIOEventListener") -> None: ...

    def on(
        self,
        event: str,
        handler: "SIOEventListener | None" = None,
    ) -> "None | typing.Callable[[SIOEventListener], None]":
        return self.sio.on(event, handler=handler)

    async def emit(
        self,
        event: str,
        data: "JsonValue | None" = None,
        callback: "EmitCallback[JsonValue] | None" = None,
    ) -> None:
        for middleware in self.emit_middlewares:
            event, data, callback = await middleware.emit(event, data=data, callback=callback)

        return await self.sio.emit(event=event, data=data, callback=callback)
