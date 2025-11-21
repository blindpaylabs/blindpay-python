import base64
import hashlib
import hmac

from blindpay import BlindPay, BlindPaySync


class TestBlindPayClient:
    def test_verify_webhook_signature_valid(self):
        client = BlindPay(api_key="test-key", instance_id="in_000000000000")

        secret_key = b"test_secret_key_1234"  # Must be properly encoded
        secret = "whsec_" + base64.b64encode(secret_key).decode()
        webhook_id = "msg_123456"
        timestamp = "1614556800"
        payload = '{"event":"receiver.new","data":{"id":"rec_000000000000"}}'

        signed_content = f"{webhook_id}.{timestamp}.{payload}"
        expected_signature = base64.b64encode(
            hmac.new(secret_key, signed_content.encode(), hashlib.sha256).digest()
        ).decode()

        is_valid = client.verify_webhook_signature(
            secret=secret, id=webhook_id, timestamp=timestamp, payload=payload, svix_signature=expected_signature
        )

        assert is_valid is True

    def test_verify_webhook_signature_invalid(self):
        client = BlindPay(api_key="test-key", instance_id="in_000000000000")

        secret = "whsec_" + base64.b64encode(b"test_secret_key_1234").decode()
        webhook_id = "msg_123456"
        timestamp = "1614556800"
        payload = '{"event":"receiver.new","data":{"id":"rec_000000000000"}}'
        invalid_signature = "invalid_signature_value"

        is_valid = client.verify_webhook_signature(
            secret=secret, id=webhook_id, timestamp=timestamp, payload=payload, svix_signature=invalid_signature
        )

        assert is_valid is False


class TestBlindPaySyncClient:
    def test_sync_client_verify_webhook_signature(self):
        """Test webhook signature verification in sync client with valid signature."""
        client = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

        secret_key = b"test_secret_key_1234"  # Must be properly encoded
        secret = "whsec_" + base64.b64encode(secret_key).decode()
        webhook_id = "msg_123456"
        timestamp = "1614556800"
        payload = '{"event":"receiver.new","data":{"id":"rec_000000000000"}}'

        signed_content = f"{webhook_id}.{timestamp}.{payload}"
        expected_signature = base64.b64encode(
            hmac.new(secret_key, signed_content.encode(), hashlib.sha256).digest()
        ).decode()

        is_valid = client.verify_webhook_signature(
            secret=secret, id=webhook_id, timestamp=timestamp, payload=payload, svix_signature=expected_signature
        )

        assert is_valid is True

    def test_sync_client_verify_webhook_signature_invalid(self):
        """Test webhook signature verification in sync client with invalid signature."""
        client = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

        secret = "whsec_" + base64.b64encode(b"test_secret_key_1234").decode()
        webhook_id = "msg_123456"
        timestamp = "1614556800"
        payload = '{"event":"receiver.new","data":{"id":"rec_000000000000"}}'
        invalid_signature = "invalid_signature_value"

        is_valid = client.verify_webhook_signature(
            secret=secret, id=webhook_id, timestamp=timestamp, payload=payload, svix_signature=invalid_signature
        )

        assert is_valid is False
