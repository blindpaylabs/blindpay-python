# BlindPay Python SDK <img src="https://github.com/user-attachments/assets/c42b121d-adf1-467c-88ce-6f5be1efa93c" align="right" width="102"/>

[![chat on Discord](https://img.shields.io/discord/856971667393609759.svg?logo=discord)](https://discord.gg/x7ap6Gkbe9)
[![twitter](https://img.shields.io/twitter/follow/blindpaylabs?style=social)](https://twitter.com/intent/follow?screen_name=blindpaylabs)
[![Version](https://img.shields.io/github/v/release/blindpaylabs/blindpay-python?include_prereleases)](https://github.com/blindpaylabs/blindpay-python/releases)

The official Python SDK for [BlindPay](https://blindpay.com) - Stablecoin API for global payments.


## Installation

```bash
pip install blindpay
```

## Requirements

- Python 3.12 or higher

## Quickstart

`BlindPay` is the async client and `BlindPaySync` the sync one. They expose the same resources and methods.

```python
import asyncio

from blindpay import BlindPay


async def main() -> None:
    async with BlindPay(api_key="your_api_key", instance_id="in_000000000000") as blindpay:
        response = await blindpay.payouts.get("po_000000000000")
        if response["error"] is not None:
            print(response["error"]["code"], response["error"]["message"])
            return
        print(response["data"]["status"])


asyncio.run(main())
```

```python
from blindpay import BlindPaySync

with BlindPaySync(api_key="your_api_key", instance_id="in_000000000000") as blindpay:
    response = blindpay.payouts.get("po_000000000000")
```

Each client owns one HTTP connection pool. Close it with `async with` / `with`, or `await blindpay.aclose()` /
`blindpay.close()`. A configured client is safe to share across threads (sync) or tasks (async); per-request options
never change it.

## Configuration

```python
blindpay = BlindPay(
    api_key="your_api_key",
    instance_id="in_000000000000",
    base_url="https://api.blindpay.com",  # default; a proxy URL also works (it receives your API key)
    timeout=60.0,  # seconds per attempt (default 60)
    max_retries=2,  # retries after the first attempt (default 2); 0 turns retries off
    http_client=None,  # your own httpx.AsyncClient (httpx.Client for BlindPaySync), e.g. with a mock transport
)
```

When you pass `http_client`, closing the BlindPay client leaves it open: you own it.

## Error handling

Methods never raise for API or network errors. They return a dict with either `data` or `error`:

```python
response = await blindpay.customers.get("cu_000000000000")

if response["error"] is not None:
    error = response["error"]
    print(error["message"])  # always present
    print(error.get("status"))  # HTTP status, or 0 when no response arrived (timeout, connection error)
    print(error.get("code"))  # stable UPPERCASE API code, e.g. "CUSTOMERS_NOT_FOUND"; "SDK_TIMEOUT" etc. client-side
    print(error.get("description"), error.get("errors"), error.get("trace_id"))
    print(error.get("request_id"))  # the X-Request-Id response header; quote it to support
    print(error.get("idempotency_key"))  # the key this request carried (see below)
    print(error.get("retryable"))  # True when resending with the same idempotency_key may succeed
else:
    customer = response["data"]
```

`BlindPayError` is raised only for programming errors caught before a request is sent (a missing API key, an
invalid `idempotency_key`). `list_auto_paging` iterators raise `BlindPayApiError`, which carries the same fields as
attributes, because an iterator can't return an error dict.

## Idempotency and retries

Every method that creates, changes or deletes something takes a trailing `options` argument:

```python
response = await blindpay.payouts.create_evm(
    {"quote_id": "qu_000000000000", "wallet_id": "wa_000000000000"},
    {"idempotency_key": "payout-for-order-42", "timeout": 30, "headers": {"X-Trace": "abc"}},
)
```

- `idempotency_key` (1 to 255 characters) is sent as `Idempotency-Key`. The API stores the response for that key, so
  resending the same request with the same key returns the stored result instead of creating a second payout. An
  empty key or one longer than 255 characters raises `BlindPayError` before anything is sent.
- With retries on (the default) and no key of yours, the SDK generates a UUIDv4 key before the first attempt, so a
  retried request can't execute twice. Uploads (`upload.create`, `upload.analyze`) never carry a key: the API
  doesn't deduplicate multipart requests.
- `timeout` overrides the client's per-attempt timeout; `headers` adds headers to this request only.

What the SDK retries, with exponential backoff (0.5 s doubling up to 8 s, with jitter) or the server's
`Retry-After` when it is 60 s or less:

| Request | Retried on |
|---|---|
| `GET` | connection errors, timeouts, HTTP 408, 429, 500, 502, 503, 504 |
| `POST` / `PUT` / `PATCH` / `DELETE` | connection errors and timeouts (no response arrived), 429, and 409 `idempotency_key_in_flight`, always with the same key and bytes |
| Uploads | connection failures before anything was sent |

A mutation that gets a 5xx is **not** retried: the API releases the idempotency key on a 5xx, so a resend could run
the operation twice. The error comes back with `retryable: True` and the `idempotency_key` it used. **If a create
or payout returns a 5xx, look the resource up (by quote, external id, or a list filter) before resending. Resend
with the same `idempotency_key` from the error.**

## Pagination

Payouts, payins, customers and transfers have cursor pagination. `list` returns one page: the
`{"data": [...], "pagination": {"has_more", "next_page", "prev_page"}}` envelope when you pass `limit`,
`starting_after` or `ending_before`, and (for payouts, payins and customers) a bare list of **every** row when you
pass none of them. For large collections use the auto-pager, which requests pages of 100 and follows
`pagination.next_page` for you:

```python
async for payout in blindpay.payouts.list_auto_paging({"customer_id": "cu_000000000000", "status": "completed"}):
    print(payout["id"], payout["status"])

for customer in blindpay_sync.customers.list_auto_paging():
    ...
```

Pagers only page forward (`ending_before` raises `BlindPayError`). Each page goes through the retry policy above;
an error that survives it raises `BlindPayApiError`.

## Webhooks

Verify every delivery against the **raw** request body, before parsing it. No client or API key is needed:

```python
from blindpay import webhooks

# Flask: request.get_data(); FastAPI/Starlette: await request.body()
raw_body = request.get_data()

if not webhooks.verify(raw_body, request.headers, secret):  # secret: "whsec_..."
    abort(400)
```

`verify` checks the Svix `v1` signatures in `svix-signature` and rejects timestamps more than 5 minutes from now
(`tolerance=` changes that). Deduplicate deliveries on the `svix-id` header, and never log the secret.

To verify and parse in one step, use `construct_event`. It returns a typed `WebhookEvent`, a union of one
`TypedDict` per event that type checkers narrow on `webhook_event`. It raises `WebhookVerificationError` when the
signature or timestamp doesn't verify:

```python
from blindpay import WebhookVerificationError, webhooks

try:
    event = webhooks.construct_event(raw_body, request.headers, secret)
except WebhookVerificationError:
    abort(400)

if event["webhook_event"] in ("payout.update", "payout.complete") and event.get("status") == "failed":
    ...  # a failed payout can arrive on either event: branch on status, not on the event name
```

Events this SDK version doesn't know yet are returned as-is (`UnknownWebhookEvent`) instead of failing.

## Uploads

`upload.create` and `upload.analyze` send `multipart/form-data`. Pass bytes or a binary file object:

```python
with open("proof_of_address.pdf", "rb") as f:
    response = await blindpay.upload.create({"bucket": "onboarding", "file": f})

file_url = response["data"]["file_url"]
```

The API checks the file's MIME type, which the SDK guesses from the filename (or the file's first bytes). Pass
`filename` and `content_type` to set them explicitly.

## Types

The SDK includes comprehensive type definitions for all API resources and parameters. These can be imported from the main package:

```python
from blindpay import (
    AccountClass,
    BankAccountType,
    Country,
    Currency,
    CurrencyType,
    Network,
    Rail,
    StablecoinToken,
    TransactionDocumentType,
    TransactionStatus,
    PaginationParams,
    PaginationMetadata,
    # ... and more
)
```

## Development

This SDK uses:
- `uv` for package management
- `httpx` for HTTP (one pooled client per BlindPay client)
- `typing_extensions` for typing

## License

MIT

## Support

Read the [API docs](https://blindpay.com/docs) or open an issue on [GitHub](https://github.com/blindpaylabs/blindpay-python/issues).
