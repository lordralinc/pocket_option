import abc
import collections.abc
import datetime
import math
import typing
from collections import defaultdict, deque

import pydantic
import pytz

from pocket_option.generated_client import PocketOptionClient
from pocket_option.models import Asset, UpdateStreamItem
from pocket_option.utils import append_or_replace

if typing.TYPE_CHECKING:
    from pocket_option.generated_client import PocketOptionClient


class Candle(pydantic.BaseModel):
    asset: Asset
    timestamp: datetime.datetime
    timeframe: int
    open: float
    low: float
    high: float
    close: float


class CandleStorage(abc.ABC):
    def __init__(self, client: "PocketOptionClient") -> None:
        self.client = client

        self.client.on.update_stream(self._on_update_stream)

    async def _on_update_stream(self, items: list[UpdateStreamItem]) -> None:
        await self.add_item_bulk(items)

    async def add_candle(self, candle: Candle) -> None:
        await self.add_item_bulk(
            [
                UpdateStreamItem(asset=candle.asset, timestamp=candle.timestamp.timestamp(), value=candle.open),
                UpdateStreamItem(asset=candle.asset, timestamp=candle.timestamp.timestamp() + 0.01, value=candle.low),
                UpdateStreamItem(asset=candle.asset, timestamp=candle.timestamp.timestamp() + 0.02, value=candle.high),
                UpdateStreamItem(
                    asset=candle.asset,
                    timestamp=candle.timestamp.timestamp() + (candle.timeframe - 0.01),
                    value=candle.close,
                ),
            ],
        )

    @abc.abstractmethod
    async def add_item(self, item: UpdateStreamItem): ...
    @abc.abstractmethod
    async def add_item_bulk(self, items: list[UpdateStreamItem]): ...
    @abc.abstractmethod
    async def get_items(
        self,
        asset: Asset,
        *,
        start: datetime.datetime | None = None,
        end: datetime.datetime | None = None,
        count: int | None = None,
    ) -> collections.abc.Iterable[UpdateStreamItem]: ...

    async def get_candles(
        self,
        asset: Asset,
        timeframe: int = 5,
        *,
        start: datetime.datetime | None = None,
        end: datetime.datetime | None = None,
        count: int | None = None,
    ) -> collections.abc.Iterable[Candle]:
        items = await self.get_items(asset, start=start, end=end, count=count)

        buckets: dict[int, list[UpdateStreamItem]] = defaultdict(list)
        for item in items:
            ts_bucket = math.floor(item.timestamp / timeframe) * timeframe
            buckets[ts_bucket].append(item)
        candles = []

        for ts_bucket in sorted(buckets):
            group = buckets[ts_bucket]
            values = [i.value for i in group]
            candle = Candle(
                asset=asset,
                timestamp=datetime.datetime.fromtimestamp(ts_bucket, tz=pytz.UTC),
                timeframe=timeframe,
                open=values[0],
                close=values[-1],
                high=max(values),
                low=min(values),
            )
            candles.append(candle)

        return candles


class MemoryCandleStorage(CandleStorage):
    def __init__(self, client: "PocketOptionClient") -> None:
        super().__init__(client)
        self._max_len = 10_000
        self._storage: dict[Asset, deque[UpdateStreamItem]] = defaultdict(lambda: deque([], 10_000))

    def set_max_len(self, _max_len: int):
        self._storage = defaultdict(lambda: deque([], _max_len))

    async def add_item(self, item: UpdateStreamItem):
        self._storage[item.asset] = append_or_replace(self._storage[item.asset], item, ["asset", "timestamp"])

    async def add_item_bulk(self, items: list[UpdateStreamItem]):
        for it in items:
            await self.add_item(it)

    async def get_items(
        self,
        asset: Asset,
        *,
        start: datetime.datetime | None = None,
        end: datetime.datetime | None = None,
        count: int | None = None,
    ) -> collections.abc.Iterable[UpdateStreamItem]:
        items = self._storage.get(asset, [])
        if start:
            items = [i for i in items if i.timestamp >= start.timestamp()]
        if end:
            items = [i for i in items if i.timestamp <= end.timestamp()]
        items = list(items)
        items.sort(key=lambda i: i.timestamp)
        if count is not None:
            items = items[-count:]
        return items
