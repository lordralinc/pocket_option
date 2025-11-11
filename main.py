import asyncio
import logging
import os

import aiohttp
from rich.logging import RichHandler

from pocket_option import PocketOptionClient, models
from pocket_option.constants import Regions
from pocket_option.contrib.candles import MemoryCandleStorage
from pocket_option.contrib.deals import MemoryDealsStorage
from pocket_option.models import Asset, Deal, OrderAction, UpdateStreamItem

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

    @client.on.connect
    async def on_connect(data: None):
        await client.emit.auth(
            models.AuthorizationData.model_validate(
                dict(
                    session=os.environ["PO_SESSION"],
                    isDemo=1,
                    uid=int(os.environ["PO_UID"]),
                    platform=2,
                    isFastHistory=True,
                    isOptimized=True,
                ),
            ),
        )

    @client.on.success_auth
    async def on_success_auth(data: models.SuccessAuthData):
        await client.emit.favorite_load()
        await client.emit.indicator_load()
        await client.emit.price_alert_load()
        await client.emit.subscribe_for(Asset.EURUSD_otc)
        await client.emit.change_symbol(models.ChangeSymbolRequest(asset=Asset.EURUSD_otc, period=30))
        await client.emit.subscribe_symbol(Asset.EURUSD_otc)

    @client.on.update_assets
    async def on_update_Assets(data: list[models.UpdateAssetItem]):
        print(data)

    MemoryCandleStorage(client)
    MemoryDealsStorage(client)

    await client.connect(Regions.DEMO)
    asyncio.create_task(ping(client))

    await client.wait()


if __name__ == "__main__":
    asyncio.run(main())
