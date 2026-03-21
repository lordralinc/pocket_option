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
import os
import random

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

rnd = random.SystemRandom()

client = PocketOptionClient()

storage = MemoryCandleStorage(client)
deals = MemoryDealsStorage(client)


@client.on.connect
async def on_connect(data: None):
    print("Success connected")
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


@client.on.success_auth
async def on_success_auth(data: SuccessAuthEvent):
    print("Success authorized with id %s", data.id)
    await client.emit.indicator_load()
    await client.emit.favorite_load()
    await client.emit.price_alert_load()
    await client.emit.subscribe_to_asset(Asset.AUDCAD_otc)
    await client.emit.change_asset(ChangeAssetRequest(asset=Asset.AUDCAD_otc, period=30))
    await client.emit.subscribe_for_market_sentiment(Asset.AUDCAD_otc)


@client.on.update_close_value
async def on_update_close_value(assets: list[UpdateCloseValueItem]):
    print("Assets updated: ", assets)


def get_signal(storage: MemoryCandleStorage) -> DealAction | None:
    # magic
    return rnd.choice([DealAction.CALL, DealAction.PUT, None])


async def main():
    await client.connect(Regions.DEMO)

    while True:
        direction = get_signal(storage)

        if direction is None:
            await asyncio.sleep(5)
            continue

        deal = await deals.open_deal(
            asset=Asset.AUDCAD_otc,
            amount=10,
            action=direction,
            is_demo=1,
            option_type=100,
            time=60,
        )
        print("✅ Opened deal:", deal)
        result = await deals.check_deal_result(wait_time=60, deal=deal)
        print("✅ Deal result:", result)
        await asyncio.sleep(65)


asyncio.run(main())
```

## 📜 Лицензия

**MIT License** — делай что хочешь, но на свой страх и риск.
