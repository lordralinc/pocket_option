import contextlib
import typing

from pocket_option.middleware import Middleware
from pocket_option.utils import fix_timestamp, get_json_function

if typing.TYPE_CHECKING:
    from pocket_option.types import JsonValue

__all__ = (
    "FixTypesOnMiddleware",
    "MakeJsonOnMiddleware",
)


class MakeJsonOnMiddleware(Middleware):
    def __init__(self) -> None:
        self.json = get_json_function()

    async def on(self, event: str, data: "str | bytes | JsonValue | None") -> "JsonValue | None":  # noqa: ARG002
        if isinstance(data, str | bytes):
            with contextlib.suppress(Exception):
                return self.json.loads(data)
        return typing.cast("JsonValue", data)


class FixTypesOnMiddleware(Middleware):
    async def on(self, event: str, data: "JsonValue | None") -> "JsonValue | None":  # type: ignore
        if data is None:
            return None
        if event == "updateStream":
            return [
                {
                    "asset": it[0],
                    "timestamp": fix_timestamp(it[1]),
                    "value": it[2],
                }
                for it in typing.cast("list[tuple[str, float, float]]", data)
            ]
        return data
