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

## Resources

Both clients expose the same namespaces (94 of 94 public API operations):

| Namespace | What it covers |
|---|---|
| `available` | rails, bank-detail fields, NAICS codes, SWIFT lookups |
| `customers` (+ `.bank_accounts`, `.rfi`) | customers (KYC/KYB), limits, limit increases, bank accounts incl. `create_plaid_link`, compliance RFIs |
| `quotes`, `payouts` | payout quotes and FX, EVM/Solana/Stellar payouts, documents, tracking |
| `payins` (+ `.quotes`) | payin quotes and FX, EVM payins, tracking |
| `payables` | bills to pay (boleto, PIX code, invoice) |
| `transfers` | transfer quotes and transfers between wallets |
| `virtual_accounts` | virtual accounts (US, Mexico, Colombia) |
| `wallets.blockchain` / `.offramp` / `.custodial` | external wallets (incl. `set_self_custody`), offramp wallets, managed wallets (balances, deposits) |
| `instances` (+ `.webhook_endpoints`, `.terms_of_service`, `.onboarding`, `.rfi`) | your instance, members, webhook endpoints, ToS links, onboarding answers |
| `partner_fees`, `fees` | partner fees and your billing fees |
| `upload` | multipart upload and document analysis, `presign` |

Every input, output and enum type is importable from the package root (`from blindpay import Payout, CreateQuoteInput`).

### Amounts and units

- Payout, payin, quote, payable and limit amounts are **integer cents** (`1000` = 10.00).
- Partner percentage fees are **basis points** (`100` = 1%); flat fees are cents.
- Managed-wallet balances (`wallets.custodial.get_balance`) are **whole tokens** (`10.5` = 10.5 USDC).
- Transfers that swap between different tokens need at least **100 USDC**, measured on the USDC side. Below that,
  `transfers.create_quote` returns a 400 with code `TRANSFERS_SWAP_AMOUNT_BELOW_MINIMUM` (see Error codes).

### Limit increases

`customers.get_limit_increase_requests` and the `limitIncrease.new` / `limitIncrease.update` webhooks carry
`review_reason`: why compliance rejected the request or approved lower limits than requested, and what to send to get
the full amount. It is set when the status is rejected or the approval is below the requested limits, and `None`
otherwise.

### "Exactly one of" inputs

- `payouts.create_evm` / `create_solana` / `create_stellar` / `authorize_stellar_token`: pass `sender_wallet_address`
  **or** `wallet_id` (a managed wallet), not both.
- `quotes.create`: pass `bank_account_id` **or** `payable_id`.

The SDK doesn't validate these; the API answers 400.

### Testing on a development instance

Development instances simulate settlement (test token `USDB`). Payouts of `66600` cents fail and `77700` are refunded;
dev payins complete in about 30 s; quotes expire after 5 minutes (OTC payin quotes after 10 s). Development instances
are rate limited per instance on every route; a limited call returns 429 `AUTH_RATE_LIMITED` with a `Retry-After`
header, which the SDK honours when it retries.

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
    print(error.get("retry_class"))  # the API's class for this code: retryable, terminal, actionable or unknown
else:
    customer = response["data"]
```

### Error codes

Branch on `code`, the stable identifier; `message` is a legacy machine string kept for compatibility, and a few
bodies (idempotency conflicts) carry no `code` at all. `ErrorCode` lists every code in the API spec, and because it is
a `str` enum it compares equal to the plain string in `error["code"]`. Codes added to the API after your SDK version
still arrive as strings.

```python
from blindpay import ErrorCode, RetryClass, error_code_info

response = await blindpay.transfers.create_quote(quote_input)
error = response["error"]
if error is not None:
    if error.get("code") == ErrorCode.TRANSFERS_SWAP_AMOUNT_BELOW_MINIMUM:
        ...  # swaps between different tokens need at least 100 USDC, measured on the USDC side
    elif error.get("retry_class") == RetryClass.ACTIONABLE:
        ...  # fix something first (fund the balance, correct the bank details), then try again
    info = error_code_info(error.get("code"))  # ErrorCodeInfo(status=400, retry=RetryClass.ACTIONABLE), or None
```

`retry_class` (`RetryClass.RETRYABLE`, `TERMINAL`, `ACTIONABLE`, or `UNKNOWN` for no code, an `SDK_*` code or a
code this version doesn't know) is the API's classification of the code. `retryable` is the SDK's decision for this
exact request and is the one to act on: a payout that got a 5xx is never `retryable`, whatever its code says.
`ErrorCodeInfo.status` is the status a code typically comes with; each endpoint can use another.

`BlindPayError` is raised only for programming errors caught before a request is sent (a missing API key, an
invalid `idempotency_key`). `list_auto_paging` iterators raise `BlindPayApiError`, which carries the same fields as
attributes, because an iterator can't return an error dict.

## Idempotency and retries

Every method takes a trailing `options` argument:

```python
response = await blindpay.payouts.create_evm(
    {"quote_id": "qu_000000000000", "wallet_id": "wa_000000000000"},
    {"idempotency_key": "payout-for-order-42", "timeout": 30, "headers": {"X-Trace": "abc"}},
)
```

- `idempotency_key` (1 to 255 characters) is sent as `Idempotency-Key`. The API stores the response for that key, so
  resending the same request with the same key returns the stored result instead of creating a second payout. An
  empty, padded or non-ASCII key, or one longer than 255 characters, raises `BlindPayError` before anything is
  sent.
- With retries on (the default) and no key of yours, the SDK generates a UUIDv4 key before the first attempt, so a
  retried request can't execute twice. Uploads (`upload.create`, `upload.analyze`) never carry a key: the API
  doesn't deduplicate multipart requests.
- `timeout` overrides the client's per-attempt timeout; `headers` adds headers to this request only (names are
  case-insensitive; `Authorization`, `User-Agent` and `Idempotency-Key` can't be set this way).
- Reads take the same argument, e.g. `await blindpay.payouts.get("pa_000000000000", {"timeout": 10})`. They use
  `timeout` and `headers` and never send an `Idempotency-Key`.

Indicative FX quote endpoints are rate limited per instance; a limited call returns 429 `AUTH_RATE_LIMITED` with a
`Retry-After` header, which the SDK honours when it retries.

What the SDK retries, with exponential backoff (0.5 s doubling up to 8 s, with jitter) or the server's
`Retry-After` when it is 60 s or less:

| Request | Retried on |
|---|---|
| `GET` | connection errors, timeouts, HTTP 408, 429, 500, 502, 503, 504 |
| `POST` / `PUT` / `PATCH` / `DELETE` | connection errors and timeouts before any response arrived, 429, and 409 `idempotency_key_in_flight`, always with the same key and bytes |
| Uploads | connection failures before anything was sent |

A mutation that gets a 5xx is **not** retried: the API releases the idempotency key on a 5xx, so a resend could run
the operation twice. The error comes back with `retryable: True` and the `idempotency_key` it used. **If a create
or payout returns a 5xx, look the resource up (by quote, external id, or a list filter) before resending. Resend
with the same `idempotency_key` from the error.**

## Pagination

Payouts, payins, payables, customers, transfers and managed-wallet deposits have cursor pagination. `list` returns one page: the
`{"data": [...], "pagination": {"has_more", "next_page", "prev_page"}}` envelope when you pass `limit`,
`starting_after` or `ending_before`, and (for payouts, payins, payables and customers) a bare list of **every** row
when you pass none of them. Transfers and deposits always return the envelope. For large collections use the auto-pager, which requests pages of 100 and follows
`pagination.next_page` for you:

```python
async for payout in blindpay.payouts.list_auto_paging({"customer_id": "cu_000000000000", "status": "completed"}):
    print(payout["id"], payout["status"])

for customer in blindpay_sync.customers.list_auto_paging():
    ...

deposits = blindpay_sync.wallets.custodial.get_deposits_auto_paging({"customer_id": "cu_000000000000", "id": "wa_000000000000"})
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

`upload.presign({"file_url": file_url})` returns a short-lived signed URL (`file_url`, `expires_at`) to download an
uploaded file.

## Upgrading from 3.x to 4.x

No public method or type was removed. Things that behave differently:

- **Retries and timeouts are on by default**: each attempt times out after 60 s (httpx's default was 5 s), and
  requests are retried up to 2 times as described above. Mutations carry an auto-generated `Idempotency-Key`. Pass
  `max_retries=0` to get the old single-attempt behaviour.
- **Typing only** (nothing changes at runtime; type checkers may report new warnings):
  - Response fields the API can omit are `NotRequired`, and nullable ones are `Optional`: read them with `.get()`.
  - Response enum fields are `Union[<known values>, str]`, so values added by the API later still type-check.
  - Request inputs follow the API's required fields: some keys became optional (`sender_wallet_address`,
    quote `bank_account_id`, most customer fields), and a few the API always required are now required
    (`name` on ACH/wire/SWIFT/RTP bank accounts, payin-quote `currency_type`/`payment_method`/`request_amount`/
    `token`, transfer-quote fields, `banking_partner`/`blockchain_wallet_id`/`token` on virtual accounts,
    `name` on `instances.update`).
  - `request_amount` on `quotes.create` and `payins.quotes.create` is `int` (cents), no longer `float`.
  - `retryable` on errors is now `False` for a mutation that carried no idempotency key, and for a mutation 408.
  - `payouts.list`, `payins.list` and `payables.list` return the `{data, pagination}` envelope **or** a bare list
    (see Pagination); `virtual_accounts.list` returns a list.
- `client.verify_webhook_signature` still works but is deprecated: use `webhooks.verify` / `webhooks.construct_event`.
- `payouts.export` and `payins.export` call a route that doesn't exist and are deprecated.

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

## Releases

Merging to `main` publishes to PyPI through release-please. [RELEASING.md](RELEASING.md) covers the flow, the secrets,
how to unstick a release and how to verify a published version.

## License

MIT

## Support

Read the [API docs](https://blindpay.com/docs) or open an issue on [GitHub](https://github.com/blindpaylabs/blindpay-python/issues).
