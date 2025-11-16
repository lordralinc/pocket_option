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


UPDATE_ITEMS_NAMES = [
    "id",  # ID актива
    "symbol",  # Символ (#AAPL)
    "label",  # Название (Apple)
    "type",  # Тип (stock, forex, crypto и т.д.)
    "precision",  # Кол-во знаков после запятой
    "payout",  # Выплата (%)
    "min_duration",  # Мин. длительность сделки
    "max_duration",  # Макс. длительность сделки
    "step_duration",  # Шаг длительности
    "volatility_index",  # Индекс волатильности / флаг
    "spread",  # Спред / коэффициент
    "leverage",  # Плечо
    "extra_data",  # Доп. данные (список или null)
    "expire_time",  # Метка времени окончания (timestamp)
    "is_active",  # Активен ли актив
    "timeframes",  # Список доступных таймфреймов [{time: 60}, ...]
    "start_time",  # Время старта (timestamp)
    "default_timeframe",  # Таймфрейм по умолчанию
    "status_code",  # Статус / код состояния
]


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
        if event == "updateAssets":
            return [dict(zip(UPDATE_ITEMS_NAMES, it, strict=True)) for it in typing.cast("list[list]", data)]
        if event == "chafor":
            return [dict(zip(["asset", "value"], it, strict=True)) for it in typing.cast("list[list]", data)]

        return data
