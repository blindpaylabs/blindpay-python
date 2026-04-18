from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestTermsOfService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_initiate_terms_of_service(self):
        mocked_url = {
            "url": "https://app.blindpay.com/e/terms-of-service?session_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_url, "error": None}

            response = await self.blindpay.instances.terms_of_service.initiate(
                {
                    "idempotency_key": "123e4567-e89b-12d3-a456-426614174000",
                    "receiver_id": None,
                    "redirect_url": None,
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_url
            mock_request.assert_called_once_with(
                "POST",
                "/e/instances/in_000000000000/tos",
                {
                    "idempotency_key": "123e4567-e89b-12d3-a456-426614174000",
                    "receiver_id": None,
                    "redirect_url": None,
                },
            )


class TestTermsOfServiceSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_initiate_terms_of_service(self):
        mocked_url = {
            "url": "https://app.blindpay.com/e/terms-of-service?session_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_url, "error": None}

            response = self.blindpay.instances.terms_of_service.initiate(
                {
                    "idempotency_key": "123e4567-e89b-12d3-a456-426614174000",
                    "receiver_id": None,
                    "redirect_url": None,
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_url
            mock_request.assert_called_once_with(
                "POST",
                "/e/instances/in_000000000000/tos",
                {
                    "idempotency_key": "123e4567-e89b-12d3-a456-426614174000",
                    "receiver_id": None,
                    "redirect_url": None,
                },
            )
