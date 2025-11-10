import abc
import asyncio
import collections.abc
import contextlib
import datetime
import itertools
import logging
import typing
import uuid

from pocket_option.constants import (
    API_LIMITS_MAX_CONCURRENT_ORDERS,
    API_LIMITS_MAX_DURATION,
    API_LIMITS_MAX_ORDER_AMOUNT,
    API_LIMITS_MIN_DURATION,
    API_LIMITS_MIN_ORDER_AMOUNT,
)
from pocket_option.errors import DealError
from pocket_option.generated_client import PocketOptionClient
from pocket_option.models import Asset, Deal, IsDemo, OpenOrderRequest, OrderAction, SuccessCloseOrder
from pocket_option.utils import append_or_replace, generate_request_id

if typing.TYPE_CHECKING:
    from pocket_option.generated_client import PocketOptionClient

__all__ = ("DealsStorage", "MemoryDealsStorage")

logger = logging.getLogger("pocket_option.deals")


class DealsStorage:
    def __init__(self, client: "PocketOptionClient") -> None:
        self.client = client

        self._open_deal_events: dict[int, asyncio.Event] = {}
        self._close_deal_events: dict[uuid.UUID, asyncio.Event] = {}

        self.client.on.success_open_order(self._on_success_deal)
        self.client.on.success_close_order(self._on_success_close_deal)
        self.client.on.update_opened_deals(self.add_or_update_deal_bulk)
        self.client.on.update_closed_deals(self.add_or_update_deal_bulk)

    async def open_deal(
        self,
        asset: Asset,
        amount: int,
        action: OrderAction,
        time: int,
        is_demo: IsDemo = 1,
        request_id: int | None = None,
        option_type: int = 100,
        *,
        check_limits: bool = True,
    ) -> Deal:
        if check_limits:
            if amount < API_LIMITS_MIN_ORDER_AMOUNT:
                raise DealError(
                    "min_amount",
                    "Min amount reached",
                    extras={
                        "amout": amount,
                        "limit": API_LIMITS_MIN_ORDER_AMOUNT,
                    },
                )
            if amount > API_LIMITS_MAX_ORDER_AMOUNT:
                raise DealError(
                    "max_amount",
                    "Max amount reached",
                    extras={
                        "amout": amount,
                        "limit": API_LIMITS_MAX_ORDER_AMOUNT,
                    },
                )
            if time < API_LIMITS_MIN_DURATION:
                raise DealError(
                    "min_duration",
                    "Min duration reached",
                    extras={
                        "time": time,
                        "limit": API_LIMITS_MIN_DURATION,
                    },
                )
            if time > API_LIMITS_MAX_DURATION:
                raise DealError(
                    "max_duration",
                    "Max duration reached",
                    extras={
                        "time": time,
                        "limit": API_LIMITS_MAX_DURATION,
                    },
                )
            if not self.client.authorization_data:
                logger.warning("Failed to check concurent orders: no authorization data")
            if self.client.authorization_data:
                orders = await self.get_deals(uid=self.client.authorization_data.uid, closed=False)
                if len(list(orders)) > API_LIMITS_MAX_CONCURRENT_ORDERS:
                    raise DealError(
                        "max_orders",
                        "Max concurent orders count reached",
                        extras={
                            "count": len(list(orders)),
                            "limit": API_LIMITS_MAX_CONCURRENT_ORDERS,
                        },
                    )

        request_id = request_id or generate_request_id()
        self._open_deal_events[request_id] = asyncio.Event()
        await self.client.emit.open_order(
            OpenOrderRequest(
                asset=asset,
                amount=amount,
                action=action,
                time=time,
                is_demo=is_demo,
                request_id=request_id,
                option_type=option_type,
            ),
        )

        try:
            await asyncio.wait_for(self._open_deal_events[request_id].wait(), 30)
        except TimeoutError as err:
            raise DealError(
                "timeout",
                "Timeout waiting for deal",
                extras={"request_id": request_id},
            ) from err

        if deal := await self.get_deal(request_id=request_id):
            return deal
        raise DealError(
            "not_found",
            "Failed to find deal",
            extras={"request_id": request_id},
        )

    @typing.overload
    async def check_deal_result(
        self,
        wait_time: int = ...,
        *,
        deal_id: uuid.UUID = ...,
        request_id: None = ...,
        deal: None = ...,
    ) -> Deal: ...
    @typing.overload
    async def check_deal_result(
        self,
        wait_time: int = ...,
        *,
        deal_id: None = ...,
        request_id: int = ...,
        deal: None = ...,
    ) -> Deal: ...
    @typing.overload
    async def check_deal_result(
        self,
        wait_time: int = ...,
        *,
        deal_id: None = ...,
        request_id: None = ...,
        deal: Deal = ...,
    ) -> Deal: ...
    async def check_deal_result(
        self,
        wait_time: int = 600,
        *,
        deal_id: uuid.UUID | None = None,
        request_id: int | None = None,
        deal: Deal | None = None,
    ) -> Deal:
        if not deal and (deal_id or request_id):
            deal = await self.get_deal(deal_id=deal_id, request_id=request_id)  # type: ignore
        if not deal:
            raise RuntimeError("Failed to find deal")
        self._close_deal_events[deal.id] = asyncio.Event()
        try:
            await asyncio.wait_for(self._close_deal_events[deal.id].wait(), wait_time)
        except TimeoutError as err:
            raise TimeoutError(f"Timeout waiting for deal {deal.id}") from err

        if deal := await self.get_deal(deal_id=deal.id):
            return deal
        raise RuntimeError("Failed to find deal")

    async def _on_success_deal(self, deal: Deal):
        await self.add_or_update_deal(deal)
        if deal.request_id and self._open_deal_events.get(deal.request_id):
            self._open_deal_events[deal.request_id].set()
            del self._open_deal_events[deal.request_id]

    async def _on_success_close_deal(self, close_deal: SuccessCloseOrder) -> None:
        await self.add_or_update_deal_bulk(close_deal.deals)
        for deal in close_deal.deals:
            if event := self._close_deal_events.pop(deal.id):
                event.set()

    @abc.abstractmethod
    async def add_or_update_deal(self, deal: Deal) -> None: ...
    @abc.abstractmethod
    async def add_or_update_deal_bulk(self, deals: list[Deal]) -> None: ...

    @typing.overload
    async def get_deal(
        self,
        *,
        deal_id: uuid.UUID = ...,
        request_id: None = ...,
    ) -> Deal | None: ...
    @typing.overload
    async def get_deal(
        self,
        *,
        deal_id: uuid.UUID | None = ...,
        request_id: int = ...,
    ) -> Deal | None: ...
    @abc.abstractmethod
    async def get_deal(
        self,
        *,
        deal_id: uuid.UUID | None = None,
        request_id: int | None = None,
    ) -> Deal | None: ...

    @abc.abstractmethod
    async def get_deals(
        self,
        *,
        asset: Asset | None = None,
        uid: int | None = None,
        open_time__gt: datetime.datetime | None = None,
        open_time__gte: datetime.datetime | None = None,
        open_time__lt: datetime.datetime | None = None,
        open_time__lte: datetime.datetime | None = None,
        close_time__gt: datetime.datetime | None = None,
        close_time__gte: datetime.datetime | None = None,
        close_time__lt: datetime.datetime | None = None,
        close_time__lte: datetime.datetime | None = None,
        open_price__gt: float | None = None,
        open_price__gte: float | None = None,
        open_price__lt: float | None = None,
        open_price__lte: float | None = None,
        close_price__gt: float | None = None,
        close_price__gte: float | None = None,
        close_price__lt: float | None = None,
        close_price__lte: float | None = None,
        count: int | None = None,
        closed: bool | None = None,
    ) -> collections.abc.Iterable[Deal]: ...


class MemoryDealsStorage(DealsStorage):
    def __init__(self, client: "PocketOptionClient") -> None:
        super().__init__(client)
        self._deals: list[Deal] = []

    async def add_or_update_deal(self, deal: Deal) -> None:
        self._deals = append_or_replace(self._deals, deal, eq_by_keys=["id"])

    async def add_or_update_deal_bulk(self, deals: list[Deal]) -> None:
        for deal in deals:
            await self.add_or_update_deal(deal)

    async def get_deal(self, *, deal_id: uuid.UUID | None = None, request_id: int | None = None) -> Deal | None:
        if deal_id:
            with contextlib.suppress(StopIteration):
                return next(deal for deal in self._deals if deal.id == deal_id)

        if request_id:
            with contextlib.suppress(StopIteration):
                return next(deal for deal in self._deals if deal.request_id == request_id)
        return None

    async def get_deals(
        self,
        *,
        asset: Asset | None = None,
        uid: int | None = None,
        open_time__gt: datetime.datetime | None = None,
        open_time__gte: datetime.datetime | None = None,
        open_time__lt: datetime.datetime | None = None,
        open_time__lte: datetime.datetime | None = None,
        close_time__gt: datetime.datetime | None = None,
        close_time__gte: datetime.datetime | None = None,
        close_time__lt: datetime.datetime | None = None,
        close_time__lte: datetime.datetime | None = None,
        open_price__gt: float | None = None,
        open_price__gte: float | None = None,
        open_price__lt: float | None = None,
        open_price__lte: float | None = None,
        close_price__gt: float | None = None,
        close_price__gte: float | None = None,
        close_price__lt: float | None = None,
        close_price__lte: float | None = None,
        count: int | None = None,
        closed: bool | None = None,
    ) -> collections.abc.Iterable[Deal]:
        def _convert_dt(dt: datetime.datetime) -> float:
            return dt.timestamp()

        data = self._deals.copy()

        if asset:
            data = filter(lambda it: it.asset == asset, data)
        if uid:
            data = filter(lambda it: it.uid == uid, data)
        if open_time__gt:
            data = filter(lambda it: _convert_dt(it.open_time) > _convert_dt(open_time__gt), data)
        if open_time__gte:
            data = filter(lambda it: _convert_dt(it.open_time) >= _convert_dt(open_time__gte), data)
        if open_time__lt:
            data = filter(lambda it: _convert_dt(it.open_time) < _convert_dt(open_time__lt), data)
        if open_time__lte:
            data = filter(lambda it: _convert_dt(it.open_time) <= _convert_dt(open_time__lte), data)
        if close_time__gt:
            data = filter(lambda it: _convert_dt(it.close_time) > _convert_dt(close_time__gt), data)
        if close_time__gte:
            data = filter(lambda it: _convert_dt(it.close_time) >= _convert_dt(close_time__gte), data)
        if close_time__lt:
            data = filter(lambda it: _convert_dt(it.close_time) < _convert_dt(close_time__lt), data)
        if close_time__lte:
            data = filter(lambda it: _convert_dt(it.close_time) <= _convert_dt(close_time__lte), data)

        if open_price__gt:
            data = filter(lambda it: it.open_price > open_price__gt, data)
        if open_price__gte:
            data = filter(lambda it: it.open_price >= open_price__gte, data)
        if open_price__lt:
            data = filter(lambda it: it.open_price < open_price__lt, data)
        if open_price__lte:
            data = filter(lambda it: it.open_price <= open_price__lte, data)
        if close_price__gt:
            data = filter(lambda it: it.close_price and it.close_price > close_price__gt, data)
        if close_price__gte:
            data = filter(lambda it: it.close_price and it.close_price >= close_price__gte, data)
        if close_price__lt:
            data = filter(lambda it: it.close_price and it.close_price < close_price__lt, data)
        if close_price__lte:
            data = filter(lambda it: it.close_price and it.close_price <= close_price__lte, data)

        if closed is True:
            data = filter(lambda it: it.close_price is not None, data)
        if closed is False:
            data = filter(lambda it: it.close_price is None, data)

        data = sorted(data, key=lambda it: it.open_time)
        if count:
            data = itertools.islice(data, -count)
        return data
