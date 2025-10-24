import asyncio
import functools
import logging
import os
import time

import aiohttp
from rich.logging import RichHandler

from pocket_option import PocketOptionClient
from pocket_option.constants import Regions
from pocket_option.contrib.candles import MemoryCandleStorage
from pocket_option.contrib.deals import MemoryDealsStorage
from pocket_option.models import (
    Asset,
    AuthorizationData,
    ChangeSymbolRequest,
    Deal,
    OpenOrderRequest,
    OrderAction,
    UpdateStreamItem,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
logging.getLogger("aiohttp").setLevel(logging.DEBUG)

logger = logging.getLogger()


async def ping(client: PocketOptionClient):
    while True:
        await client.sio.emit("ps")
        await asyncio.sleep(60)


async def main():
    session = aiohttp.ClientSession(
        proxy="http://127.0.0.1:12334",
        headers={
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Origin": "https://m.pocketoption.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
        },
    )

    client = PocketOptionClient(http_session=session)

    # === Обработчики ===
    @client.sio.event
    async def connect():
        logger.info("✅ Connected to server")

    @client.sio.event
    async def connect_error(data):
        logger.warning("🔥 connect_error received: %r", data)

    @client.sio.event
    async def disconnect():
        logger.info("❌ Disconnected from server")

    @client.on.update_stream
    async def on_update_stream(deals: list[UpdateStreamItem]): ...

    @client.on.update_closed_deals
    async def on_update_closed_deals(deals: list[Deal]): ...

    @client.on.success_open_order
    async def on_success_open_order(deals: Deal): ...

    storage = MemoryCandleStorage(client)
    deals = MemoryDealsStorage(client)

    await client.connect(Regions.DEMO)
    await client.emit.auth(
        AuthorizationData.model_validate(
            {
                "session": os.environ["PO_SESSION"],
                "isDemo": 1,
                "uid": int(os.environ["PO_UID"]),
                "platform": 2,
                "isFastHistory": True,
                "isOptimized": True,
            },
        ),
    )
    asyncio.create_task(ping(client))
    await asyncio.sleep(5)
    await client.emit.indicator_load()
    await client.emit.favorite_load()
    await client.emit.price_alert_load()

    await asyncio.sleep(2)

    await client.emit.subscribe_symbol(Asset.AUDCAD_otc)
    await client.emit.change_symbol(ChangeSymbolRequest(asset=Asset.AUDCAD_otc, period=30))
    await client.emit.subscribe_for(Asset.AUDCAD_otc)

    await asyncio.sleep(2)
    deal = await deals.open_deal(
        asset=Asset.AUDCAD_otc,
        amount=10,
        action=OrderAction.CALL,
        is_demo=1,
        option_type=100,
        time=60,
    )
    logger.debug("Deal %r", deal)
    result = await deals.check_deal_result(wait_time=60, deal=deal)
    logger.debug("result %r", result)
    await client.wait()


if __name__ == "__main__":
    asyncio.run(main())
