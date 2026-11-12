"""Workflow: fund a managed wallet with a payin, then pay a bank account from it with ``wallet_id``.

1. ``wallets.custodial.create`` gives the customer a BlindPay-managed wallet.
2. A payin quote with ``wallet_id`` and ``payins.create_evm`` fund it (dev payins complete in about 30 s).
3. A payout quote with ``bank_account_id`` and ``payouts.create_evm`` with ``wallet_id`` pay out of it. A payout
   takes exactly one of ``wallet_id`` (managed, on the quote's network) or ``sender_wallet_address`` (self-custody).

Amounts are integer cents. On a development instance the payout quote's ``request_amount`` picks the outcome:
``66600`` ends ``failed`` and ``77700`` ends ``refunded``. Production code waits for the ``payin.complete`` and
``payout.complete`` webhooks (see ``webhook_endpoint.py``) instead of polling.
"""

import os
import time
import uuid
from typing import Callable, Union

from _helpers import unwrap

from blindpay import BlindPaySync, Network

FINAL_STATUSES = {"completed", "failed", "refunded"}
FAILS = 66600  # dev sentinel: the payout fails
REFUNDS = 77700  # dev sentinel: the payout is refunded


def wait_for(read_status: Callable[[], Union[str, None]], timeout: float = 120, every: float = 5) -> str:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        status = read_status()
        if status in FINAL_STATUSES:
            return status
        time.sleep(every)
    raise TimeoutError("no final status yet: keep waiting for the webhook")


def fund_managed_wallet(blindpay: BlindPaySync, customer_id: str, network: Network, amount_cents: int) -> str:
    wallet = unwrap(blindpay.wallets.custodial.create({"customer_id": customer_id, "network": network, "name": "ops"}))
    quote = unwrap(
        blindpay.payins.quotes.create(
            {
                "wallet_id": wallet["id"],
                "currency_type": "sender",
                "payment_method": "pix",
                "request_amount": amount_cents,
                "token": "USDB",
            }
        )
    )
    payin = unwrap(blindpay.payins.create_evm(quote["id"], {"idempotency_key": f"payin-{uuid.uuid4()}"}))
    status = wait_for(lambda: unwrap(blindpay.payins.get(payin["id"]))["status"])
    if status != "completed":
        raise RuntimeError(f"payin {payin['id']} ended {status}")
    return wallet["id"]


def pay_out(blindpay: BlindPaySync, wallet_id: str, bank_account_id: str, network: Network, amount_cents: int) -> str:
    quote = unwrap(
        blindpay.quotes.create(
            {
                "bank_account_id": bank_account_id,
                "currency_type": "sender",
                "request_amount": amount_cents,
                "network": network,
                "token": "USDB",
            }
        )
    )
    key = f"payout-{uuid.uuid4()}"  # persist it with your order before sending
    payout = unwrap(
        blindpay.payouts.create_evm({"quote_id": quote["id"], "wallet_id": wallet_id}, {"idempotency_key": key})
    )
    status = wait_for(lambda: unwrap(blindpay.payouts.get(payout["id"]))["status"])
    if status == "failed":
        print(f"payout {payout['id']} failed: check the payout before quoting again")
    elif status == "refunded":
        print(f"payout {payout['id']} was refunded")
    return status


if __name__ == "__main__":
    network: Network = "base_sepolia"
    with BlindPaySync(api_key=os.environ["BLINDPAY_API_KEY"], instance_id=os.environ["BLINDPAY_INSTANCE_ID"]) as client:
        wallet_id = fund_managed_wallet(client, os.environ["CUSTOMER_ID"], network, 100000)
        for amount in (10000, FAILS, REFUNDS):
            print(amount, pay_out(client, wallet_id, os.environ["BANK_ACCOUNT_ID"], network, amount))
