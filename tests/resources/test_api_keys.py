from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestApiKeys:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_create_api_key(self):
        mocked_api_key = {
            "id": "ap_000000000000",
            "token": "token",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_api_key, "error": None}

            response = await self.blindpay.instances.api_keys.create(
                {
                    "name": "test",
                    "permission": "full_access",
                    "ip_whitelist": [],
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_api_key
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/api-keys",
                {"name": "test", "permission": "full_access", "ip_whitelist": []},
            )

    @pytest.mark.asyncio
    async def test_get_api_key(self):
        mocked_api_key = {
            "id": "ap_000000000000",
            "token": "token",
            "name": "test",
            "permission": "full_access",
            "ip_whitelist": ["127.0.0.1"],
            "unkey_id": "key_123456789",
            "last_used_at": "2024-01-01T00:00:00.000Z",
            "instance_id": "in_000000000000",
            "created_at": "2021-01-01",
            "updated_at": "2021-01-01",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_api_key, "error": None}

            response = await self.blindpay.instances.api_keys.get("ap_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_api_key
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/api-keys/ap_000000000000")

    @pytest.mark.asyncio
    async def test_list_api_keys(self):
        mocked_api_keys = [
            {
                "id": "ap_000000000000",
                "token": "token",
                "name": "test",
                "permission": "full_access",
                "ip_whitelist": ["127.0.0.1"],
                "unkey_id": "key_123456789",
                "last_used_at": "2024-01-01T00:00:00.000Z",
                "instance_id": "in_000000000000",
                "created_at": "2021-01-01",
                "updated_at": "2021-01-01",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_api_keys, "error": None}

            response = await self.blindpay.instances.api_keys.list()

            assert response["error"] is None
            assert response["data"] == mocked_api_keys
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/api-keys")

    @pytest.mark.asyncio
    async def test_delete_api_key(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = await self.blindpay.instances.api_keys.delete("ap_000000000000")

            assert response["error"] is None
            assert response["data"] == {"data": None}
            mock_request.assert_called_once_with("DELETE", "/instances/in_000000000000/api-keys/ap_000000000000", None)


class TestApiKeysSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_create_api_key(self):
        mocked_api_key = {
            "id": "ap_000000000000",
            "token": "token",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_api_key, "error": None}

            response = self.blindpay.instances.api_keys.create(
                {
                    "name": "test",
                    "permission": "full_access",
                    "ip_whitelist": [],
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_api_key
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/api-keys",
                {"name": "test", "permission": "full_access", "ip_whitelist": []},
            )

    def test_get_api_key(self):
        mocked_api_key = {
            "id": "ap_000000000000",
            "token": "token",
            "name": "test",
            "permission": "full_access",
            "ip_whitelist": ["127.0.0.1"],
            "unkey_id": "key_123456789",
            "last_used_at": "2024-01-01T00:00:00.000Z",
            "instance_id": "in_000000000000",
            "created_at": "2021-01-01",
            "updated_at": "2021-01-01",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_api_key, "error": None}

            response = self.blindpay.instances.api_keys.get("ap_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_api_key
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/api-keys/ap_000000000000")

    def test_list_api_keys(self):
        mocked_api_keys = [
            {
                "id": "ap_000000000000",
                "token": "token",
                "name": "test",
                "permission": "full_access",
                "ip_whitelist": ["127.0.0.1"],
                "unkey_id": "key_123456789",
                "last_used_at": "2024-01-01T00:00:00.000Z",
                "instance_id": "in_000000000000",
                "created_at": "2021-01-01",
                "updated_at": "2021-01-01",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_api_keys, "error": None}

            response = self.blindpay.instances.api_keys.list()

            assert response["error"] is None
            assert response["data"] == mocked_api_keys
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/api-keys")

    def test_delete_api_key(self):
        """Test deleting an API key."""
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = self.blindpay.instances.api_keys.delete("ap_000000000000")

            assert response["error"] is None
            assert response["data"] == {"data": None}
            mock_request.assert_called_once_with("DELETE", "/instances/in_000000000000/api-keys/ap_000000000000", None)
