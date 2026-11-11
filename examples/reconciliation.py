"""Workflow: reconcile a customer's completed payouts with the auto-pager (pages of 100, follows the cursor)."""

import os
from typing import Dict

from blindpay import BlindPaySync


def totals_by_currency(blindpay: BlindPaySync, customer_id: str) -> Dict[str, int]:
    totals: Dict[str, int] = {}
    for payout in blindpay.payouts.list_auto_paging({"customer_id": customer_id, "status": "completed"}):
        currency = str(payout.get("currency") or "unknown")
        totals[currency] = totals.get(currency, 0) + int(payout.get("receiver_amount") or 0)  # cents
    return totals


if __name__ == "__main__":
    with BlindPaySync(api_key=os.environ["BLINDPAY_API_KEY"], instance_id=os.environ["BLINDPAY_INSTANCE_ID"]) as client:
        print(totals_by_currency(client, os.environ["CUSTOMER_ID"]))
