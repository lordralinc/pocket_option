# ⚡ PocketOption API SDK (Unofficial)

[![PyPI version](https://img.shields.io/pypi/v/pocket-option.svg)](https://pypi.org/project/pocket-option)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pocket-option.svg)](https://pypi.org/project/pocket-option)
[![Downloads](https://pepy.tech/badge/pocket-option)](https://pepy.tech/project/pocket-option)
[![License](https://img.shields.io/github/license/lordralinc/pocket_option.svg)](https://github.com/lordralinc/pocket_option/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/lordralinc/pocket_option.svg?style=social)](https://github.com/lordralinc/pocket_option/stargazers)


🌐 Available languages:
[🇬🇧 English](README.md) | [🇷🇺 Русский](README.ru.md)

Asynchronous **Python SDK for interacting with the PocketOption API** (unofficial).

Fully type-hinted, built on `pydantic`, with middleware and event support.

Supports Python 3.13+ and is fully asynchronous (`asyncio` + `aiohttp`).

> ⚠️ **Disclaimer**

> ⚠️ This project **is not a trading bot**.

> ⚠️ It is **not affiliated with PocketOption** and is intended for integrations and analytical purposes only.

> ⚠️ Investing in financial instruments carries risks. Past performance does not guarantee future returns, and asset values may fluctuate due to market conditions and movements in underlying instruments. Any forecasts or illustrations are for informational purposes only and do not constitute guarantees or investment advice. This project is **not an invitation or recommendation to invest**. Before making investment decisions, consult financial, legal, and tax professionals to determine whether such products suit your goals, risk tolerance, and personal circumstances.

> P.S. Their demo mode is surprisingly fun to play around with 😎

## 🚀 Features

- 🔌 Connects to PocketOption WebSocket API (via `socket.io`)

- 🔐 Session-based authentication

- 💹 Order and trade management (demo / real account)

- 📊 Market stream subscriptions

- 💾 Built-in in-memory storages (`MemoryCandleStorage`, `MemoryDealsStorage`)

- ⚙️ Middleware chain for event and request interception

- 💬 Event model with decorators (`@client.on.*`)

- ✅ Strict type hints

## ⚙️ Usage Example

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

## 📜 License

**MIT License** — do whatever you want, but at your own risk.
