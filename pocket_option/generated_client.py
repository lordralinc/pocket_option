import asyncio
import typing

from pocket_option.client import BasePocketOptionClient

if typing.TYPE_CHECKING:
    from pocket_option import models
    from pocket_option.types import JsonValue, TypedEventListener

__all__ = ("PocketOptionClient",)


class PocketOptionClient(BasePocketOptionClient):
    @typing.overload
    def on_success_update_balance(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[models.SuccessUpdateBalance]], None]": ...
    @typing.overload
    def on_success_update_balance(
        self,
        handler: "TypedEventListener[models.SuccessUpdateBalance]",
    ) -> None: ...

    def on_success_update_balance(
        self,
        handler: "TypedEventListener[models.SuccessUpdateBalance] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[models.SuccessUpdateBalance]], None]":
        return self.on("successupdateBalance", handler=handler)

    @typing.overload
    def on_update_history_new_fast(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[models.UpdateHistoryFastEvent]], None]": ...
    @typing.overload
    def on_update_history_new_fast(
        self,
        handler: "TypedEventListener[models.UpdateHistoryFastEvent]",
    ) -> None: ...

    def on_update_history_new_fast(
        self,
        handler: "TypedEventListener[models.UpdateHistoryFastEvent] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[models.UpdateHistoryFastEvent]], None]":
        return self.on("updateHistoryNewFast", handler=handler)

    @typing.overload
    def on_update_stream(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[list[models.UpdateStreamItem]]], None]": ...
    @typing.overload
    def on_update_stream(
        self,
        handler: "TypedEventListener[list[models.UpdateStreamItem]]",
    ) -> None: ...

    def on_update_stream(
        self,
        handler: "TypedEventListener[list[models.UpdateStreamItem]] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[list[models.UpdateStreamItem]]], None]":
        def _process(data: list[tuple[str, float, float]]) -> "list[models.UpdateStreamItem]":
            return [
                typing.cast(
                    "models.UpdateStreamItem",
                    {
                        "asset": typing.cast("str", it[0]),
                        "timestamp": typing.cast("float", it[1]) - 7200,  # TO UTC
                        "value": typing.cast("float", it[2]),
                    },
                )
                for it in data
            ]

        if handler is not None:

            async def wrapper(data: list[tuple[str, float, float]]):
                result = handler(_process(data))
                if asyncio.iscoroutine(result):
                    return await result
                return result

            self.sio.on("updateStream", handler=wrapper)
        else:

            def set_handler(_handler: "TypedEventListener[list[models.UpdateStreamItem]]"):
                async def wrapper(data: list[tuple[str, float, float]]):
                    result = _handler(_process(data))
                    if asyncio.iscoroutine(result):
                        return await result
                    return result

                self.sio.on("updateStream", handler=wrapper)

            return set_handler

    @typing.overload
    def on_update_opened_deals(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[list[models.Deal]]], None]": ...
    @typing.overload
    def on_update_opened_deals(
        self,
        handler: "TypedEventListener[list[models.Deal]]",
    ) -> None: ...

    def on_update_opened_deals(
        self,
        handler: "TypedEventListener[list[models.Deal]] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[list[models.Deal]]], None]":
        return self.on("updateOpenedDeals", handler=handler)

    @typing.overload
    def on_update_closed_deals(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[list[models.Deal]]], None]": ...
    @typing.overload
    def on_update_closed_deals(
        self,
        handler: "TypedEventListener[list[models.Deal]]",
    ) -> None: ...

    def on_update_closed_deals(
        self,
        handler: "TypedEventListener[list[models.Deal]] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[list[models.Deal]]], None]":
        return self.on("updateClosedDeals", handler=handler)

    async def emit_ps(self) -> None:
        await self.emit("ps")

    async def emit_indicator_load(self) -> None:
        await self.emit("indicator/load")

    async def emit_favorite_load(self) -> None:
        await self.emit("favorite/load")

    async def emit_price_alert_load(self) -> None:
        await self.emit("price-alert/load")

    async def emit_subscribe_symbol(self, asset: "str") -> None:
        await self.emit("subscribeSymbol", asset)

    async def emit_subscribe_for(self, asset: "str") -> None:
        await self.emit("subfor", asset)

    async def emit_unsubscribe_for(self, asset: "str") -> None:
        await self.emit("unsubfor", asset)

    async def emit_open_order(self, data: "models.OpenOrderRequest") -> None:
        await self.emit("openOrder", typing.cast("JsonValue", data))
