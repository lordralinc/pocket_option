import datetime
import enum
import typing
import uuid

import pydantic

__all__ = (
    "Asset",
    "AssetItemTimeframe",
    "AssetType",
    "AuthorizationData",
    "ChangeAssetRequest",
    "Command",
    "CopyOrderRequest",
    "CopyOrderRequest",
    "CopySignalRequest",
    "Deal",
    "DealAction",
    "DealsDoubleUpRequest",
    "DealsRolloverRequest",
    "IsDemo",
    "MarketSentimentItem",
    "MarketSentimentItemListTypeAdapter",
    "OpenDealRequest",
    "OpenPendingDealRequest",
    "OpenPendingDealRequestOpenType",
    "SuccessAuthEvent",
    "SuccessUpdateBalanceEvent",
    "UpdateAssetItem",
    "UpdateAssetItemListTypeAdapter",
    "UpdateCloseValueItem",
    "UpdateCloseValueListTypeAdapter",
    "UpdateHistoryFastEvent",
)

type IsDemo = typing.Literal[0, 1]


class BaseModel(pydantic.BaseModel): ...


class BaseRequest(BaseModel): ...


class BaseEvent(BaseModel): ...


class Asset(enum.StrEnum):
    AUDCAD = "AUDCAD"
    EURUSD = "EURUSD"
    GBPUSD = "GBPUSD"
    USDJPY = "USDJPY"
    USDCHF = "USDCHF"
    USDCAD = "USDCAD"
    AUDUSD = "AUDUSD"
    NZDUSD = "NZDUSD"
    XAUUSD = "XAUUSD"
    XAGUSD = "XAGUSD"
    UKBrent = "UKBrent"
    USCrude = "USCrude"
    XNGUSD = "XNGUSD"
    XPTUSD = "XPTUSD"
    XPDUSD = "XPDUSD"
    BTCUSD = "BTCUSD"
    ETHUSD = "ETHUSD"
    DASH_USD = "DASH_USD"
    BTCGBP = "BTCGBP"
    BTCJPY = "BTCJPY"
    BCHEUR = "BCHEUR"
    BCHGBP = "BCHGBP"
    BCHJPY = "BCHJPY"
    DOTUSD = "DOTUSD"
    LNKUSD = "LNKUSD"
    SP500 = "SP500"
    NASUSD = "NASUSD"
    DJI30 = "DJI30"
    JPN225 = "JPN225"
    D30EUR = "D30EUR"
    E50EUR = "E50EUR"
    F40EUR = "F40EUR"
    E35EUR = "E35EUR"
    A_100GBP = "100GBP"
    AUS200 = "AUS200"
    CAC40 = "CAC40"
    AEX25 = "AEX25"
    SMI20 = "SMI20"
    H33HKD = "H33HKD"
    AAPL = "#AAPL"
    MSFT = "#MSFT"
    TSLA = "#TSLA"
    FB = "#FB"
    NFLX = "#NFLX"
    INTC = "#INTC"
    BA = "#BA"
    JPM = "#JPM"
    JNJ = "#JNJ"
    PFE = "#PFE"
    XOM = "#XOM"
    AXP = "#AXP"
    MCD = "#MCD"
    CSCO = "#CSCO"
    CITI = "#CITI"
    TWITTER = "#TWITTER"
    BABA = "#BABA"

    XAUUSD_otc = "XAUUSD_otc"
    XAGUSD_otc = "XAGUSD_otc"
    UKBrent_otc = "UKBrent_otc"
    USCrude_otc = "USCrude_otc"
    XNGUSD_otc = "XNGUSD_otc"
    XPTUSD_otc = "XPTUSD_otc"
    XPDUSD_otc = "XPDUSD_otc"
    SP500_otc = "SP500_otc"
    NASUSD_otc = "NASUSD_otc"
    DJI30_otc = "DJI30_otc"
    JPN225_otc = "JPN225_otc"
    D30EUR_otc = "D30EUR_otc"
    E50EUR_otc = "E50EUR_otc"
    F40EUR_otc = "F40EUR_otc"
    E35EUR_otc = "E35EUR_otc"
    A_100GBP_otc = "100GBP_otc"
    AUS200_otc = "AUS200_otc"
    EURRUB_otc = "EURRUB_otc"
    USDRUB_otc = "USDRUB_otc"
    EURHUF_otc = "EURHUF_otc"
    CHFNOK_otc = "CHFNOK_otc"
    Microsoft_otc = "Microsoft_otc"
    Facebook_OTC = "Facebook_OTC"
    Tesla_otc = "Tesla_otc"
    Boeing_OTC = "Boeing_OTC"
    American_Express_otc = "American_Express_otc"
    EURUSD_otc = "EURUSD_otc"
    GBPUSD_otc = "GBPUSD_otc"
    USDJPY_otc = "USDJPY_otc"
    USDCHF_otc = "USDCHF_otc"
    USDCAD_otc = "USDCAD_otc"
    AUDUSD_otc = "AUDUSD_otc"
    AUDNZD_otc = "AUDNZD_otc"
    AUDCAD_otc = "AUDCAD_otc"
    AUDCHF_otc = "AUDCHF_otc"
    AUDJPY_otc = "AUDJPY_otc"
    CADCHF_otc = "CADCHF_otc"
    CADJPY_otc = "CADJPY_otc"
    CHFJPY_otc = "CHFJPY_otc"
    EURCHF_otc = "EURCHF_otc"
    EURGBP_otc = "EURGBP_otc"
    EURJPY_otc = "EURJPY_otc"
    EURNZD_otc = "EURNZD_otc"
    GBPAUD_otc = "GBPAUD_otc"
    GBPJPY_otc = "GBPJPY_otc"
    NZDJPY_otc = "NZDJPY_otc"
    NZDUSD_otc = "NZDUSD_otc"
    AAPL_otc = "#AAPL_otc"
    MSFT_otc = "#MSFT_otc"
    TSLA_otc = "#TSLA_otc"
    FB_otc = "#FB_otc"
    AMZN_otc = "#AMZN_otc"
    NFLX_otc = "#NFLX_otc"
    INTC_otc = "#INTC_otc"
    BA_otc = "#BA_otc"
    JNJ_otc = "#JNJ_otc"
    PFE_otc = "#PFE_otc"
    XOM_otc = "#XOM_otc"
    AXP_otc = "#AXP_otc"
    MCD_otc = "#MCD_otc"
    CSCO_otc = "#CSCO_otc"
    VISA_otc = "#VISA_otc"
    CITI_otc = "#CITI_otc"
    FDX_otc = "#FDX_otc"
    TWITTER_otc = "#TWITTER_otc"
    BABA_otc = "#BABA_otc"

    def is_otc(self) -> bool:
        return self.endswith("_otc")

    def __new__(cls, value: str) -> typing.Self:
        for member in cls:
            if member.value == value:
                return member

        obj = str.__new__(cls, value)
        obj._name_ = value
        obj._value_ = value
        return obj

    @classmethod
    def _missing_(cls, value: str) -> typing.Self:  # type: ignore
        """
        Create a new Asset instance for unknown values dynamically.
        Does NOT modify class attributes (avoids AttributeError).
        """
        obj = str.__new__(cls, value)
        obj._name_ = value
        obj._value_ = value

        # Register in value map so that repeated calls return the same object
        cls._value2member_map_[value] = obj

        return obj

    @classmethod
    def __get_validators__(cls):  # noqa: ANN206
        yield cls.validate

    @classmethod
    def validate(cls, value: typing.Any) -> typing.Self:
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            return cls(value)
        raise TypeError(f"Invalid type for Asset: {type(value)}")

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):  # noqa: ANN001, ANN206
        from pydantic_core import core_schema  # noqa: F811, PLC0415, RUF100

        return core_schema.no_info_after_validator_function(cls, core_schema.str_schema())


class AuthorizationData(BaseRequest):
    """
    PocketOption authorization payload.

    Contains authentication and client configuration data required
    to establish an authorized API session.

    This model is used during the authentication handshake and is sent
    to PocketOption server through the ``auth`` Socket.IO event.
    """

    session: str
    is_demo: typing.Annotated[
        IsDemo,
        pydantic.Field(..., alias="isDemo"),
    ]
    uid: int
    platform: int
    is_fast_history: typing.Annotated[
        bool,
        pydantic.Field(..., alias="isFastHistory"),
    ]
    is_optimized: typing.Annotated[
        bool,
        pydantic.Field(..., alias="isOptimized"),
    ]


class SuccessAuthEvent(BaseEvent):
    id: str


class SuccessUpdateBalanceEvent(BaseEvent):
    """
    Balance update event.

    Represents a successful balance synchronization event received
    from PocketOption after account balance changes or balance request.

    The event contains the account type and current account balance.

    :ivar is_demo:
        Account type for which the balance was updated.

    :ivar balance:
        Current account balance value.
    """

    is_demo: typing.Annotated[IsDemo, pydantic.Field(..., alias="isDemo")]
    balance: float


class UpdateHistoryFastEvent(BaseEvent):
    """
    Fast history update event.

    Represents a historical candle data update received from
    PocketOption using the fast history endpoint.

    The event contains the target asset, requested timeframe and
    raw historical price data.

    The ``history`` field contains serialized candle information
    as a list of numeric arrays. The exact array structure depends
    on PocketOption API response format.


    :ivar asset:
        Trading asset associated with historical data.

    :ivar period:
        Candle timeframe in seconds.

    :ivar history:
        Raw historical candle data returned by PocketOption API.

        Each item contains numeric values representing candle data.
    """

    asset: Asset
    period: int
    history: list[list[float]]


class UpdateCloseValueItem(BaseEvent):
    """
    Close value update item.

    Represents a single price update received from PocketOption.

    This model is used for real-time price stream updates and contains
    the asset identifier, event timestamp and current price value.

    :ivar asset: Trading asset associated with the update.
    :ivar timestamp: Unix timestamp of the price update.
    :ivar value: Current asset price value.
    """

    asset: Asset
    timestamp: float
    value: float


UpdateCloseValueListTypeAdapter = pydantic.TypeAdapter(list[UpdateCloseValueItem])


class OpenPendingDealRequestOpenType(enum.IntEnum):
    TIME = 0
    PRICE = 1


class Command(enum.IntEnum):
    CALL = 0
    PUT = 1


class Deal(BaseEvent):
    """
    Trading deal model.

    Represents a complete PocketOption trading deal.

    The model contains:
        - deal identification data;
        - trading parameters;
        - account information;
        - opening and closing timestamps;
        - price information;
        - profit and loss data;
        - additional deal metadata.

    A deal is created after successful order execution and is updated
    when the position is closed.


    :ivar id: Unique deal identifier.
    :ivar command: Trading command/action.
    :ivar asset: Trading asset.
    :ivar uid: PocketOption user identifier.
    :ivar amount: Deal investment amount.
    :ivar is_demo: Account type.
    :ivar profit: Deal profit or loss value.
    :ivar percent_profit: Profit percentage.
    :ivar percent_loss: Loss percentage.
    :ivar open_time: Deal opening datetime.
    :ivar close_time: Deal closing datetime.
    :ivar open_timestamp: Deal opening Unix timestamp.
    :ivar close_timestamp: Deal closing Unix timestamp.
    :ivar refund_time: Refund datetime if applicable.
    :ivar refund_timestamp: Refund Unix timestamp.
    :ivar open_price: Price at deal opening.
    :ivar close_price: Price at deal closing.
    :ivar copy_ticket: Copy trading ticket identifier.
    :ivar open_ms: Opening timestamp in milliseconds.
    :ivar close_ms: Closing timestamp in milliseconds.
    :ivar option_type: PocketOption option type identifier.
    :ivar is_rollover: Indicates rollover operation.
    :ivar is_copy_signal: Indicates deal created from copy signal.
    :ivar is_ai: Indicates AI-generated deal.
    :ivar currency: Deal currency.
    :ivar amount_usd: Deal amount converted to USD.
    :ivar request_id: Client request identifier used when opening the deal.
    """

    id: uuid.UUID
    command: Command
    asset: Asset

    uid: int
    amount: float
    is_demo: typing.Annotated[IsDemo, pydantic.Field(..., alias="isDemo")]

    profit: float
    percent_profit: typing.Annotated[float, pydantic.Field(..., alias="percentProfit")]
    percent_loss: typing.Annotated[float, pydantic.Field(..., alias="percentLoss")]

    open_time: typing.Annotated[datetime.datetime, pydantic.Field(..., alias="openTime")]
    close_time: typing.Annotated[datetime.datetime, pydantic.Field(..., alias="closeTime")]
    open_timestamp: typing.Annotated[float, pydantic.Field(..., alias="openTimestamp")]
    close_timestamp: typing.Annotated[float | None, pydantic.Field(None, alias="closeTimestamp")]
    refund_time: typing.Annotated[datetime.datetime | None, pydantic.Field(None, alias="refundTime")]
    refund_timestamp: typing.Annotated[int | None, pydantic.Field(None, alias="refundTimestamp")]

    open_price: typing.Annotated[float, pydantic.Field(..., alias="openPrice")]
    close_price: typing.Annotated[float | None, pydantic.Field(None, alias="closePrice")]

    copy_ticket: typing.Annotated[str, pydantic.Field(..., alias="copyTicket")]
    open_ms: typing.Annotated[int | None, pydantic.Field(None, alias="openMs")]
    close_ms: typing.Annotated[int | None, pydantic.Field(None, alias="closeMs")]
    option_type: typing.Annotated[int | None, pydantic.Field(None, alias="optionType")]
    is_rollover: typing.Annotated[bool | None, pydantic.Field(None, alias="isRollover")]
    is_copy_signal: typing.Annotated[bool, pydantic.Field(..., alias="isCopySignal")]
    is_ai: typing.Annotated[bool | None, pydantic.Field(None, alias="isAI")]
    currency: str
    amount_usd: typing.Annotated[float | None, pydantic.Field(None, alias="amountUSD")]
    request_id: typing.Annotated[int | None, pydantic.Field(None, alias="requestId")]

    @property
    def closed(self) -> bool:
        return self.close_timestamp is not None


DealListTypeAdapter = pydantic.TypeAdapter(list[Deal])


class DealAction(enum.StrEnum):
    CALL = "call"
    PUT = "put"


class OpenDealRequest(BaseRequest):
    """
    Request model for opening a new trading deal.

    Contains parameters required to create a new order through
    the PocketOption API.

    :ivar asset:
        Trading asset for the deal.

    :ivar amount:
        Investment amount.

    :ivar action:
        Trading action direction.

    :ivar is_demo:
        Account type used for the deal.

    :ivar request_id:
        Unique client request identifier.

    :ivar option_type:
        Deal option type identifier.

    :ivar time:
        Deal duration in seconds.
    """

    model_config = pydantic.ConfigDict(validate_by_name=True, validate_by_alias=True)

    asset: Asset
    amount: int
    action: DealAction
    is_demo: typing.Annotated[IsDemo, pydantic.Field(..., alias="isDemo")]
    request_id: typing.Annotated[int, pydantic.Field(..., alias="requestId")]
    option_type: typing.Annotated[int, pydantic.Field(..., alias="optionType")]
    time: int


class CopySignalRequest(BaseRequest):
    """
    Request model for copy trading signal execution.

    Contains signal metadata and trading parameters required
    to replicate a trading action.

    :ivar symbol:
        Trading asset associated with the signal.

    :ivar amount:
        Investment amount.

    :ivar expired_at:
        Signal expiration timestamp.

    :ivar action:
        Trading action direction.

    :ivar is_demo:
        Account type used for execution.

    :ivar request_id:
        Client request identifier.

    :ivar created_at:
        Signal creation timestamp.

    :ivar timeframe:
        Signal timeframe.

    :ivar signal_id:
        Identifier of the source signal.
    """

    symbol: Asset
    amount: int
    expired_at: typing.Annotated[int, pydantic.Field(..., alias="expiredAt")]
    action: DealAction
    is_demo: typing.Annotated[IsDemo, pydantic.Field(..., alias="isDemo")]
    request_id: typing.Annotated[int, pydantic.Field(..., alias="requestId")]
    created_at: typing.Annotated[int, pydantic.Field(..., alias="createdAt")]
    timeframe: int
    signal_id: typing.Annotated[str, pydantic.Field(..., alias="signalId")]


class OpenPendingDealRequest(BaseRequest):
    """
    Request model for creating a pending trading deal.

    Defines conditions required for delayed order execution.

    :ivar open_type:
        Pending order opening mode.

    :ivar amount:
        Investment amount.

    :ivar asset:
        Trading asset.

    :ivar open_time:
        Target opening time.

    :ivar open_price:
        Target opening price.

    :ivar timeframe:
        Deal duration timeframe.

    :ivar min_payout:
        Minimum required payout.

    :ivar command:
        Trading command.
    """

    open_type: typing.Annotated[OpenPendingDealRequestOpenType, pydantic.Field(..., alias="openType")]
    amount: int
    asset: Asset
    open_time: typing.Annotated[str, pydantic.Field(..., alias="openTime")]
    open_price: typing.Annotated[int, pydantic.Field(..., alias="openPrice")]
    timeframe: int
    min_payout: typing.Annotated[int, pydantic.Field(..., alias="minPayout")]
    command: Command


class ChangeAssetRequest(BaseRequest):
    """
    Request model for changing active trading asset subscription.

    :ivar asset: Trading asset to subscribe.
    :ivar period: Market update period.
    """

    asset: Asset
    period: int


class SuccessCloseDealEvent(BaseEvent):
    profit: float
    deals: list[Deal]


class AssetType(enum.StrEnum):
    """
    Trading asset category.

    Defines a group of supported financial instruments.
    """

    STOCK = "stock"
    COMMODITY = "commodity"
    CURRENCY = "currency"
    CRYPTOCURRENCY = "cryptocurrency"
    INDEX = "index"


class AssetItemTimeframe(BaseEvent):
    """
    Asset timeframe configuration.

    :ivar time:
        Available timeframe value.
    """

    time: int


class UpdateAssetItem(BaseEvent):
    """
    Model describing an asset update item received from the trading server.

    Contains asset metadata, payout information, expiration settings,
    OTC mapping, availability status, and supported timeframes.

    :ivar id: Unique asset identifier.
    :ivar asset: Asset symbol identifier.
    :ivar label: Human-readable asset name.
    :ivar type: Asset category.

    :ivar digits: Number of decimal places used for asset prices.
    :ivar payout: Current payout percentage for the asset.
    :ivar default_expiration: Default trade expiration time in seconds.
    :ivar min_expiration: Minimum allowed trade expiration time in seconds.
    :ivar expiration_step: Step size for changing expiration time in seconds.

    :ivar is_otc: Whether the asset is an OTC asset.
    :ivar otc_id: Identifier of the OTC asset counterpart.
    :ivar real_id: Identifier of the real market asset counterpart.

    :ivar signals: Additional asset signals or metadata provided by the server.

    :ivar exp_time: Asset expiration timestamp.
    :ivar active: Whether the asset is currently available for trading.

    :ivar timeframes: List of supported trade expiration timeframes.
    :ivar scheduled_until: Timestamp until which the asset schedule is valid.
    :ivar min_quick_timeframe: Minimum timeframe available for quick trades.
    :ivar scheduled_at: Timestamp when the asset schedule was created.
    """

    id: int
    asset: Asset
    label: str
    type: AssetType

    digits: int
    payout: int

    default_expiration: int
    min_expiration: int
    expiration_step: int

    is_otc: bool
    otc_id: int
    real_id: int

    signals: list[typing.Any]

    exp_time: int
    active: bool

    timeframes: list[AssetItemTimeframe]

    scheduled_until: int
    min_quick_timeframe: int
    scheduled_at: int


UpdateAssetItemListTypeAdapter = pydantic.TypeAdapter(list[UpdateAssetItem])


class MarketSentimentItem(BaseEvent):
    """
    Market sentiment data model.

    :ivar asset:
        Trading asset.

    :ivar value:
        Sentiment value.
    """

    asset: Asset
    value: int


MarketSentimentItemListTypeAdapter = pydantic.TypeAdapter(list[MarketSentimentItem])


class LoadHistoryPeriodRequest(BaseRequest):
    """
    Request historical candlestick data for a specific time range.

    :ivar asset: Trading asset.
    :ivar index:
    :ivar time: Timestamp.
    :ivar offset:
    :ivar period: Candle timeframe in seconds
    """

    asset: Asset
    index: int | None
    time: float
    offset: int
    period: int


class LoadHistoryPeriodItem(BaseEvent):
    """
    Historical candlestick (OHLCV) data.

    :ivar symbol_id:
    :ivar time:     Candle opening time as a Unix timestamp in seconds.
    :ivar open:     Opening price.
    :ivar close:    Closing price.
    :ivar high:     Highest price during the candle.
    :ivar low:      Lowest price during the candle.
    :ivar volume:   Tick volume for the candle.
    """

    symbol_id: int
    time: int
    open: float
    close: float
    high: float
    low: float
    volume: int


class LoadHistoryPeriodFastResponse(BaseEvent):
    """
    Response containing historical candlestick data.

    :ivar asset:    Trading asset.
    :ivar index:
    :ivar period:   Candle timeframe in seconds.
    :ivar data:     List of historical candlesticks.
    """

    asset: Asset
    index: int | None
    period: int
    data: list[LoadHistoryPeriodItem]


class CopyOrderRequest(BaseRequest):
    """
    Request to copy an existing order.

    :ivar ticket:    Deal ID to copy.
    """

    ticket: typing.Annotated[uuid.UUID, pydantic.Field(alias="copyTicket")]


class DealsDoubleUpRequest(BaseRequest):
    """
    Request to double up an existing order.

    :ivar ticket:    Deal ID to double up.
    """

    ticket: uuid.UUID


class DealsRolloverRequest(BaseRequest):
    ticket: uuid.UUID
    amount: float


class CancelPendingDealRequest(BaseRequest):
    ticket: uuid.UUID
