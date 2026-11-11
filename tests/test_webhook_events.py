"""``webhooks.construct_event`` and the generated typed payloads, against the shared webhook fixtures (plan C6)."""

import base64
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple, cast

import pytest

import blindpay
from blindpay import BlindPayError, WebhookVerificationError, construct_webhook_event, webhooks
from blindpay.webhook_events import WEBHOOK_EVENT_TYPES
from tests.spec_fixtures import SPEC_DIR, assert_matches_spec

WEBHOOKS_DIR = SPEC_DIR / "webhooks"
SECRET = "whsec_" + base64.b64encode(b"test-webhook-secret-0000000000000").decode()
NOW = 1_700_000_000


def signed(body: bytes, msg_id: str = "msg_000000000000", timestamp: int = NOW) -> Dict[str, str]:
    key = base64.b64decode(SECRET[len("whsec_") :])
    digest = hmac.new(key, f"{msg_id}.{timestamp}.".encode() + body, hashlib.sha256).digest()
    return {
        "svix-id": msg_id,
        "svix-timestamp": str(timestamp),
        "svix-signature": f"v1,{base64.b64encode(digest).decode()}",
    }


def fixture(path: Path) -> Dict[str, Any]:
    return cast(Dict[str, Any], json.loads(path.read_text()))


EVENT_FILES = sorted(p for p in WEBHOOKS_DIR.glob("*.json") if not p.name.startswith("_"))
VARIANTS: List[Tuple[str, str, Dict[str, Any]]] = [
    (doc["event"], name, payload)
    for doc in (fixture(p) for p in EVENT_FILES)
    for name, payload in doc["variants"].items()
]


def test_every_spec_event_is_typed():
    assert sorted(WEBHOOK_EVENT_TYPES) == sorted(fixture(p)["event"] for p in EVENT_FILES)
    assert len(WEBHOOK_EVENT_TYPES) == 28


@pytest.mark.parametrize("event,variant,payload", VARIANTS, ids=[f"{e}-{v}" for e, v, _ in VARIANTS])
def test_construct_event_returns_every_fixture_variant(event: str, variant: str, payload: Dict[str, Any]):
    body = json.dumps(payload).encode()

    parsed = webhooks.construct_event(body, signed(body), SECRET, now=NOW)

    assert parsed == payload
    assert parsed["webhook_event"] == event, variant


@pytest.mark.parametrize("path", EVENT_FILES, ids=[p.stem for p in EVENT_FILES])
def test_event_type_matches_the_spec_shape(path: Path):
    doc = fixture(path)

    assert_matches_spec(WEBHOOK_EVENT_TYPES[doc["event"]], doc["variants"])


def test_unknown_event_is_returned_as_is():
    doc = fixture(WEBHOOKS_DIR / "_unknown_event.json")
    for payload in doc["variants"].values():
        body = json.dumps(payload).encode()

        parsed = construct_webhook_event(body, signed(body), SECRET, now=NOW)

        assert parsed == payload
        assert parsed["webhook_event"] not in WEBHOOK_EVENT_TYPES


def test_str_payload_and_case_insensitive_headers():
    body = json.dumps({"webhook_event": "customer.delete", "id": "cu_000000000000"})
    headers = {key.upper(): value for key, value in signed(body.encode()).items()}

    assert webhooks.construct_event(body, headers, SECRET, now=NOW)["webhook_event"] == "customer.delete"


Delivery = Tuple[bytes, Dict[str, str]]


def _tamper_body(body: bytes, headers: Dict[str, str]) -> Delivery:
    return body + b" ", headers


def _stale_timestamp(body: bytes, headers: Dict[str, str]) -> Delivery:
    return body, {**headers, "svix-timestamp": str(NOW - 301)}


def _missing_header(body: bytes, headers: Dict[str, str]) -> Delivery:
    return body, {k: v for k, v in headers.items() if k != "svix-id"}


@pytest.mark.parametrize("tamper", [_tamper_body, _stale_timestamp, _missing_header])
def test_unverified_delivery_raises(tamper: Callable[[bytes, Dict[str, str]], Delivery]):
    body = json.dumps({"webhook_event": "customer.delete"}).encode()
    bad_body, bad_headers = tamper(body, signed(body))

    with pytest.raises(WebhookVerificationError):
        webhooks.construct_event(bad_body, bad_headers, SECRET, now=NOW)


@pytest.mark.parametrize("body", [b"not json", b"[1, 2]", b'{"id": "x"}', b'{"webhook_event": 1}'])
def test_verified_but_malformed_body_raises(body: bytes):
    with pytest.raises(BlindPayError) as raised:
        webhooks.construct_event(body, signed(body), SECRET, now=NOW)

    assert not isinstance(raised.value, WebhookVerificationError)


def test_event_types_are_exported_from_the_package_root():
    for cls in WEBHOOK_EVENT_TYPES.values():
        assert getattr(blindpay, cls.__name__) is cls
    for name in ("UnknownWebhookEvent", "WebhookEvent", "WebhookEventName"):
        assert name in blindpay.__all__
