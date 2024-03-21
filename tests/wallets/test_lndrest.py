import pytest
from pytest_httpserver import HTTPServer

from lnbits.wallets.corelightningrest import settings
from lnbits.wallets.lndrest import LndRestWallet

ENDPOINT = "http://127.0.0.1:8555"
MACAROON = "eNcRyPtEdMaCaRoOn"

headers = {
    "Grpc-Metadata-macaroon": MACAROON,
    "User-Agent": settings.user_agent,
}


bolt11_sample = str(
    "lnbc210n1pjlgal5sp5xr3uwlfm7ltum"
    + "djyukhys0z2rw6grgm8me9k4w9vn05zt"
    + "9svzzjspp5ud2jdfpaqn5c2k2vphatsj"
    + "ypfafyk8rcvkvwexnrhmwm94ex4jtqdq"
    + "u24hxjapq23jhxapqf9h8vmmfvdjscqp"
    + "jrzjqta942048v7qxh5x7pxwplhmtwfl"
    + "0f25cq23jh87rhx7lgrwwvv86r90guqq"
    + "nwgqqqqqqqqqqqqqqpsqyg9qxpqysgqy"
    + "lngsyg960lltngzy90e8n22v4j2hvjs4"
    + "l4ttuy79qqefjv8q87q9ft7uhwdjakvn"
    + "sgk44qyhalv6ust54x98whl3q635hkwgsyw8xgqjl7jwu",
)


# specify where the server should bind to
@pytest.fixture(scope="session")
def httpserver_listen_address():
    return ("127.0.0.1", 8555)


@pytest.mark.asyncio
async def test_status_no_balance(httpserver: HTTPServer):
    settings.lnd_rest_endpoint = ENDPOINT
    settings.lnd_rest_macaroon = MACAROON
    settings.lnd_rest_cert = ""

    server_response = {}
    httpserver.expect_request(
        uri="/v1/balance/channels", headers=headers, method="GET"
    ).respond_with_json(server_response)

    wallet = LndRestWallet()

    status = await wallet.status()
    assert status.balance_msat == 0
    assert status.error_message == "{}"

    httpserver.check_assertions()


@pytest.mark.asyncio
async def test_status_ok(httpserver: HTTPServer):
    settings.lnd_rest_endpoint = ENDPOINT
    settings.lnd_rest_macaroon = MACAROON
    settings.lnd_rest_cert = ""

    server_response = {"balance": 21}
    httpserver.expect_request(
        uri="/v1/balance/channels", headers=headers, method="GET"
    ).respond_with_json(server_response)

    wallet = LndRestWallet()

    status = await wallet.status()
    assert status.balance_msat == 21_000
    assert status.error_message is None

    httpserver.check_assertions()
