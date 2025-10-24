import typing

from pocket_option import models
from pocket_option.client import BasePocketOptionClient

if typing.TYPE_CHECKING:
    from pocket_option.types import TypedEventListener

__all__ = ("PocketOptionClient",)


class PocketOptionClientEmit:
    def __init__(self, client: BasePocketOptionClient) -> None:
        self.client = client

    async def ps(self) -> None:
        """No description"""
        await self.client.send("ps")

    async def indicator_load(self) -> None:
        """No description"""
        await self.client.send("indicator/load")

    async def favorite_load(self) -> None:
        """No description"""
        await self.client.send("favorite/load")

    async def price_alert_load(self) -> None:
        """No description"""
        await self.client.send("price-alert/load")

    async def auth(self, data: models.AuthorizationData) -> None:
        """No description


        :type data: models.AuthorizationData
        """
        await self.client.send("auth", data)

    async def subscribe_symbol(self, asset: models.Asset) -> None:
        """Subscribes to live updates for a specific asset symbol.

        :param asset: The asset symbol to subscribe to.
        :type asset: models.Asset
        """
        await self.client.send("subscribeSymbol", asset)

    async def subscribe_for(self, asset: models.Asset) -> None:
        """Subscribes to specific data streams for the given asset.

        :param asset: The asset symbol to subscribe for.
        :type asset: models.Asset
        """
        await self.client.send("subfor", asset)

    async def unsubscribe_for(self, asset: models.Asset) -> None:
        """Unsubscribes from data streams for the given asset.

        :param asset: The asset symbol to unsubscribe from.
        :type asset: models.Asset
        """
        await self.client.send("unsubfor", asset)

    async def change_symbol(self, data: models.ChangeSymbolRequest) -> None:
        """No description


        :type data: models.ChangeSymbolRequest
        """
        await self.client.send("changeSymbol", data)

    async def open_order(self, data: models.OpenOrderRequest) -> None:
        """Sends a request to open a new trading order.

        :param data: Order request payload.
        :type data: models.OpenOrderRequest
        """
        await self.client.send("openOrder", data)

    async def copy_signal_order(self, data: models.CopySignalRequest) -> None:
        """Executes an order based on a copied trading signal.

        :param data: Copy trading signal request payload.
        :type data: models.CopySignalRequest
        """
        await self.client.send("copySignalOrder", data)


class PocketOptionClientOn:
    def __init__(self, client: BasePocketOptionClient) -> None:
        self.client = client

    @typing.overload
    def success_update_balance(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[models.SuccessUpdateBalance]], None]": ...

    @typing.overload
    def success_update_balance(
        self,
        handler: "TypedEventListener[models.SuccessUpdateBalance]",
    ) -> None: ...

    def success_update_balance(
        self,
        handler: "TypedEventListener[models.SuccessUpdateBalance] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[models.SuccessUpdateBalance]], None]":
        """Triggered when the user's account balance is updated.

        :param handler: Callback
        :type handler: TypedEventListener[models.SuccessUpdateBalance] | None
        """
        return self.client.add_on("successupdateBalance", handler=handler, model=models.SuccessUpdateBalance)

    @typing.overload
    def update_history_new_fast(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[models.UpdateHistoryFastEvent]], None]": ...

    @typing.overload
    def update_history_new_fast(
        self,
        handler: "TypedEventListener[models.UpdateHistoryFastEvent]",
    ) -> None: ...

    def update_history_new_fast(
        self,
        handler: "TypedEventListener[models.UpdateHistoryFastEvent] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[models.UpdateHistoryFastEvent]], None]":
        """Triggered when a new fast trading history record is received.

        :param handler: Callback
        :type handler: TypedEventListener[models.UpdateHistoryFastEvent] | None
        """
        return self.client.add_on("updateHistoryNewFast", handler=handler, model=models.UpdateHistoryFastEvent)

    @typing.overload
    def update_stream(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[list[models.UpdateStreamItem]]], None]": ...

    @typing.overload
    def update_stream(
        self,
        handler: "TypedEventListener[list[models.UpdateStreamItem]]",
    ) -> None: ...

    def update_stream(
        self,
        handler: "TypedEventListener[list[models.UpdateStreamItem]] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[list[models.UpdateStreamItem]]], None]":
        """Triggered when a live data stream update is received.

        :param handler: Callback
        :type handler: TypedEventListener[list[models.UpdateStreamItem]] | None
        """
        return self.client.add_on("updateStream", handler=handler, model=models.UpdateStreamTypeAdapter)

    @typing.overload
    def update_opened_deals(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[list[models.Deal]]], None]": ...

    @typing.overload
    def update_opened_deals(
        self,
        handler: "TypedEventListener[list[models.Deal]]",
    ) -> None: ...

    def update_opened_deals(
        self,
        handler: "TypedEventListener[list[models.Deal]] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[list[models.Deal]]], None]":
        """Triggered when the list of currently opened deals is updated.

        :param handler: Callback
        :type handler: TypedEventListener[list[models.Deal]] | None
        """
        return self.client.add_on("updateOpenedDeals", handler=handler, model=models.DealListTypeAdapter)

    @typing.overload
    def success_open_order(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[models.Deal]], None]": ...

    @typing.overload
    def success_open_order(
        self,
        handler: "TypedEventListener[models.Deal]",
    ) -> None: ...

    def success_open_order(
        self,
        handler: "TypedEventListener[models.Deal] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[models.Deal]], None]":
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[models.Deal] | None
        """
        return self.client.add_on("successopenOrder", handler=handler, model=models.Deal)

    @typing.overload
    def update_closed_deals(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[list[models.Deal]]], None]": ...

    @typing.overload
    def update_closed_deals(
        self,
        handler: "TypedEventListener[list[models.Deal]]",
    ) -> None: ...

    def update_closed_deals(
        self,
        handler: "TypedEventListener[list[models.Deal]] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[list[models.Deal]]], None]":
        """Triggered when the list of recently closed deals is updated.

        :param handler: Callback
        :type handler: TypedEventListener[list[models.Deal]] | None
        """
        return self.client.add_on("updateClosedDeals", handler=handler, model=models.DealListTypeAdapter)

    @typing.overload
    def success_close_order(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[models.SuccessCloseOrder]], None]": ...

    @typing.overload
    def success_close_order(
        self,
        handler: "TypedEventListener[models.SuccessCloseOrder]",
    ) -> None: ...

    def success_close_order(
        self,
        handler: "TypedEventListener[models.SuccessCloseOrder] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[models.SuccessCloseOrder]], None]":
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[models.SuccessCloseOrder] | None
        """
        return self.client.add_on("successcloseOrder", handler=handler, model=models.SuccessCloseOrder)


class PocketOptionClient(BasePocketOptionClient):
    @property
    def on(self) -> PocketOptionClientOn:
        return PocketOptionClientOn(self)

    @property
    def emit(self) -> PocketOptionClientEmit:
        return PocketOptionClientEmit(self)
