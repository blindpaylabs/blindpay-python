"""``unwrap``: the typed way to read ``data`` in both pyright and mypy, and the error it raises."""

from typing import Any, Optional

import httpx
import pytest
from typing_extensions import assert_type

from blindpay import BlindPayApiError, ErrorCode, RetryClass, SuccessResponse, unwrap
from blindpay.resources.payouts.payouts import Payout
from tests.http_mock import async_client, sync_client

PAYOUT = {"id": "po_000000000000", "status": "processing"}
KINDS = ["async", "sync"]


def client(kind: str, status: int, body: Any) -> Any:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, json=body)

    return async_client(handler, max_retries=0) if kind == "async" else sync_client(handler, max_retries=0)


async def call(kind: str, result: Any) -> Any:
    return await result if kind == "async" else result


@pytest.mark.parametrize("kind", KINDS)
async def test_unwrap_returns_the_data(kind: str):
    response = await call(kind, client(kind, 200, PAYOUT).payouts.get("po_000000000000"))

    assert unwrap(response) == PAYOUT


@pytest.mark.parametrize("kind", KINDS)
async def test_unwrap_raises_the_api_error(kind: str):
    body = {"code": "TRANSFERS_SWAP_AMOUNT_BELOW_MINIMUM", "message": "fx_amount_below_minimum"}
    response = await call(kind, client(kind, 400, body).payouts.get("po_000000000000"))

    with pytest.raises(BlindPayApiError) as raised:
        unwrap(response)

    assert raised.value.code == ErrorCode.TRANSFERS_SWAP_AMOUNT_BELOW_MINIMUM
    assert raised.value.status == 400 and raised.value.retry_class is RetryClass.ACTIONABLE
    assert raised.value.error is response["error"]


@pytest.mark.parametrize("kind", KINDS)
async def test_deletes_return_the_success_body(kind: str):
    response = await call(kind, client(kind, 200, {"success": True}).partner_fees.delete("pf_000000000000"))

    assert unwrap(response) == {"success": True}


def test_unwrap_is_typed_as_the_data_without_narrowing() -> None:
    """Type-level: pyright (strict) and mypy check these ``assert_type`` calls; the error check doesn't narrow."""
    from blindpay import BlindPaySync

    def read(blindpay: BlindPaySync) -> None:
        response = blindpay.payouts.get("po_000000000000")
        error = response["error"]
        if error is not None:
            return
        assert_type(unwrap(response), Payout)
        deleted = blindpay.partner_fees.delete("pf_000000000000")
        assert_type(unwrap(deleted), Optional[SuccessResponse])

    assert callable(read)
