from __future__ import annotations

import abc
import collections.abc
import datetime
import math
import typing
from collections import defaultdict, deque
from itertools import chain

import pydantic
import pytz

from pocket_option.generated_client import PocketOptionClient
from pocket_option.models import Asset, LoadHistoryPeriodFastResponse, UpdateCloseValueItem
from pocket_option.utils import append_or_replace

if typing.TYPE_CHECKING:
    from pocket_option.generated_client import PocketOptionClient

__all__ = ("Candle", "CandleStorage", "MemoryCandleStorage")


class Candle(pydantic.BaseModel):
    asset: Asset
    timestamp: datetime.datetime
    timeframe: int
    open: float
    low: float
    high: float
    close: float


class CandleStorage(abc.ABC):
    """
    Abstract candle storage.

    CandleStorage stores raw price updates and provides OHLC candle
    aggregation.

    The storage subscribes to PocketOption close value updates and converts
    incoming price events into stored items.

    Raw price updates are represented by UpdateCloseValueItem.
    Candles are generated dynamically using timeframe buckets.

    Example:

        candles = await storage.get_candles(
            Asset.AUDCAD_otc,
            timeframe=60,
            count=100,
        )

    """

    def __init__(self, client: PocketOptionClient) -> None:
        self.client = client

        self.client.on.update_close_value(self._on_update_close_value)
        self.client.on.load_history_period_fast(self._on_load_history_period_fast)

    async def _on_load_history_period_fast(self, data: LoadHistoryPeriodFastResponse) -> None:
        await self.add_item_bulk(
            list(
                chain.from_iterable(
                    [
                        [
                            UpdateCloseValueItem(asset=data.asset, timestamp=it.time, value=it.open),
                            UpdateCloseValueItem(
                                asset=data.asset,
                                timestamp=it.time + 0.01,
                                value=it.low,
                            ),
                            UpdateCloseValueItem(
                                asset=data.asset,
                                timestamp=it.time + 0.02,
                                value=it.high,
                            ),
                            UpdateCloseValueItem(
                                asset=data.asset,
                                timestamp=it.time + (data.period - 0.01),
                                value=it.close,
                            ),
                        ]
                        for it in data.data
                    ],
                ),
            ),
        )

    async def _on_update_close_value(self, items: list[UpdateCloseValueItem]) -> None:
        await self.add_item_bulk(items)

    async def add_candle(self, candle: Candle) -> None:
        """
        Add complete candle into storage.

        The candle is converted into synthetic price updates:

        - open  -> timestamp + 0.00
        - low   -> timestamp + 0.01
        - high  -> timestamp + 0.02
        - close -> timestamp + timeframe - 0.01

        This allows candle reconstruction through the same aggregation
        mechanism used for live market data.
        """
        await self.add_item_bulk(
            [
                UpdateCloseValueItem(asset=candle.asset, timestamp=candle.timestamp.timestamp(), value=candle.open),
                UpdateCloseValueItem(
                    asset=candle.asset,
                    timestamp=candle.timestamp.timestamp() + 0.01,
                    value=candle.low,
                ),
                UpdateCloseValueItem(
                    asset=candle.asset,
                    timestamp=candle.timestamp.timestamp() + 0.02,
                    value=candle.high,
                ),
                UpdateCloseValueItem(
                    asset=candle.asset,
                    timestamp=candle.timestamp.timestamp() + (candle.timeframe - 0.01),
                    value=candle.close,
                ),
            ],
        )

    @abc.abstractmethod
    async def add_item(self, item: UpdateCloseValueItem):
        """
        Store a single price update.

        Must be implemented by subclasses.
        """

    @abc.abstractmethod
    async def add_item_bulk(self, items: list[UpdateCloseValueItem]):
        """
        Store multiple price updates.

        Must be implemented by subclasses.
        """

    @abc.abstractmethod
    async def get_items(
        self,
        asset: Asset,
        *,
        start: datetime.datetime | None = None,
        end: datetime.datetime | None = None,
        count: int | None = None,
    ) -> collections.abc.Iterable[UpdateCloseValueItem]:
        """
        Retrieve raw price updates.

        :param asset: Asset to query.
        :type asset: Asset

        :param start: Minimum timestamp filter.
        :type start: datetime.datetime | None

        :param end: Maximum timestamp filter.
        :type end: datetime.datetime | None

        :param count: Maximum number of latest items.
        :type count: int | None

        :return: Iterable of price updates ordered by timestamp.
        :rtype: collections.abc.Iterable[UpdateCloseValueItem]
        """

    async def get_candles(
        self,
        asset: Asset,
        timeframe: int = 5,
        *,
        start: datetime.datetime | None = None,
        end: datetime.datetime | None = None,
        count: int | None = None,
    ) -> collections.abc.Iterable[Candle]:
        """
        Build OHLC candles from stored price updates.

        Price updates are grouped into timeframe buckets:

            bucket = floor(timestamp / timeframe) * timeframe

        For each bucket:

            open  = first price
            close = last price
            high  = maximum price
            low   = minimum price


        :param asset: Asset to build candles for.
        :type asset: Asset

        :param timeframe: Candle size in seconds.
        :type timeframe: int

        :param start: Start datetime filter.
        :type start: datetime.datetime | None

        :param end: End datetime filter.
        :type end: datetime.datetime | None

        :param count: Number of latest candles.
        :type count: int | None

        :return: Iterable of generated candles.
        :rtype: collections.abc.Iterable[Candle]
        """
        items = await self.get_items(asset, start=start, end=end, count=count)

        buckets: dict[int, list[UpdateCloseValueItem]] = defaultdict(list)
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
    """
    In-memory candle storage.

    Stores raw price updates in memory using bounded deques.

    Features:
        - separate storage per asset;
        - automatic replacement of duplicate timestamps;
        - configurable maximum history size.

    Data is lost after process restart.

    Example:

        storage = MemoryCandleStorage(client)
        ...
        candles = await storage.get_candles(
            Asset.AUDCAD_otc,
            timeframe=60,
        )
    """

    def __init__(self, client: PocketOptionClient) -> None:
        super().__init__(client)
        self._max_len = 10_000
        self._storage: dict[Asset, deque[UpdateCloseValueItem]] = defaultdict(lambda: deque(maxlen=10_000))

    def set_max_len(self, _max_len: int):
        """
        Change maximum number of stored price updates per asset.


        :param max_len: Maximum deque size.
        :type max_len: int
        """
        self._storage = defaultdict(lambda: deque(maxlen=_max_len))

    async def add_item(self, item: UpdateCloseValueItem):
        self._storage[item.asset] = append_or_replace(self._storage[item.asset], item, ["asset", "timestamp"])

    async def add_item_bulk(self, items: list[UpdateCloseValueItem]):
        for it in items:
            await self.add_item(it)

    async def get_items(
        self,
        asset: Asset,
        *,
        start: datetime.datetime | None = None,
        end: datetime.datetime | None = None,
        count: int | None = None,
    ) -> collections.abc.Iterable[UpdateCloseValueItem]:
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
