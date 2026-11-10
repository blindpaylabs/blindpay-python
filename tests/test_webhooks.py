"""Webhook verification against the shared Svix vectors (tests/fixtures/webhook-vectors.json).

The vectors were generated and self-verified with the official svix package. Each one is run through the
standalone verifier and through both clients' ``verify_webhook_signature`` wrappers.
"""

import base64
import hashlib
import hmac
from typing import Any, Dict

import pytest

from blindpay import BlindPay, BlindPaySync, webhooks
from tests.spec_fixtures import load_webhook_vectors

VECTORS = load_webhook_vectors()
VECTOR_IDS = [vector["name"] for vector in VECTORS]
# The clients' verify_webhook_signature keeps accepting the bare signature that earlier SDK versions required.
WRAPPER_ACCEPTS = {"invalid_bare_signature_without_v1_prefix"}

SECRET = "whsec_MfKQ9r8GKYqrTwjUPD8ILPZIo2LaLaSw"
NOW = 1762790400
PAYLOAD = '{"webhook_event":"payout.complete","id":"pa_000000000000"}'


def sign(payload: str, msg_id: str = "msg_000000000000", timestamp: int = NOW, secret: str = SECRET) -> Dict[str, str]:
    key = base64.b64decode(secret.removeprefix("whsec_"))
    digest = hmac.new(key, f"{msg_id}.{timestamp}.{payload}".encode(), hashlib.sha256).digest()
    return {
        "svix-id": msg_id,
        "svix-timestamp": str(timestamp),
        "svix-signature": f"v1,{base64.b64encode(digest).decode()}",
    }


def test_all_fourteen_vectors_are_present():
    assert len(VECTORS) == 14


@pytest.mark.parametrize("vector", VECTORS, ids=VECTOR_IDS)
def test_standalone_verify_matches_vector(vector: Dict[str, Any]):
    result = webhooks.verify(vector["payload"], vector["headers"], vector["secret"], now=vector["now"])
    assert result is (vector["expect"] == "valid")


@pytest.mark.parametrize("vector", VECTORS, ids=VECTOR_IDS)
def test_standalone_verify_accepts_raw_bytes(vector: Dict[str, Any]):
    payload = vector["payload"].encode()
    assert webhooks.verify(payload, vector["headers"], vector["secret"], now=vector["now"]) is (
        vector["expect"] == "valid"
    )


@pytest.mark.parametrize("client_class", [BlindPay, BlindPaySync])
@pytest.mark.parametrize("vector", VECTORS, ids=VECTOR_IDS)
def test_client_wrapper_matches_vector(vector: Dict[str, Any], client_class: Any, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("blindpay.webhooks.time.time", lambda: float(vector["now"]))
    client = client_class(api_key="test_key", instance_id="in_000000000000")
    headers = vector["headers"]
    result = client.verify_webhook_signature(
        secret=vector["secret"],
        id=headers.get("svix-id", ""),
        timestamp=headers.get("svix-timestamp", ""),
        payload=vector["payload"],
        svix_signature=headers.get("svix-signature", ""),
    )
    expected = vector["expect"] == "valid" or vector["name"] in WRAPPER_ACCEPTS
    assert result is expected


class TestClientWrapperCompatibility:
    @pytest.mark.parametrize("client_class", [BlindPay, BlindPaySync])
    def test_bare_signature_is_still_accepted_by_the_wrapper(self, client_class: Any, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr("blindpay.webhooks.time.time", lambda: float(NOW))
        headers = sign(PAYLOAD)
        bare = headers["svix-signature"].removeprefix("v1,")
        client = client_class(api_key="test_key", instance_id="in_000000000000")

        assert client.verify_webhook_signature(
            secret=SECRET,
            id=headers["svix-id"],
            timestamp=headers["svix-timestamp"],
            payload=PAYLOAD,
            svix_signature=bare,
        )
        assert webhooks.verify(PAYLOAD, {**headers, "svix-signature": bare}, SECRET, now=NOW) is False


class TestVerifyEdgeCases:
    def test_valid_signature(self):
        assert webhooks.verify(PAYLOAD, sign(PAYLOAD), SECRET, now=NOW) is True

    def test_header_names_are_case_insensitive(self):
        headers = {key.upper(): value for key, value in sign(PAYLOAD).items()}
        assert webhooks.verify(PAYLOAD, headers, SECRET, now=NOW) is True

    def test_webhook_header_aliases_are_accepted(self):
        headers = {key.replace("svix-", "webhook-"): value for key, value in sign(PAYLOAD).items()}
        assert webhooks.verify(PAYLOAD, headers, SECRET, now=NOW) is True

    def test_secret_without_whsec_prefix(self):
        assert webhooks.verify(PAYLOAD, sign(PAYLOAD), SECRET.removeprefix("whsec_"), now=NOW) is True

    def test_secret_that_is_not_base64_returns_false(self):
        assert webhooks.verify(PAYLOAD, sign(PAYLOAD), "whsec_not-base64!", now=NOW) is False

    def test_empty_secret_returns_false(self):
        assert webhooks.verify(PAYLOAD, sign(PAYLOAD), "", now=NOW) is False

    def test_non_ascii_signature_returns_false(self):
        headers = {**sign(PAYLOAD), "svix-signature": "v1,çñ€"}
        assert webhooks.verify(PAYLOAD, headers, SECRET, now=NOW) is False

    def test_unicode_digit_timestamp_returns_false(self):
        headers = {**sign(PAYLOAD), "svix-timestamp": "١٧٦٢٧٩٠٤٠٠"}
        assert webhooks.verify(PAYLOAD, headers, SECRET, now=NOW) is False

    def test_custom_tolerance(self):
        headers = sign(PAYLOAD, timestamp=NOW - 10)
        assert webhooks.verify(PAYLOAD, headers, SECRET, now=NOW, tolerance=5) is False
        assert webhooks.verify(PAYLOAD, headers, SECRET, now=NOW, tolerance=10) is True

    def test_defaults_to_the_current_time(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr("blindpay.webhooks.time.time", lambda: float(NOW + 301))
        assert webhooks.verify(PAYLOAD, sign(PAYLOAD), SECRET) is False
        monkeypatch.setattr("blindpay.webhooks.time.time", lambda: float(NOW + 300))
        assert webhooks.verify(PAYLOAD, sign(PAYLOAD), SECRET) is True

    def test_empty_headers_return_false(self):
        assert webhooks.verify(PAYLOAD, {}, SECRET, now=NOW) is False
