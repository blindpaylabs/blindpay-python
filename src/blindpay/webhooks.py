"""Standalone verification of BlindPay webhooks (Svix signatures).

BlindPay delivers webhooks through Svix. Verify each delivery against the raw request body, before parsing it::

    from blindpay import webhooks

    if not webhooks.verify(request_body, request.headers, secret):
        return 400

No API key or client is needed. Never log the ``whsec_`` secret, and deduplicate deliveries on ``svix-id``.
"""

import base64
import binascii
import hashlib
import hmac
import re
import time
from typing import Mapping, Optional, Union

__all__ = ["DEFAULT_TOLERANCE_SECONDS", "verify"]

DEFAULT_TOLERANCE_SECONDS = 300
"""How far, in seconds, a delivery's ``svix-timestamp`` may be from the current time (replay protection)."""

_SECRET_PREFIX = "whsec_"
_TIMESTAMP_PATTERN = re.compile(r"[0-9]+")


def _header(headers: Mapping[str, str], *names: str) -> Optional[str]:
    lowered = {key.lower(): value for key, value in headers.items()}
    for name in names:
        value = lowered.get(name)
        if value is not None:
            return value
    return None


def _decode_secret(secret: str) -> Optional[bytes]:
    if secret.startswith(_SECRET_PREFIX):
        secret = secret[len(_SECRET_PREFIX) :]
    try:
        return base64.b64decode(secret)
    except (binascii.Error, ValueError):
        return None


def verify(
    payload: Union[str, bytes],
    headers: Mapping[str, str],
    secret: str,
    *,
    tolerance: int = DEFAULT_TOLERANCE_SECONDS,
    now: Optional[float] = None,
) -> bool:
    """Return whether a webhook delivery carries a valid BlindPay (Svix) signature. Never raises.

    Args:
        payload: The raw request body, exactly as received. Re-serialized JSON will not verify.
        headers: The request headers. Names are matched case-insensitively; ``svix-id``,
            ``svix-timestamp`` and ``svix-signature`` are read (``webhook-*`` aliases are accepted).
        secret: The endpoint's signing secret (``whsec_...``), from ``instances.webhook_endpoints.get_secret``.
        tolerance: Maximum distance, in seconds, between ``svix-timestamp`` and ``now``.
        now: Unix time to check the timestamp against. Defaults to the current time.

    Returns:
        True if any ``v1`` signature in ``svix-signature`` matches and the timestamp is within tolerance.
    """
    try:
        msg_id = _header(headers, "svix-id", "webhook-id")
        timestamp = _header(headers, "svix-timestamp", "webhook-timestamp")
        signature_header = _header(headers, "svix-signature", "webhook-signature")
        if msg_id is None or timestamp is None or signature_header is None:
            return False

        if not _TIMESTAMP_PATTERN.fullmatch(timestamp):
            return False
        current = time.time() if now is None else now
        if abs(current - int(timestamp)) > tolerance:
            return False

        key = _decode_secret(secret)
        if not key:
            return False

        body = payload.encode("utf-8") if isinstance(payload, str) else bytes(payload)
        signed_content = f"{msg_id}.{timestamp}.".encode() + body
        expected = base64.b64encode(hmac.new(key, signed_content, hashlib.sha256).digest())

        for entry in signature_header.split(" "):
            version, _, signature = entry.partition(",")
            if version != "v1":
                continue
            candidate = signature.encode("utf-8")
            if len(candidate) == len(expected) and hmac.compare_digest(candidate, expected):
                return True
        return False
    except Exception:
        return False
