# ⚡ PocketOption API SDK (Unofficial)

[![PyPI version](https://img.shields.io/pypi/v/pocket-option.svg)](https://pypi.org/project/pocket-option)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pocket-option.svg)](https://pypi.org/project/pocket-option)
[![Downloads](https://pepy.tech/badge/pocket-option)](https://pepy.tech/project/pocket-option)
[![License](https://img.shields.io/github/license/lordralinc/pocket_option.svg)](https://github.com/lordralinc/pocket_option/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/lordralinc/pocket_option.svg?style=social)](https://github.com/lordralinc/pocket_option/stargazers)

🌐 Available languages:
[🇬🇧 English](README.md) | [🇷🇺 Русский](README.ru.md)

Асинхронный **Python-SDK для взаимодействия с PocketOption API** (неофициальный).

Полностью типизирован, построен на `pydantic`, с поддержкой middleware, событий.

Поддерживает Python 3.13+ и полностью асинхронен (`asyncio` + `aiohttp`).

> ⚠️ **Предупреждение**

> ⚠️ Этот проект **не является торговым ботом**.

> ⚠️ Проект не связан с PocketOption. Предназначен для интеграций и анализа.

> ⚠️ Инвестирование в финансовые продукты сопряжено с рисками. Прошлые результаты не гарантируют будущую доходность, а стоимость активов может изменяться в зависимости от рыночных условий и колебаний базовых инструментов. Любые прогнозы или иллюстрации приведены исключительно для справки и не являются гарантией результата. Этот проект не является приглашением или рекомендацией к инвестированию. Перед инвестированием проконсультируйтесь с финансовыми, юридическими и налоговыми специалистами и решите, подходит ли данный продукт вашим целям, допустимому уровню риска и текущей ситуации.

> P.S. У них демо прикольное, чисто позалипать кайф

## 🚀 Возможности

- 🔌 Подключение к WebSocket-API PocketOption (через `socket io`)

- 🔐 Авторизация по активной сессии

- 💹 Управление ордерами и сделками (демо / реальный счёт)

- 📊 Подписка на рыночные потоки

- 💾 Встроенные in-memory-хранилища (`MemoryCandleStorage`, `MemoryDealsStorage`)

- ⚙️ Middleware-цепочка для перехвата событий и запросов

- 💬 Событийная модель с декораторами (`@client.on.*`)

- ✅ Строгая типизация

## 🔑 Получение Session ID и UID

Для работы с API необходимо получить корректные данные сессии из браузера.

1. Откройте Pocket Option в браузере
2. Откройте инструменты разработчика (F12)
3. Перейдите во вкладку **Network**
4. Отфильтруйте по **WebSocket (WS)**
5. Найдите запрос к `{region}`
6. Найдите сообщение, содержащее `42["auth"`
7. Скопируйте значения `session` и `uid`

**Пример**:

```json
42["auth",{"session":"abcd1234efgh5678","isDemo":1,"uid":1234589,"platform":1}]
```

## ⚙️ Пример использования

```python
import asyncio
import logging
import os
import random
from contextlib import suppress

from pocket_option import PocketOptionClient
from pocket_option.constants import Regions
from pocket_option.contrib.candles import MemoryCandleStorage
from pocket_option.contrib.deals import MemoryDealsStorage
from pocket_option.models import (
    Asset,
    AuthorizationData,
    ChangeAssetRequest,
    DealAction,
    SuccessAuthEvent,
    UpdateCloseValueItem,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


ASSET = Asset.AUDCAD_otc
TRADE_AMOUNT = 10
EXPIRATION_TIME = 60
CANDLE_PERIOD = 30
OPTION_TYPE = 100
IS_DEMO = 1


client = PocketOptionClient(logger=True)

candles = MemoryCandleStorage(client)
deals = MemoryDealsStorage(client)

stop_event = asyncio.Event()

ping_task_handle: asyncio.Task | None = None

rng = random.SystemRandom()


async def ping_loop() -> None:
    try:
        while not stop_event.is_set():
            await client.emit.ps()
            await asyncio.sleep(60)

    except asyncio.CancelledError:
        logger.info("Ping task stopped")


async def start_ping() -> None:
    global ping_task_handle  # noqa: PLW0603

    if ping_task_handle and not ping_task_handle.done():
        return

    ping_task_handle = asyncio.create_task(ping_loop())


@client.on.connect
async def on_connect():
    logger.info("Connected")
    stop_event.clear()
    await start_ping()
    await client.emit.auth(
        AuthorizationData.model_validate(
            {
                "session": os.environ["PO_SESSION"],
                "isDemo": IS_DEMO,
                "uid": int(os.environ["PO_UID"]),
                "platform": 2,
                "isFastHistory": True,
                "isOptimized": True,
            },
        ),
    )


@client.on.success_auth
async def on_success_auth(data: SuccessAuthEvent):
    logger.info("Authorized: %s", data.id)

    await client.emit.indicator_load()
    await client.emit.favorite_load()
    await client.emit.price_alert_load()
    await client.emit.subscribe_to_asset(ASSET)
    await client.emit.change_asset(
        ChangeAssetRequest(
            asset=ASSET,
            period=CANDLE_PERIOD,
        ),
    )

    await client.emit.subscribe_for_market_sentiment(ASSET)
    logger.info("Trading ready")


@client.on.update_close_value
async def on_update_close_value(
    assets: list[UpdateCloseValueItem],
):
    logger.debug("Assets updated: %s", assets)


@client.on.disconnect
async def on_disconnect():
    logger.warning("Disconnected")
    stop_event.set()


def get_signal() -> DealAction | None:
    return rng.choice(
        [
            DealAction.CALL,
            DealAction.PUT,
            None,
        ],
    )


async def execute_trade(direction: DealAction):
    logger.info(
        "Opening %s trade",
        direction.name,
    )
    deal = await deals.open_deal(
        asset=ASSET,
        amount=TRADE_AMOUNT,
        action=direction,
        is_demo=IS_DEMO,
        option_type=OPTION_TYPE,
        time=EXPIRATION_TIME,
    )
    logger.info(
        "Deal opened: %s",
        deal,
    )
    result = await deals.check_deal_result(
        wait_time=EXPIRATION_TIME + 5,
        deal=deal,
    )
    logger.info(
        "Deal result: %s",
        result,
    )


async def trader_loop():
    await client.authorized_event.wait()
    logger.info("Trader started")
    while not stop_event.is_set():
        try:
            signal = get_signal()
            if signal is None:
                await asyncio.sleep(5)
                continue

            await execute_trade(signal)
            await asyncio.sleep(5)
        except Exception:
            logger.exception("Trading error")
            await asyncio.sleep(10)


async def main():
    try:
        await client.connect(Regions.DEMO)
        await trader_loop()
    except KeyboardInterrupt:
        logger.info("Stopping...")

    finally:
        stop_event.set()
        if ping_task_handle:
            ping_task_handle.cancel()
            with suppress(asyncio.CancelledError):
                await ping_task_handle


if __name__ == "__main__":
    asyncio.run(main())
```

## 📜 Лицензия

**MIT License** — делай что хочешь, но на свой страх и риск.
