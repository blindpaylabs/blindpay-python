"""GENERATED from README.md by tests/test_readme_snippets.py. Do not edit: edit the README and re-render."""
# ruff: noqa
# pyright: reportUnusedImport=false, reportUnusedVariable=false, reportUnusedFunction=false

from typing import Any, Callable, NoReturn

from blindpay import BlindPay, BlindPaySync, CreateTransferQuoteInput


async def readme_block_1() -> None:
    import asyncio

    from blindpay import BlindPay, unwrap


    async def main() -> None:
        async with BlindPay(api_key="your_api_key", instance_id="in_000000000000") as blindpay:
            response = await blindpay.payouts.get("po_000000000000")
            error = response["error"]
            if error is not None:
                print(error.get("code"), error["message"])
                return
            payout = unwrap(response)  # the data, typed for mypy and pyright alike (see Type checkers)
            print(payout["status"])


    asyncio.run(main())


async def readme_block_2() -> None:
    from blindpay import BlindPaySync

    with BlindPaySync(api_key="your_api_key", instance_id="in_000000000000") as blindpay:
        response = blindpay.payouts.get("po_000000000000")


async def readme_block_3() -> None:
    blindpay = BlindPay(
        api_key="your_api_key",
        instance_id="in_000000000000",
        base_url="https://api.blindpay.com",  # default; a proxy URL also works (it receives your API key)
        timeout=60.0,  # seconds per attempt (default 60)
        max_retries=2,  # retries after the first attempt (default 2); 0 turns retries off
        http_client=None,  # your own httpx.AsyncClient (httpx.Client for BlindPaySync), e.g. with a mock transport
    )


async def readme_block_4(blindpay: BlindPay, request: Any) -> None:
    from blindpay import unwrap

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
        customer = unwrap(response)  # typed data; see Type checkers below


async def readme_block_5(blindpay: BlindPay, quote_input: CreateTransferQuoteInput) -> None:
    from blindpay import ErrorCode, RetryClass, error_code_info

    response = await blindpay.transfers.create_quote(quote_input)
    error = response["error"]
    if error is not None:
        if error.get("code") == ErrorCode.TRANSFERS_SWAP_AMOUNT_BELOW_MINIMUM:
            ...  # swaps between different tokens need at least 100 USDC, measured on the USDC side
        elif error.get("retry_class") == RetryClass.ACTIONABLE:
            ...  # fix something first (fund the balance, correct the bank details), then try again
        info = error_code_info(error.get("code"))  # ErrorCodeInfo(status=400, retry=RetryClass.ACTIONABLE), or None


async def readme_block_6(blindpay: BlindPay) -> None:
    response = await blindpay.payouts.create_evm(
        {"quote_id": "qu_000000000000", "wallet_id": "wa_000000000000"},
        {"idempotency_key": "payout-for-order-42", "timeout": 30, "headers": {"X-Trace": "abc"}},
    )


async def readme_block_7(blindpay: BlindPay, blindpay_sync: BlindPaySync) -> None:
    async for payout in blindpay.payouts.list_auto_paging({"customer_id": "cu_000000000000", "status": "completed"}):
        print(payout["id"], payout["status"])

    for customer in blindpay_sync.customers.list_auto_paging():
        ...

    deposits = blindpay_sync.wallets.custodial.get_deposits_auto_paging({"customer_id": "cu_000000000000", "id": "wa_000000000000"})


async def readme_block_8(blindpay: BlindPay, request: Any, secret: str, abort: Callable[[int], NoReturn]) -> None:
    from blindpay import webhooks

    # Flask: request.get_data(); FastAPI/Starlette: await request.body()
    raw_body = request.get_data()

    if not webhooks.verify(raw_body, request.headers, secret):  # secret: "whsec_..."
        abort(400)


async def readme_block_9(blindpay: BlindPay, request: Any, secret: str, raw_body: bytes, abort: Callable[[int], NoReturn]) -> None:
    from blindpay import WebhookVerificationError, webhooks

    try:
        event = webhooks.construct_event(raw_body, request.headers, secret)
    except WebhookVerificationError:
        abort(400)

    if event["webhook_event"] in ("payout.update", "payout.complete") and event.get("status") == "failed":
        ...  # a failed payout can arrive on either event: branch on status, not on the event name


async def readme_block_10(blindpay: BlindPay) -> None:
    from blindpay import unwrap

    with open("proof_of_address.pdf", "rb") as f:
        response = await blindpay.upload.create({"bucket": "onboarding", "file": f})

    file_url = unwrap(response)["file_url"]  # raises BlindPayApiError if the upload failed


async def readme_block_11(blindpay: BlindPay) -> None:
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
