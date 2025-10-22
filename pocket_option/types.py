import collections.abc
import typing

__all__ = ("EmitCallback", "JsonFunction", "JsonValue", "SIOEventListener", "TypedEventListener")


type JsonValue = int | float | str | "dict[str, JsonValue]" | "list[JsonValue]"


class JsonFunction(typing.Protocol):
    def dumps(self, value: JsonValue, *, separators: tuple[str, str] | None = None) -> JsonValue: ...
    def loads(self, value: str | bytes) -> JsonValue: ...


type EmitCallback[T] = (
    collections.abc.Callable[
        [str, int, T],
        None,
    ]
    | collections.abc.Callable[
        [str, int, T],
        collections.abc.Coroutine[None, None, None],
    ]
)
type SIOEventListener = (
    collections.abc.Callable[..., None] | collections.abc.Callable[..., collections.abc.Coroutine[None, None, None]]
)

type TypedEventListener[T] = (
    collections.abc.Callable[[T], None] | collections.abc.Callable[[T], collections.abc.Coroutine[None, None, None]]
)
