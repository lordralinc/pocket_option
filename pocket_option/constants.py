import enum

__all__ = (
    "API_LIMITS_MAX_CONCURRENT_ORDERS",
    "API_LIMITS_MAX_DURATION",
    "API_LIMITS_MAX_ORDER_AMOUNT",
    "API_LIMITS_MIN_DURATION",
    "API_LIMITS_MIN_ORDER_AMOUNT",
    "API_LIMITS_RATE_LIMIT",
    "DEFAULT_ORIGIN",
    "DEFAULT_USER_AGENT",
    "MAX_INT_32",
    "TIMESTAMP_OFFSET",
    "Regions",
)


API_LIMITS_MIN_ORDER_AMOUNT = 1
API_LIMITS_MAX_ORDER_AMOUNT = 50_000
API_LIMITS_MIN_DURATION = 5
API_LIMITS_MAX_DURATION = 43_200
API_LIMITS_MAX_CONCURRENT_ORDERS = 10
API_LIMITS_RATE_LIMIT = 100
MAX_INT_32 = 2_147_483_647
TIMESTAMP_OFFSET = -7200
DEFAULT_ORIGIN = "https://m.pocketoption.com"
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0"


class Regions(enum.StrEnum):
    UNITED_STATES_NORTH = "wss://api-us-north.po.market"
    UNITED_STATES_SOUTH = "wss://api-us-south.po.market"
    EUROPA = "wss://api-eu.po.market"
    ASIA = "wss://api-asia.po.market"

    UNITED_STATES_2 = "wss://api-us2.po.market"
    UNITED_STATES_3 = "wss://api-us3.po.market"
    UNITED_STATES_4 = "wss://api-us4.po.market"

    FRANCE_1 = "wss://api-fr.po.market"
    FRANCE_2 = "wss://api-fr2.po.market"
    RUSSIA = "wss://api-msk.po.market"
    INDIA = "wss://api-in.po.market"
    FINLAND = "wss://api-fin.po.market"

    SEYCHELLES = "wss://api-sc.po.market"
    HONGKONG = "wss://api-hk.po.market"

    SERVER_1 = "wss://api-spb.po.market"
    SERVER_2 = "wss://api-l.po.market"
    SERVER_3 = "wss://api-c.po.market"

    DEMO = "wss://demo-api-eu.po.market"
    DEMO_2 = "wss://try-demo-eu.po.market"
