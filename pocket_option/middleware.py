import abc
import typing

if typing.TYPE_CHECKING:
    from pocket_option.types import EmitCallback, JsonValue


class EmitMiddleware(abc.ABC):
    @abc.abstractmethod
    async def emit(
        self,
        event: str,
        data: "JsonValue | None" = None,
        callback: "EmitCallback[JsonValue] | None" = None,
    ) -> "tuple[str, JsonValue | None, EmitCallback[JsonValue] | None]": ...
