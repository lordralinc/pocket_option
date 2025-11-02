import contextlib
import inspect
import random
import time
import typing
from collections import deque

from pocket_option.constants import TIMESTAMP_OFFSET
from pocket_option.types import JsonFunction, JsonValue

__all__ = ("append_or_replace", "fix_timestamp", "generate_request_id", "get_json_function")

rnd = random.SystemRandom()


def get_function_full_name(fn: typing.Callable) -> str:
    if inspect.isclass(fn):
        return fn.__name__ + ".__init__"
    if fn.__module__:
        return f"{fn.__module__}.{fn.__qualname__}"
    return fn.__qualname__


def get_json_function() -> JsonFunction:
    with contextlib.suppress(ImportError):
        import ujson  # type: ignore  # noqa: PLC0415

        class _UJson:
            def loads(self, value: str | bytes) -> JsonValue:
                return ujson.loads(value)

            def dumps(self, value: JsonValue, *, separators: tuple[str, str] | None = None) -> str:
                return ujson.dumps(value, ensure_ascii=False, separators=separators)

        return _UJson()

    import json  # noqa: PLC0415

    class _JsonLoads:
        def loads(self, value: str | bytes) -> JsonValue:
            return json.loads(value)

        def dumps(self, value: JsonValue, *, separators: tuple[str, str] | None = None) -> str:
            return json.dumps(value, ensure_ascii=False, separators=separators)

    return _JsonLoads()


def fix_timestamp(ts: float) -> float:
    return ts + TIMESTAMP_OFFSET


@typing.overload
def append_or_replace[T](
    array: list[T],
    item: T,
    eq_by_keys: list[str],
    get_key_method: typing.Callable[[T, str], typing.Any] = getattr,
) -> list[T]: ...
@typing.overload
def append_or_replace[T](
    array: deque[T],
    item: T,
    eq_by_keys: list[str],
    get_key_method: typing.Callable[[T, str], typing.Any] = getattr,
) -> deque[T]: ...
def append_or_replace[T](
    array: list[T] | deque[T],
    item: T,
    eq_by_keys: list[str],
    get_key_method: typing.Callable[[T, str], typing.Any] = getattr,
) -> list[T] | deque[T]:
    for i, it in enumerate(array):
        if all(get_key_method(it, key) == get_key_method(item, key) for key in eq_by_keys):
            array[i] = item
            return array
    array.append(item)
    return array


def generate_request_id() -> int:
    return int(time.time()) - TIMESTAMP_OFFSET + rnd.randint(1, 100)
