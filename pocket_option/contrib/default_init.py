import asyncio
import contextlib
import functools

from pocket_option.contrib.assets import AssetsStorage, MemoryAssetsStorage
from pocket_option.contrib.candles import CandleStorage, MemoryCandleStorage
from pocket_option.contrib.deals import DealsStorage, MemoryDealsStorage
from pocket_option.generated_client import PocketOptionClient
from pocket_option.models import Asset, AuthorizationData, ChangeAssetRequest, SuccessAuthEvent

__all__ = ("default_init",)


async def on_connect(
    *,
    client: PocketOptionClient,
    stop_event: asyncio.Event,
    authorization: AuthorizationData,
) -> None:
    await client.emit.auth(authorization)
    stop_event.clear()
    asyncio.create_task(ping_loop(client, stop_event))  # noqa: RUF006


async def on_disconnect(
    *,
    stop_event: asyncio.Event,
) -> None:
    stop_event.set()


async def on_success_auth(
    _: SuccessAuthEvent,
    *,
    client: PocketOptionClient,
    sub_assets: list[Asset] | None = None,
    sub_period: int = 30,
) -> None:
    sub_assets = sub_assets or []

    await client.emit.indicator_load()
    await client.emit.favorite_load()
    await client.emit.price_alert_load()
    for asset in sub_assets:
        await client.emit.subscribe_to_asset(asset)
        await client.emit.change_asset(
            ChangeAssetRequest(
                asset=asset,
                period=sub_period,
            ),
        )
        await client.emit.subscribe_for_market_sentiment(asset)


async def ping_loop(client: PocketOptionClient, stop_event: asyncio.Event) -> None:
    with contextlib.suppress(asyncio.CancelledError):
        while not stop_event.is_set():
            await client.emit.ps()
            await asyncio.sleep(60)


def default_init(
    client: PocketOptionClient,
    *,
    authorization: AuthorizationData,
    sub_assets: list[Asset] | None = None,
    sub_period: int = 30,
    candle_storage_cls: type[CandleStorage] = MemoryCandleStorage,
    deals_storage_cls: type[DealsStorage] = MemoryDealsStorage,
    assets_storage_cls: type[AssetsStorage] = MemoryAssetsStorage,
):
    candle_storage_cls(client)
    deals_storage_cls(client)
    assets_storage_cls(client)

    stop_event = asyncio.Event()

    client.on.connect(
        functools.partial(
            on_connect,
            client=client,
            stop_event=stop_event,
            authorization=authorization,
        ),
    )
    client.on.success_auth(
        functools.partial(
            on_success_auth,
            client=client,
            sub_assets=sub_assets,
            sub_period=sub_period,
        ),
    )
    client.on.disconnect(
        functools.partial(
            on_disconnect,
            stop_event=stop_event,
        ),
    )
