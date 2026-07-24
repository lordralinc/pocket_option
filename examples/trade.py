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
