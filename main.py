import asyncio
import json
import logging
import os
import pathlib

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

    @client.add_on("updateAssets")
    async def on_update_Assets(data):
        names = [
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
        items = [dict(zip(names, it, strict=True)) for it in data]
        print(items)
        pathlib.Path("updateAssets.json").write_text(json.dumps(items))

    MemoryCandleStorage(client)
    MemoryDealsStorage(client)

    await client.connect(Regions.DEMO)
    asyncio.create_task(ping(client))

    await client.wait()


if __name__ == "__main__":
    asyncio.run(main())
