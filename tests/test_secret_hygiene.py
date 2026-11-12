"""C13 / W8: printing or dumping a client never shows the API key, and transport errors never echo a query string."""

import pprint
from typing import Any

import httpx
import pytest

from blindpay import BlindPay, BlindPaySync, WebhookVerificationError, webhooks
from tests.http_mock import Recorder, async_client, sync_client

KEY = "sk_live_0123456789abcdefSECRET"
WEBHOOK_SECRET = "whsec_dGVzdC13ZWJob29rLXNlY3JldC0wMDAwMDAwMDAwMDAw"
KINDS = ["async", "sync"]


def make(kind: str, handler: Any = None) -> Any:
    transport = httpx.MockTransport(handler or Recorder())
    if kind == "async":
        return BlindPay(api_key=KEY, instance_id="in_000000000000", http_client=httpx.AsyncClient(transport=transport))
    return BlindPaySync(api_key=KEY, instance_id="in_000000000000", http_client=httpx.Client(transport=transport))


async def call(kind: str, client: Any, method: str, *args: Any) -> Any:
    result = getattr(client.payouts, method)(*args)
    return await result if kind == "async" else result


@pytest.mark.parametrize("kind", KINDS)
def test_printing_or_dumping_a_client_hides_the_key(kind: str):
    client = make(kind)
    client.payouts  # noqa: B018 -- materialise a cached resource so it shows up in the dump

    dumps = [
        repr(client),
        str(client),
        pprint.pformat(vars(client)),
        pprint.pformat(vars(client._api)),
        repr(client._headers),
        repr(client.payouts.__dict__),
    ]

    for dump in dumps:
        assert KEY not in dump
    assert "***" in repr(client)


@pytest.mark.parametrize("kind", KINDS)
async def test_the_key_still_reaches_the_wire(kind: str):
    recorder = Recorder(body={"data": [], "pagination": {}})
    client = make(kind, recorder)

    await call(kind, client, "list")

    assert recorder.last.headers["Authorization"] == f"Bearer {KEY}"
    assert KEY not in repr(recorder.last.headers)


@pytest.mark.parametrize("kind", KINDS)
async def test_transport_errors_drop_the_query_string(kind: str):
    def refuse(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError(f"connection refused while requesting {request.url}", request=request)

    client = async_client(refuse, max_retries=0) if kind == "async" else sync_client(refuse, max_retries=0)

    response = await call(kind, client, "list", {"receiver_id": "cu_000000000000", "limit": 10})

    error = response["error"]
    assert error["code"] == "SDK_CONNECTION_ERROR"
    assert "/v1/instances/in_000000000000/payouts" in error["message"]
    assert "?" not in error["message"] and "receiver_id" not in error["message"]


def test_webhook_errors_never_echo_the_secret():
    with pytest.raises(WebhookVerificationError) as raised:
        webhooks.construct_event(
            b"{}", {"svix-id": "msg_1", "svix-timestamp": "1", "svix-signature": "v1,x"}, WEBHOOK_SECRET
        )

    assert WEBHOOK_SECRET not in str(raised.value) and WEBHOOK_SECRET not in repr(raised.value)
