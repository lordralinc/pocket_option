import asyncio
import datetime
import logging
import os
import random
import uuid

import tortoise
from tortoise import fields, models

from pocket_option import PocketOptionClient
from pocket_option.constants import Regions
from pocket_option.contrib.default_init import default_init
from pocket_option.models import (
    Asset,
    AuthorizationData,
    LoadHistoryPeriodFastResponse,
    LoadHistoryPeriodRequest,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)
rng = random.SystemRandom()
client = PocketOptionClient(logger=True, filter_events_log=["updateStream"])

ASSET = Asset.EURUSD_otc
CANDLE_PERIOD = 30
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


class DBOHLV(models.Model):
    id = fields.UUIDField(pk=True)
    asset = fields.CharEnumField(Asset)
    time = fields.DatetimeField()
    open = fields.FloatField()
    close = fields.FloatField()
    high = fields.FloatField()
    low = fields.FloatField()
    volume = fields.IntField()

    class Meta(models.Model.Meta):
        table = "candles"
        unique_together = ("asset", "time")


@client.on.load_history_period_fast()
async def load_history(data: LoadHistoryPeriodFastResponse):
    logger.info(
        "Received history: asset=%s candles=%d",
        data.asset,
        len(data.data),
    )

    items = [
        DBOHLV(
            id=uuid.uuid4(),
            asset=data.asset,
            time=datetime.datetime.fromtimestamp(it.time, tz=datetime.UTC),
            open=it.open,
            close=it.close,
            high=it.high,
            low=it.low,
            volume=it.volume,
        )
        for it in data.data
    ]

    await DBOHLV.bulk_create(
        items,
        update_fields=("open", "close", "high", "low", "volume"),
        on_conflict=("asset", "time"),
    )

    logger.info(
        "Saved candles: asset=%s count=%d range=%s..%s",
        data.asset,
        len(items),
        items[0].time if items else None,
        items[-1].time if items else None,
    )


def time_range(
    start: datetime.datetime,
    end: datetime.datetime,
    step: datetime.timedelta,
):
    if not step:
        raise ValueError("Step cannot be zero")

    current = start

    while (step.total_seconds() > 0 and current < end) or (step.total_seconds() < 0 and current > end):
        current += step
        yield current


async def main():
    await tortoise.Tortoise.init(db_url="sqlite://db.sqlite3", modules={"models": ["__main__"]})
    await tortoise.Tortoise.generate_schemas()
    try:
        await client.connect(Regions.DEMO)
        await client.authorized_event.wait()
        for time in time_range(
            datetime.datetime.now(),
            datetime.datetime.now() - datetime.timedelta(hours=12),
            step=datetime.timedelta(seconds=-CANDLE_PERIOD * 150),
        ):
            logger.info(
                "Request candles: asset=%s time=%s",
                ASSET,
                time,
            )
            await client.emit.load_history_period(
                LoadHistoryPeriodRequest(
                    asset=ASSET,
                    index=None,
                    time=time.timestamp(),
                    offset=1000,
                    period=CANDLE_PERIOD,
                ),
            )
            await asyncio.sleep(5)

    except KeyboardInterrupt:
        logger.info("Stopping...")
    finally:
        await client.disconnect()
        await tortoise.Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(main())
