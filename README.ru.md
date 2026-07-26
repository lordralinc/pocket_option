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

from pocket_option import PocketOptionClient
from pocket_option.constants import Regions
from pocket_option.contrib.default_init import default_init
from pocket_option.models import (
    Asset,
    AuthorizationData,
    DealAction,
    UpdateCloseValueItem,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)
rng = random.SystemRandom()
client = PocketOptionClient(logger=True)

ASSET = Asset.AUDCAD_otc
TRADE_AMOUNT = 10
EXPIRATION_TIME = 60
CANDLE_PERIOD = 30
OPTION_TYPE = 100
IS_DEMO = 1

default_init(
    client,
    authorization=AuthorizationData.model_validate(
        {
            "session": os.environ["PO_SESSION"],
            "isDemo": IS_DEMO,
            "uid": int(os.environ["PO_UID"]),
            "platform": 2,
            "isFastHistory": True,
            "isOptimized": True,
        },
    ),
    sub_assets=[ASSET],
    sub_period=CANDLE_PERIOD,
)


@client.on.update_close_value
async def on_update_close_value(
    assets: list[UpdateCloseValueItem],
):
    logger.debug("Assets updated: %s", assets)


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
    deal = await client.deals.open_deal(
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
    result = await client.deals.check_deal_result(
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
    while True:
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
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

```

## 📤 Доступные события для отправки

<!-- START_AVAILABLE_EMIT_EVENTS -->

| Method | Event |  Category  | Description |
|--------|-------|:----------:|-------------|
| `client.emit.ai_strategy_multi_get_state` | `ai-strategy-multi/get-state` | ai | Get AI strategy state. |
| `client.emit.change_asset` | `changeSymbol` | assets | Changes the active trading asset and timeframe. |
| `client.emit.subscribe_for_market_sentiment` | `subfor` | assets | Subscribes to market sentiment updates for an asset. |
| `client.emit.subscribe_to_asset` | `subscribeSymbol` | assets | Subscribes to real-time updates for a trading asset. |
| `client.emit.unsubscribe_for_market_sentiment` | `unsubfor` | assets | Removes market sentiment subscription for an asset. |
| `client.emit.unsubscribe_from_asset` | `unSubscribeSymbol` | assets | Unsubscribes from real-time updates for a trading asset. |
| `client.emit.auth` | `auth` | common | Authorizes the client session. |
| `client.emit.demo_refill_balance` | `td/refill` | common | Refill demo account balance. |
| `client.emit.load_history_period` | `loadHistoryPeriod` | common | Requests historical market data for a specific period. |
| `client.emit.ps` | `ps` | common | Sends a heartbeat request to keep the connection alive. |
| `client.emit.update_balance` | `updateBalance` | common | Request balance update. |
| `client.emit.copy_signal` | `copySignalOrder` | deals | Creates a deal from a copy trading signal. |
| `client.emit.deals_ai` | `deals/ai` | deals | AI deal operation. |
| `client.emit.deals_copy` | `copyorder` | deals | Copy existing order |
| `client.emit.deals_double_up` | `deals/double-up` | deals | Double existing deal. |
| `client.emit.deals_open` | `openOrder` | deals | Creates a new trading deal. |
| `client.emit.deals_pending_cancel` | `cancelPendingOrder` | deals | Cancel pending order. |
| `client.emit.deals_pending_open` | `openPendingOrder` | deals | Create pending order. |
| `client.emit.deals_rollover` | `deals/rollover` | deals | Rollover existing deal. |
| `client.emit.deals_update_opened` | `updateOpenedDeals` | deals | - |
| `client.emit.social_disable_only_watched` | `social/disable-only-watched` | deals | Disable watched filter. |
| `client.emit.social_enable_only_watched` | `social/enable-only-watched` | deals | Enable watched filter. |
| `client.emit.update_closed_expresses` | `updateClosedExpresses` | deals | - |
| `client.emit.indicator_load` | `indicator/load` | indicator | Indicates that indicator data has been loaded by the platform. |
| `client.emit.signals_subscribe` | `signals/subscribe` | signals | - |
| `client.emit.signals_unsubscribe` | `signals/unsubscribe` | signals | - |
| `client.emit.favorite_load` | `favorite/load` | ui | Indicates that favorite has been loaded by the platform. |
| `client.emit.price_alert_load` | `price-alert/load` | ui | Indicates that price alert data has been loaded by the platform. |

<!-- END_AVAILABLE_EMIT_EVENTS -->


## 📥 Доступные события для получения

<!-- START_AVAILABLE_ON_EVENTS -->

| Method | Event |  Category  | Description |
|--------|-------|:----------:|-------------|
| `client.on.ai_strategy_multi_get_state` | `ai-strategy-multi/get-state` | ai | Get AI strategy state. |
| `client.on.change_asset` | `changeSymbol` | assets | Changes the active trading asset and timeframe. |
| `client.on.subscribe_for_market_sentiment` | `subfor` | assets | Subscribes to market sentiment updates for an asset. |
| `client.on.subscribe_to_asset` | `subscribeSymbol` | assets | Subscribes to real-time updates for a trading asset. |
| `client.on.unsubscribe_for_market_sentiment` | `unsubfor` | assets | Removes market sentiment subscription for an asset. |
| `client.on.unsubscribe_from_asset` | `unSubscribeSymbol` | assets | Unsubscribes from real-time updates for a trading asset. |
| `client.on.auth` | `auth` | common | Authorizes the client session. |
| `client.on.demo_refill_balance` | `td/refill` | common | Refill demo account balance. |
| `client.on.load_history_period` | `loadHistoryPeriod` | common | Requests historical market data for a specific period. |
| `client.on.ps` | `ps` | common | Sends a heartbeat request to keep the connection alive. |
| `client.on.update_balance` | `updateBalance` | common | Request balance update. |
| `client.on.copy_signal` | `copySignalOrder` | deals | Creates a deal from a copy trading signal. |
| `client.on.deals_ai` | `deals/ai` | deals | AI deal operation. |
| `client.on.deals_copy` | `copyorder` | deals | Copy existing order |
| `client.on.deals_double_up` | `deals/double-up` | deals | Double existing deal. |
| `client.on.deals_open` | `openOrder` | deals | Creates a new trading deal. |
| `client.on.deals_pending_cancel` | `cancelPendingOrder` | deals | Cancel pending order. |
| `client.on.deals_pending_open` | `openPendingOrder` | deals | Create pending order. |
| `client.on.deals_rollover` | `deals/rollover` | deals | Rollover existing deal. |
| `client.on.deals_update_opened` | `updateOpenedDeals` | deals | - |
| `client.on.social_disable_only_watched` | `social/disable-only-watched` | deals | Disable watched filter. |
| `client.on.social_enable_only_watched` | `social/enable-only-watched` | deals | Enable watched filter. |
| `client.on.update_closed_expresses` | `updateClosedExpresses` | deals | - |
| `client.on.indicator_load` | `indicator/load` | indicator | Indicates that indicator data has been loaded by the platform. |
| `client.on.signals_subscribe` | `signals/subscribe` | signals | - |
| `client.on.signals_unsubscribe` | `signals/unsubscribe` | signals | - |
| `client.on.favorite_load` | `favorite/load` | ui | Indicates that favorite has been loaded by the platform. |
| `client.on.price_alert_load` | `price-alert/load` | ui | Indicates that price alert data has been loaded by the platform. |

<!-- END_AVAILABLE_ON_EVENTS -->

## 📜 Лицензия

**MIT License** — делай что хочешь, но на свой страх и риск.
