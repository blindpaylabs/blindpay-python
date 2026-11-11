"""Workflow: pay a bank account from a managed wallet, with an explicit idempotency key.

Amounts are integer cents. The payout uses ``wallet_id`` (a managed wallet) instead of ``sender_wallet_address``:
pass exactly one of them.
"""

import os
import uuid

from _helpers import unwrap

from blindpay import BlindPaySync


def pay(blindpay: BlindPaySync, bank_account_id: str, wallet_id: str, amount_cents: int) -> str:
    quote = blindpay.quotes.create(
        {
            "bank_account_id": bank_account_id,
            "currency_type": "sender",
            "request_amount": amount_cents,
            "network": "base",
            "token": "USDC",
        }
    )
    key = f"payout-{uuid.uuid4()}"  # persist it with your order before sending
    payout = blindpay.payouts.create_evm(
        {"quote_id": unwrap(quote)["id"], "wallet_id": wallet_id}, {"idempotency_key": key}
    )
    error = payout["error"]
    if error is not None:
        if error.get("retryable"):
            # A 5xx on a payout is never retried automatically: look the payout up first, then resend with the
            # same key (error["idempotency_key"]) only if it doesn't exist.
            raise RuntimeError(f"retry later with idempotency_key={error.get('idempotency_key')}")
        raise RuntimeError(f"{error.get('code')}: {error['message']}")
    return unwrap(payout)["id"]


if __name__ == "__main__":
    with BlindPaySync(api_key=os.environ["BLINDPAY_API_KEY"], instance_id=os.environ["BLINDPAY_INSTANCE_ID"]) as client:
        print(pay(client, os.environ["BANK_ACCOUNT_ID"], os.environ["WALLET_ID"], 1000))
