"""Workflow: register a webhook endpoint, then verify and handle deliveries.

Verify against the raw request body (Flask: ``request.get_data()``, FastAPI: ``await request.body()``), deduplicate
on ``svix-id`` (deliveries can repeat), and never log the ``whsec_`` secret.
"""

import os
from typing import Mapping, Set

from _helpers import unwrap

from blindpay import BlindPaySync, WebhookVerificationError, webhooks

seen_deliveries: Set[str] = set()  # use a database table in production


def register_endpoint(blindpay: BlindPaySync, url: str) -> str:
    created = blindpay.instances.webhook_endpoints.create(
        {"url": url, "events": ["payout.update", "payout.complete", "payin.complete"]}
    )
    secret = unwrap(blindpay.instances.webhook_endpoints.get_secret(unwrap(created)["id"]))
    return secret["key"]  # store it like a password


def handle_delivery(raw_body: bytes, headers: Mapping[str, str], secret: str) -> int:
    """Returns the HTTP status to answer the delivery with."""
    try:
        event = webhooks.construct_event(raw_body, headers, secret)
    except WebhookVerificationError:
        return 400
    delivery_id = {k.lower(): v for k, v in headers.items()}["svix-id"]
    if delivery_id in seen_deliveries:
        return 200
    seen_deliveries.add(delivery_id)

    if event["webhook_event"] in ("payout.update", "payout.complete"):
        # A failed payout can arrive on either event: branch on status, not on the event name.
        if event.get("status") == "failed":
            print(f"payout {event.get('id')} failed")
    elif event["webhook_event"] == "payin.complete":
        print(f"payin {event.get('id')} completed")
    return 200


if __name__ == "__main__":
    with BlindPaySync(api_key=os.environ["BLINDPAY_API_KEY"], instance_id=os.environ["BLINDPAY_INSTANCE_ID"]) as client:
        print(register_endpoint(client, "https://example.com/webhooks/blindpay")[:10] + "...")
