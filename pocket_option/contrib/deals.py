from __future__ import annotations

import abc
import asyncio
import contextlib
import itertools
import logging
import typing

from pocket_option.constants import (
    API_LIMITS_MAX_CONCURRENT_ORDERS,
    API_LIMITS_MAX_DURATION,
    API_LIMITS_MAX_ORDER_AMOUNT,
    API_LIMITS_MIN_DURATION,
    API_LIMITS_MIN_ORDER_AMOUNT,
)
from pocket_option.errors import DealError
from pocket_option.generated_client import PocketOptionClient
from pocket_option.models import Asset, Deal, DealAction, IsDemo, OpenDealRequest, SuccessCloseDealEvent
from pocket_option.utils import Q, append_or_replace, generate_request_id

if typing.TYPE_CHECKING:
    import collections.abc
    import uuid

    from pocket_option.generated_client import PocketOptionClient

__all__ = ("DealsStorage", "MemoryDealsStorage")

logger = logging.getLogger("pocket_option.deals")


class DealsStorage:
    """
    Abstract storage and manager for trading deals.

    DealsStorage provides a high-level interface for:

    - opening new deals;
    - waiting for deal execution confirmation;
    - waiting for deal closing;
    - storing and querying deal history.

    The storage subscribes to PocketOption events:

        success_open_deal
            -> saves newly opened deals

        success_close_deal
            -> updates closed deals

        update_opened_deals
            -> synchronizes active deals

        update_closed_deals
            -> synchronizes completed deals

    Concrete storage implementations must provide persistence logic.

    Examples:
        storage = MemoryDealsStorage(client)

        deal = await storage.open_deal(
            asset=Asset.AUDCAD_otc,
            amount=10,
            action=DealAction.CALL,
            time=60,
        )

        result = await storage.check_deal_result(
            deal=deal,
        )
    """

    def __init__(self, client: PocketOptionClient) -> None:
        self.client = client

        self._open_deal_events: dict[int, asyncio.Event] = {}
        self._close_deal_events: dict[uuid.UUID, asyncio.Event] = {}

        self.client.on.success_open_deal(self._on_success_open_deal)
        self.client.on.success_close_deal(self._on_success_close_deal)
        self.client.on.update_opened_deals(self.add_or_update_deal_bulk)
        self.client.on.update_closed_deals(self.add_or_update_deal_bulk)

        self.client.deals = self

    async def open_deal(
        self,
        asset: Asset,
        amount: int,
        action: DealAction,
        time: int,
        is_demo: IsDemo = 1,
        request_id: int | None = None,
        option_type: int = 100,
        *,
        check_limits: bool = True,
    ) -> Deal:
        """
        Open a new trading deal.

        Sends an order request to PocketOption and waits until the server
        confirms deal creation.

        Validation is performed before sending:

        - order amount limits;
        - expiration duration limits;
        - concurrent opened deals limit.

        :param asset: Trading asset
        :type asset: Asset

        :param amount: Deal amount
        :type amount: int

        :param action: Deal direction
        :type action: DealAction

        :param time: Deal duration in seconds
        :type time: int

        :param is_demo: Use demo account
        :type is_demo: IsDemo

        :param request_id: Custom request id
        :type request_id: int | None

        :param option_type: Option type
        :type option_type: int

        :param check_limits: Check API limits before opening
        :type check_limits: bool

        :raises DealError: If deal cannot be opened

        :return: Opened deal
        :rtype: Deal
        """
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
                self.client.logger.warning("Failed to check concurent orders: no authorization data")
            if self.client.authorization_data:
                orders = await self.get_deals(
                    query=Q.field("uid", "eq", self.client.authorization_data.uid) & Q.field("closed", "eq", False),
                )
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
        await self.client.emit.open_deal(
            OpenDealRequest(
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
        """
        Wait for deal closing.

        :param wait_time: Maximum wait time in seconds
        :type wait_time: int

        :param deal_id: Deal identifier
        :type deal_id: uuid.UUID | None

        :param request_id: Deal request identifier
        :type request_id: int | None

        :param deal: Existing deal object
        :type deal: Deal | None

        :raises TimeoutError: If waiting timeout exceeded

        :return: Closed deal
        :rtype: Deal
        """
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

    async def _on_success_open_deal(self, deal: Deal):
        await self.add_or_update_deal(deal)
        if deal.request_id and self._open_deal_events.get(deal.request_id):
            self._open_deal_events[deal.request_id].set()
            del self._open_deal_events[deal.request_id]

    async def _on_success_close_deal(self, close_deal: SuccessCloseDealEvent) -> None:
        await self.add_or_update_deal_bulk(close_deal.deals)
        for deal in close_deal.deals:
            if event := self._close_deal_events.pop(deal.id, None):
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
    ) -> Deal | None:
        """
        Get deal by identifier.

        :param deal_id: Deal UUID
        :type deal_id: uuid.UUID | None

        :param request_id: Open request identifier
        :type request_id: int | None

        :return: Deal or None
        :rtype: Deal | None
        """

    @abc.abstractmethod
    async def get_deals(
        self,
        *,
        query: typing.Any,
        count: int | None = None,
    ) -> collections.abc.Iterable[Deal]: ...


class MemoryDealsStorage(DealsStorage):
    """
    In-memory deals storage.

    Stores deals in process memory.
    """

    def __init__(self, client: PocketOptionClient) -> None:
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
        query: Q | None = None,
        count: int | None = None,
    ) -> collections.abc.Iterable[Deal]:
        """
        Query stored deals using Q expressions.

        Filtering is delegated to Q objects, allowing composition
        of complex queries.

        Example:

            query = (
                Q.field("asset", "eq", Asset.AUDCAD_otc)
                &
                Q.field("closed", "eq", False)
            )

            deals = await storage.get_deals(
                query=query
            )

        :param query: Deal filter expression
        :type query: Q

        :param count: Maximum number of returned deals
        :type count: int | None

        :return: Iterable of deals
        :rtype: collections.abc.Iterable[Deal]
        """
        data = self._deals.copy()

        if query:
            data = [deal for deal in data if query(deal)]

        data = sorted(data, key=lambda it: it.open_time)
        if count:
            data = itertools.islice(data, -count)
        return data
