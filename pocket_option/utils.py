from __future__ import annotations

import contextlib
import datetime
import inspect
import random
import time
import typing
from dataclasses import dataclass

from pocket_option.constants import TIMESTAMP_OFFSET

if typing.TYPE_CHECKING:
    from collections import deque
    from collections.abc import Callable

    from pocket_option.types import JsonFunction, JsonValue

__all__ = ("Q", "append_or_replace", "fix_timestamp", "generate_index", "generate_request_id", "get_json_function")

rnd = random.SystemRandom()


@dataclass(slots=True)
class Q:
    """
    Query expression builder.

    Provides a lightweight filtering system inspired by ORM query objects.

    Q objects encapsulate boolean predicates and can be combined using
    logical operators:

        - ``&`` creates AND expressions.
        - ``|`` creates OR expressions.
        - ``~`` creates NOT expressions.

    This allows building reusable and composable filters.

    Example:

        query = (
            Q.field("asset", "eq", Asset.AUDCAD_otc)
            &
            Q.field("price", "gte", 10)
        )

        filtered = [
            item
            for item in items
            if query(item)
        ]

    Field lookup expressions are created using :meth:`field`.

    Supported operators:

        - ``eq``:
            Field equals value.

        - ``gt``:
            Field greater than value.

        - ``gte``:
            Field greater than or equal to value.

        - ``lt``:
            Field less than value.

        - ``lte``:
            Field less than or equal to value.

        - ``isnull``:
            Checks whether field value is None.

    DateTime fields are automatically converted to Unix timestamps
    before comparison.

    """

    func: Callable[[typing.Any], bool]

    def __call__(self, obj: typing.Any) -> bool:
        return self.func(obj)

    def __and__(self, other: Q) -> Q:
        return Q(lambda obj: self(obj) and other(obj))

    def __or__(self, other: Q) -> Q:
        return Q(lambda obj: self(obj) or other(obj))

    def __invert__(self) -> Q:
        return Q(lambda obj: not self(obj))

    @classmethod
    def field(
        cls,
        name: str,
        op: str,
        value: typing.Any,
    ) -> typing.Self:
        """
        Create field comparison query.

        Generates a predicate that compares an object attribute with
        the provided value.

        The attribute value is retrieved using ``getattr``.
        datetime values are automatically converted to Unix timestamps
        before comparison.

        Example:

            query = Q.field(
                "asset",
                "eq",
                Asset.AUDCAD_otc,
            )

        Supported operators:

            - eq
            - gt
            - gte
            - lt
            - lte
            - isnull

        :param name: Object attribute name.
        :type name: str

        :param op: Comparison operator.
        :type op: str

        :param value: Value to compare against.
        :type value: typing.Any

        :raises ValueError: If operator is not supported.

        :return: Query expression.
        :rtype: Q
        """

        def getter(obj: typing.Any):
            result = getattr(obj, name)
            if isinstance(result, datetime.datetime):
                return result.timestamp()
            return result

        match op:
            case "eq":
                return cls(lambda obj: getter(obj) == value)

            case "gt":
                return cls(lambda obj: getter(obj) > value)

            case "gte":
                return cls(lambda obj: getter(obj) >= value)

            case "lt":
                return cls(lambda obj: getter(obj) < value)

            case "lte":
                return cls(lambda obj: getter(obj) <= value)

            case "isnull":
                return cls(lambda obj: (getter(obj) is None) == value)

            case _:
                raise ValueError(op)


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


def get_server_time() -> float:
    return time.time() - TIMESTAMP_OFFSET


def generate_request_id() -> int:
    return int(get_server_time()) + rnd.randint(1, 100)


def generate_index() -> int:
    return int(f"{int(get_server_time())}{rnd.randint(1, 100)}")
