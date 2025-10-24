import typing

if typing.TYPE_CHECKING:
    from pocket_option.types import EmitCallback, JsonValue

__all__ = ("Middleware",)


class Middleware:
    async def emit(
        self,
        event: str,
        data: "JsonValue | None" = None,
        callback: "EmitCallback[JsonValue] | None" = None,
    ) -> "tuple[str, JsonValue | None, EmitCallback[JsonValue] | None]":
        return event, data, callback

    async def on(self, event: str, data: "str | bytes | JsonValue | None") -> "JsonValue | None":  # noqa: ARG002
        return data  # type: ignore
