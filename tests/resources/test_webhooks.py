from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestWebhookEndpoints:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_create_webhook_endpoint(self):
        mocked_webhook_endpoint = {
            "id": "we_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_webhook_endpoint, "error": None}

            response = await self.blindpay.instances.webhook_endpoints.create(
                {
                    "url": "https://example.com/webhook",
                    "events": ["receiver.new"],
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_webhook_endpoint
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/webhook-endpoints",
                {"url": "https://example.com/webhook", "events": ["receiver.new"]},
            )

    @pytest.mark.asyncio
    async def test_list_webhook_endpoints(self):
        mocked_webhook_endpoints = [
            {
                "id": "we_000000000000",
                "url": "https://example.com/webhook",
                "events": ["receiver.new"],
                "last_event_at": "2024-01-01T00:00:00.000Z",
                "instance_id": "in_000000000000",
                "created_at": "2021-01-01T00:00:00Z",
                "updated_at": "2021-01-01T00:00:00Z",
            }
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_webhook_endpoints, "error": None}

            response = await self.blindpay.instances.webhook_endpoints.list()

            assert response["error"] is None
            assert response["data"] == mocked_webhook_endpoints
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/webhook-endpoints")

    @pytest.mark.asyncio
    async def test_delete_webhook_endpoint(self):
        mocked_response = {"data": None}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_response, "error": None}

            response = await self.blindpay.instances.webhook_endpoints.delete("we_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_response
            mock_request.assert_called_once_with(
                "DELETE", "/instances/in_000000000000/webhook-endpoints/we_000000000000", None
            )

    @pytest.mark.asyncio
    async def test_get_webhook_secret(self):
        mocked_webhook_secret = {"key": "whsec_000000000000"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_webhook_secret, "error": None}

            response = await self.blindpay.instances.webhook_endpoints.get_secret("we_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_webhook_secret
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/webhook-endpoints/we_000000000000/secret"
            )

    @pytest.mark.asyncio
    async def test_get_portal_access_url(self):
        mocked_webhook_url = {"url": "https://example.com/webhook"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_webhook_url, "error": None}

            response = await self.blindpay.instances.webhook_endpoints.get_portal_access_url()

            assert response["error"] is None
            assert response["data"] == mocked_webhook_url
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/webhook-endpoints/portal-access")


class TestWebhookEndpointsSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_create_webhook_endpoint(self):
        mocked_webhook_endpoint = {
            "id": "we_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_webhook_endpoint, "error": None}

            response = self.blindpay.instances.webhook_endpoints.create(
                {
                    "url": "https://example.com/webhook",
                    "events": ["receiver.new"],
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_webhook_endpoint
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/webhook-endpoints",
                {"url": "https://example.com/webhook", "events": ["receiver.new"]},
            )

    def test_list_webhook_endpoints(self):
        mocked_webhook_endpoints = [
            {
                "id": "we_000000000000",
                "url": "https://example.com/webhook",
                "events": ["receiver.new"],
                "last_event_at": "2024-01-01T00:00:00.000Z",
                "instance_id": "in_000000000000",
                "created_at": "2021-01-01T00:00:00Z",
                "updated_at": "2021-01-01T00:00:00Z",
            }
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_webhook_endpoints, "error": None}

            response = self.blindpay.instances.webhook_endpoints.list()

            assert response["error"] is None
            assert response["data"] == mocked_webhook_endpoints
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/webhook-endpoints")

    def test_delete_webhook_endpoint(self):
        mocked_response = {"data": None}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_response, "error": None}

            response = self.blindpay.instances.webhook_endpoints.delete("we_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_response
            mock_request.assert_called_once_with(
                "DELETE", "/instances/in_000000000000/webhook-endpoints/we_000000000000", None
            )

    def test_get_webhook_secret(self):
        mocked_webhook_secret = {"key": "whsec_000000000000"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_webhook_secret, "error": None}

            response = self.blindpay.instances.webhook_endpoints.get_secret("we_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_webhook_secret
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/webhook-endpoints/we_000000000000/secret"
            )

    def test_get_portal_access_url(self):
        mocked_webhook_url = {"url": "https://example.com/webhook"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_webhook_url, "error": None}

            response = self.blindpay.instances.webhook_endpoints.get_portal_access_url()

            assert response["error"] is None
            assert response["data"] == mocked_webhook_url
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/webhook-endpoints/portal-access")
