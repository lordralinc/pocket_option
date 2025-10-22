import contextlib

from pocket_option.types import JsonFunction, JsonValue

__all__ = ("get_json_function",)


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
