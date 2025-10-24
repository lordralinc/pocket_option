import datetime
import enum
import typing
import uuid

import pydantic

__all__ = (
    "Asset",
    "AuthorizationData",
    "ChangeSymbolRequest",
    "Command",
    "CopySignalRequest",
    "Deal",
    "IsDemo",
    "OpenOrderRequest",
    "OpenPendingOrderRequest",
    "OpenPendingOrderRequestOpenType",
    "OrderAction",
    "SuccessUpdateBalance",
    "UpdateHistoryFastEvent",
    "UpdateStreamItem",
    "UpdateStreamTypeAdapter",
)

type IsDemo = typing.Literal[0, 1]


class Asset(str, enum.Enum):
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

    def __new__(cls, value: str) -> "Asset":
        for member in cls:
            if member.value == value:
                return member

        obj = str.__new__(cls, value)
        obj._name_ = value
        obj._value_ = value
        return obj

    @classmethod
    def _missing_(cls, value: str) -> "Asset":  # type: ignore
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
    def validate(cls, value: typing.Any) -> "Asset":
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            return cls(value)
        raise TypeError(f"Invalid type for Asset: {type(value)}")

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):  # noqa: ANN001, ANN206
        from pydantic_core import core_schema  # noqa: F811, PLC0415, RUF100

        return core_schema.no_info_after_validator_function(cls, core_schema.str_schema())


class AuthorizationData(pydantic.BaseModel):
    session: str
    is_demo: typing.Annotated[IsDemo, pydantic.Field(..., alias="isDemo")]
    uid: int
    platform: int
    is_fast_history: typing.Annotated[bool, pydantic.Field(..., alias="isFastHistory")]
    is_optimized: typing.Annotated[bool, pydantic.Field(..., alias="isOptimized")]


class SuccessUpdateBalance(pydantic.BaseModel):
    is_demo: typing.Annotated[IsDemo, pydantic.Field(..., alias="isDemo")]
    balance: float


class UpdateHistoryFastEvent(pydantic.BaseModel):
    asset: Asset
    period: int
    history: list[list[float]]


class UpdateStreamItem(pydantic.BaseModel):
    asset: Asset
    timestamp: float
    value: float


UpdateStreamTypeAdapter = pydantic.TypeAdapter(list[UpdateStreamItem])


class OpenPendingOrderRequestOpenType(enum.IntEnum):
    TIME = 0
    PRICE = 1


class Command(enum.IntEnum):
    PUT = 0
    CALL = 1


class Deal(pydantic.BaseModel):
    id: uuid.UUID
    open_time: typing.Annotated[datetime.datetime, pydantic.Field(..., alias="openTime")]
    close_time: typing.Annotated[datetime.datetime, pydantic.Field(..., alias="closeTime")]
    open_timestamp: typing.Annotated[float, pydantic.Field(..., alias="openTimestamp")]
    close_timestamp: typing.Annotated[float | None, pydantic.Field(None, alias="closeTimestamp")]
    refund_time: typing.Annotated[datetime.datetime | None, pydantic.Field(None, alias="refundTime")]
    refund_timestamp: typing.Annotated[int | None, pydantic.Field(None, alias="refundTimestamp")]
    uid: int
    amount: float
    profit: float
    percent_profit: typing.Annotated[float, pydantic.Field(..., alias="percentProfit")]
    percent_loss: typing.Annotated[float, pydantic.Field(..., alias="percentLoss")]
    open_price: typing.Annotated[float, pydantic.Field(..., alias="openPrice")]
    close_price: typing.Annotated[float | None, pydantic.Field(None, alias="closePrice")]
    command: Command
    asset: Asset
    is_demo: typing.Annotated[IsDemo, pydantic.Field(..., alias="isDemo")]
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


DealListTypeAdapter = pydantic.TypeAdapter(list[Deal])


class OrderAction(enum.StrEnum):
    CALL = "call"
    PUT = "put"


class OpenOrderRequest(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(validate_by_name=True, validate_by_alias=True)

    asset: Asset
    amount: int
    action: OrderAction
    is_demo: typing.Annotated[IsDemo, pydantic.Field(..., alias="isDemo")]
    request_id: typing.Annotated[int, pydantic.Field(..., alias="requestId")]
    option_type: typing.Annotated[int, pydantic.Field(..., alias="optionType")]
    time: int


class CopySignalRequest(pydantic.BaseModel):
    symbol: Asset
    amount: int
    expired_at: typing.Annotated[int, pydantic.Field(..., alias="expiredAt")]
    action: OrderAction
    is_demo: typing.Annotated[IsDemo, pydantic.Field(..., alias="isDemo")]
    request_id: typing.Annotated[int, pydantic.Field(..., alias="requestId")]
    created_at: typing.Annotated[int, pydantic.Field(..., alias="createdAt")]
    timeframe: int
    signal_id: typing.Annotated[str, pydantic.Field(..., alias="signalId")]


class OpenPendingOrderRequest(pydantic.BaseModel):
    open_type: typing.Annotated[OpenPendingOrderRequestOpenType, pydantic.Field(..., alias="openType")]
    amount: int
    asset: Asset
    open_time: typing.Annotated[str, pydantic.Field(..., alias="openTime")]
    open_price: typing.Annotated[int, pydantic.Field(..., alias="openPrice")]
    timeframe: int
    min_payout: typing.Annotated[int, pydantic.Field(..., alias="minPayout")]
    command: Command


class ChangeSymbolRequest(pydantic.BaseModel):
    asset: Asset
    period: int


class SuccessCloseOrder(pydantic.BaseModel):
    profit: float
    deals: list[Deal]
