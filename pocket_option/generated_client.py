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

    async def subscribe_to_asset(self, asset: models.Asset) -> None:
        """No description


        :type asset: models.Asset
        """
        await self.client.send("subscribeSymbol", asset)

    async def subscribe_for_market_sentiment(self, asset: models.Asset) -> None:
        """No description


        :type asset: models.Asset
        """
        await self.client.send("subfor", asset)

    async def unsubscribe_for_market_sentiment(self, asset: models.Asset) -> None:
        """No description


        :type asset: models.Asset
        """
        await self.client.send("unsubfor", asset)

    async def change_asset(self, data: models.ChangeAssetRequest) -> None:
        """No description


        :type data: models.ChangeAssetRequest
        """
        await self.client.send("changeSymbol", data)

    async def open_deal(self, data: models.OpenDealRequest) -> None:
        """No description


        :type data: models.OpenDealRequest
        """
        await self.client.send("openOrder", data)

    async def copy_signal(self, data: models.CopySignalRequest) -> None:
        """No description


        :type data: models.CopySignalRequest
        """
        await self.client.send("copySignalOrder", data)


class PocketOptionClientOn:
    def __init__(self, client: BasePocketOptionClient) -> None:
        self.client = client

    @typing.overload
    def update_balance(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[models.SuccessUpdateBalanceEvent]], None]": ...

    @typing.overload
    def update_balance(
        self,
        handler: "TypedEventListener[models.SuccessUpdateBalanceEvent]",
    ) -> None: ...

    def update_balance(
        self,
        handler: "TypedEventListener[models.SuccessUpdateBalanceEvent] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[models.SuccessUpdateBalanceEvent]], None]":
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[models.SuccessUpdateBalanceEvent] | None
        """
        return self.client.add_on("successupdateBalance", handler=handler, model=models.SuccessUpdateBalanceEvent)

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
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[models.UpdateHistoryFastEvent] | None
        """
        return self.client.add_on("updateHistoryNewFast", handler=handler, model=models.UpdateHistoryFastEvent)

    @typing.overload
    def update_close_value(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[list[models.UpdateCloseValueItem]]], None]": ...

    @typing.overload
    def update_close_value(
        self,
        handler: "TypedEventListener[list[models.UpdateCloseValueItem]]",
    ) -> None: ...

    def update_close_value(
        self,
        handler: "TypedEventListener[list[models.UpdateCloseValueItem]] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[list[models.UpdateCloseValueItem]]], None]":
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[list[models.UpdateCloseValueItem]] | None
        """
        return self.client.add_on("updateStream", handler=handler, model=models.UpdateCloseValueListTypeAdapter)

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
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[list[models.Deal]] | None
        """
        return self.client.add_on("updateOpenedDeals", handler=handler, model=models.DealListTypeAdapter)

    @typing.overload
    def success_open_deal(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[models.Deal]], None]": ...

    @typing.overload
    def success_open_deal(
        self,
        handler: "TypedEventListener[models.Deal]",
    ) -> None: ...

    def success_open_deal(
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
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[list[models.Deal]] | None
        """
        return self.client.add_on("updateClosedDeals", handler=handler, model=models.DealListTypeAdapter)

    @typing.overload
    def update_assets(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[list[models.UpdateAssetItem]]], None]": ...

    @typing.overload
    def update_assets(
        self,
        handler: "TypedEventListener[list[models.UpdateAssetItem]]",
    ) -> None: ...

    def update_assets(
        self,
        handler: "TypedEventListener[list[models.UpdateAssetItem]] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[list[models.UpdateAssetItem]]], None]":
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[list[models.UpdateAssetItem]] | None
        """
        return self.client.add_on("updateAssets", handler=handler, model=models.UpdateAssetItemListTypeAdapter)

    @typing.overload
    def success_close_deal(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[models.SuccessCloseDealEvent]], None]": ...

    @typing.overload
    def success_close_deal(
        self,
        handler: "TypedEventListener[models.SuccessCloseDealEvent]",
    ) -> None: ...

    def success_close_deal(
        self,
        handler: "TypedEventListener[models.SuccessCloseDealEvent] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[models.SuccessCloseDealEvent]], None]":
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[models.SuccessCloseDealEvent] | None
        """
        return self.client.add_on("successcloseOrder", handler=handler, model=models.SuccessCloseDealEvent)

    @typing.overload
    def connect(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[None]], None]": ...

    @typing.overload
    def connect(
        self,
        handler: "TypedEventListener[None]",
    ) -> None: ...

    def connect(
        self,
        handler: "TypedEventListener[None] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[None]], None]":
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[None] | None
        """
        return self.client.add_on("connect", handler=handler, model=None)

    @typing.overload
    def disconnect(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[None]], None]": ...

    @typing.overload
    def disconnect(
        self,
        handler: "TypedEventListener[None]",
    ) -> None: ...

    def disconnect(
        self,
        handler: "TypedEventListener[None] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[None]], None]":
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[None] | None
        """
        return self.client.add_on("disconnect", handler=handler, model=None)

    @typing.overload
    def success_auth(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[models.SuccessAuthEvent]], None]": ...

    @typing.overload
    def success_auth(
        self,
        handler: "TypedEventListener[models.SuccessAuthEvent]",
    ) -> None: ...

    def success_auth(
        self,
        handler: "TypedEventListener[models.SuccessAuthEvent] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[models.SuccessAuthEvent]], None]":
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[models.SuccessAuthEvent] | None
        """
        return self.client.add_on("successauth", handler=handler, model=models.SuccessAuthEvent)

    @typing.overload
    def change_market_sentiment(
        self,
        handler: None = None,
    ) -> "typing.Callable[[TypedEventListener[list[models.MarketSentimentItem]]], None]": ...

    @typing.overload
    def change_market_sentiment(
        self,
        handler: "TypedEventListener[list[models.MarketSentimentItem]]",
    ) -> None: ...

    def change_market_sentiment(
        self,
        handler: "TypedEventListener[list[models.MarketSentimentItem]] | None" = None,
    ) -> "None | typing.Callable[[TypedEventListener[list[models.MarketSentimentItem]]], None]":
        """No description

        :param handler: Callback
        :type handler: TypedEventListener[list[models.MarketSentimentItem]] | None
        """
        return self.client.add_on("chafor", handler=handler, model=models.MarketSentimentItemListTypeAdapter)


class PocketOptionClient(BasePocketOptionClient):
    @property
    def on(self) -> PocketOptionClientOn:
        return PocketOptionClientOn(self)

    @property
    def emit(self) -> PocketOptionClientEmit:
        return PocketOptionClientEmit(self)
