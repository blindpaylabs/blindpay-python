from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestSandbox:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_list(self):
        mocked_data = [{"id": "sb_000000000000", "name": "My Sandbox Item", "status": "active"}]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_data, "error": None}

            response = await self.blindpay.sandbox.list()

            assert response["error"] is None
            assert response["data"] == mocked_data
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/sandbox")

    @pytest.mark.asyncio
    async def test_get(self):
        mocked_data = {"id": "sb_000000000000", "name": "My Sandbox Item", "status": "active"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_data, "error": None}

            response = await self.blindpay.sandbox.get("sb_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_data
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/sandbox/sb_000000000000")

    @pytest.mark.asyncio
    async def test_create(self):
        mocked_data = {"id": "sb_000000000000", "name": "My Sandbox Item", "status": "active"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_data, "error": None}

            response = await self.blindpay.sandbox.create({"name": "My Sandbox Item"})

            assert response["error"] is None
            assert response["data"] == mocked_data
            mock_request.assert_called_once_with("POST", "/instances/in_000000000000/sandbox", {"name": "My Sandbox Item"})

    @pytest.mark.asyncio
    async def test_update(self):
        mocked_data = {"id": "sb_000000000000", "name": "Updated Name", "status": "active"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_data, "error": None}

            response = await self.blindpay.sandbox.update({"sandbox_id": "sb_000000000000", "name": "Updated Name"})

            assert response["error"] is None
            assert response["data"] == mocked_data
            mock_request.assert_called_once_with(
                "PATCH", "/instances/in_000000000000/sandbox/sb_000000000000", {"name": "Updated Name"}
            )

    @pytest.mark.asyncio
    async def test_delete(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": None, "error": None}

            response = await self.blindpay.sandbox.delete("sb_000000000000")

            assert response["error"] is None
            mock_request.assert_called_once_with("DELETE", "/instances/in_000000000000/sandbox/sb_000000000000", None)


class TestSandboxSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_list(self):
        mocked_data = [{"id": "sb_000000000000", "name": "My Sandbox Item", "status": "active"}]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_data, "error": None}

            response = self.blindpay.sandbox.list()

            assert response["error"] is None
            assert response["data"] == mocked_data
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/sandbox")

    def test_get(self):
        mocked_data = {"id": "sb_000000000000", "name": "My Sandbox Item", "status": "active"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_data, "error": None}

            response = self.blindpay.sandbox.get("sb_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_data
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/sandbox/sb_000000000000")

    def test_create(self):
        mocked_data = {"id": "sb_000000000000", "name": "My Sandbox Item", "status": "active"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_data, "error": None}

            response = self.blindpay.sandbox.create({"name": "My Sandbox Item"})

            assert response["error"] is None
            assert response["data"] == mocked_data
            mock_request.assert_called_once_with("POST", "/instances/in_000000000000/sandbox", {"name": "My Sandbox Item"})

    def test_update(self):
        mocked_data = {"id": "sb_000000000000", "name": "Updated Name", "status": "active"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_data, "error": None}

            response = self.blindpay.sandbox.update({"sandbox_id": "sb_000000000000", "name": "Updated Name"})

            assert response["error"] is None
            assert response["data"] == mocked_data
            mock_request.assert_called_once_with(
                "PATCH", "/instances/in_000000000000/sandbox/sb_000000000000", {"name": "Updated Name"}
            )

    def test_delete(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": None, "error": None}

            response = self.blindpay.sandbox.delete("sb_000000000000")

            assert response["error"] is None
            mock_request.assert_called_once_with("DELETE", "/instances/in_000000000000/sandbox/sb_000000000000", None)
