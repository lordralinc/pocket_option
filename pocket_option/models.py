import typing

__all__ = ("AuthorizationData", "SuccessUpdateBalance", "UpdateHistoryFastEvent")


class AuthorizationData(typing.TypedDict):
    session: str
    isDemo: typing.Literal[0, 1]
    uid: int
    platform: int
    isFastHistory: bool
    isOptimized: bool


class SuccessUpdateBalance(typing.TypedDict):
    isDemo: typing.Literal[0, 1]
    balance: float


class UpdateHistoryFastEvent(typing.TypedDict):
    asset: str
    period: int
    history: list[list[float]]


class UpdateStreamItem(typing.TypedDict):
    asset: str
    timestamp: float
    value: float


class Deal(typing.TypedDict):
    id: str
    openTime: float
    closeTime: float
    openTimestamp: int
    closeTimestamp: typing.NotRequired[int | None]
    refundTime: typing.NotRequired[float | None]
    refundTimestamp: typing.NotRequired[int | None]
    uid: int
    amount: float
    profit: float
    percentProfit: float
    percentLoss: float
    openPrice: float
    closePrice: typing.NotRequired[float | None]
    command: int
    asset: str
    isDemo: typing.Literal[0, 1]
    copyTicket: str
    openMs: typing.NotRequired[int | None]
    closeMs: typing.NotRequired[int | None]
    optionType: typing.NotRequired[int | None]
    isRollover: bool
    isCopySignal: bool
    isAI: bool
    currency: str
    amountUSD: typing.NotRequired[float | None]
    requestId: typing.NotRequired[int | None]




class OpenOrderRequest(typing.TypedDict):
    asset: str
    amount: int
    action: typing.Literal["call", "put"]
    isDemo: typing.Literal[0, 1]
    requestId: int
    optionType: int
    time: int
