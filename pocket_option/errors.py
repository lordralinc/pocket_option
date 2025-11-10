import typing

__all__ = ("DealError", "DealErrorCode")

type DealErrorCode = typing.Literal[
    "min_amount",
    "max_amount",
    "min_duration",
    "max_duration",
    "max_orders",
    "timeout",
    "not_found",
]


class DealError(ValueError):
    def __init__(self, code: DealErrorCode, message: str, extras: dict | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.extras = extras

    def __str__(self) -> str:
        return f"[{self.code}] {self.message} {self.extras!r}"
