import asyncio
import functools
import logging
import os

import aiohttp
from rich.logging import RichHandler

from pocket_option import PocketOptionClient

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)
logging.getLogger("aiohttp").setLevel(logging.DEBUG)
logging.getLogger("engineio").setLevel(logging.DEBUG)
logging.getLogger("socketio").setLevel(logging.DEBUG)

logger = logging.getLogger()


# ---------- Trace handlers for HTTP requests ----------
async def on_request_start(session, trace_config_ctx, params):
    logger.debug("➡ HTTP START %s %s", params.method, params.url)
    if params.headers:
        for k, v in params.headers.items():
            logging.debug("   > %s: %s", k, v)


async def on_request_end(session, trace_config_ctx, params):
    logger.debug(
        "⬅ HTTP END  %s %s -> status=%s",
        params.method,
        params.url,
        getattr(params, "response", None).status if getattr(params, "response", None) else "N/A",
    )


trace = aiohttp.TraceConfig()
trace.on_request_start.append(on_request_start)
trace.on_request_end.append(on_request_end)
_orig_ws_connect = aiohttp.ClientSession.ws_connect


@functools.wraps(_orig_ws_connect)
async def _ws_connect_and_log(self, url, **kwargs):
    logging.debug("=== ws_connect called ===")
    logging.debug("WS URL: %s", url)
    # headers can be in kwargs or in session.headers
    headers = kwargs.get("headers") or getattr(self, "headers", None)
    if headers:
        logging.debug("WS Headers (from kwargs/session):")
        for k, v in headers.items():
            logging.debug("   %s: %s", k, v)
    # log proxy param if present
    if "proxy" in kwargs:
        logging.debug("WS proxy: %s", kwargs["proxy"])
    # call original
    return await _orig_ws_connect(self, url, **kwargs)


# apply monkeypatch
aiohttp.ClientSession.ws_connect = _ws_connect_and_log


async def ping(client: PocketOptionClient):
    while True:
        await client.sio.emit("ps")
        await asyncio.sleep(60)


async def main():
    session = aiohttp.ClientSession(
        proxy="http://127.0.0.1:12334",
        trace_configs=[trace],
        headers={
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Origin": "https://m.pocketoption.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
        },
    )

    client = PocketOptionClient(http_session=session, logger=True)

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

    @client.on("*")
    async def message(*args, **kwargs):
        logger.info(f"new message {args!r} {kwargs!r}")

    await client.connect(
        "wss://demo-api-eu.po.market",
    )
    await client.emit(
        "auth",
        {
            "session": os.environ["PO_SESSION"],
            "isDemo": 1,
            "uid": int(os.environ["PO_UID"]),
            "platform": 2,
            "isFastHistory": True,
            "isOptimized": True,
        },
    )
    asyncio.create_task(ping(client))
    await asyncio.sleep(5)
    await client.emit("indicator/load")
    await client.emit("favorite/load")
    await client.emit("price-alert/load")

    await asyncio.sleep(2)

    await client.emit("subscribeSymbol", "AUDCAD_otc")
    await client.emit("changeSymbol", {"asset": "AUDCAD_otc", "period": 30})
    await client.emit("subfor", "AUDCAD_otc")
    await client.wait()


if __name__ == "__main__":
    asyncio.run(main())
