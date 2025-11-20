from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestInstances:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_get_instance_members(self):
        mocked_members = [
            {
                "id": "us_000000000000",
                "email": "email@example.com",
                "first_name": "Harry",
                "middle_name": "James",
                "last_name": "Potter",
                "image_url": "https://example.com/image.png",
                "created_at": "2021-01-01T00:00:00Z",
                "role": "admin",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_members, "error": None}

            response = await self.blindpay.instances.get_members()

            assert response["error"] is None
            assert response["data"] == mocked_members

    @pytest.mark.asyncio
    async def test_update_instance(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = await self.blindpay.instances.update(
                {
                    "name": "New Instance Name",
                }
            )

            assert response["error"] is None
            assert response["data"] == {"data": None}

    @pytest.mark.asyncio
    async def test_delete_instance(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = await self.blindpay.instances.delete()

            assert response["error"] is None
            assert response["data"] == {"data": None}

    @pytest.mark.asyncio
    async def test_delete_instance_member(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = await self.blindpay.instances.delete_member("us_000000000000")

            assert response["error"] is None
            assert response["data"] == {"data": None}

    @pytest.mark.asyncio
    async def test_update_instance_member_role(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = await self.blindpay.instances.update_member_role("us_000000000000", "checker")

            assert response["error"] is None
            assert response["data"] == {"data": None}


class TestInstancesSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_get_instance_members(self):
        mocked_members = [
            {
                "id": "us_000000000000",
                "email": "email@example.com",
                "first_name": "Harry",
                "middle_name": "James",
                "last_name": "Potter",
                "image_url": "https://example.com/image.png",
                "created_at": "2021-01-01T00:00:00Z",
                "role": "admin",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_members, "error": None}

            response = self.blindpay.instances.get_members()

            assert response["error"] is None
            assert response["data"] == mocked_members

    def test_update_instance(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = self.blindpay.instances.update(
                {
                    "name": "New Instance Name",
                }
            )

            assert response["error"] is None
            assert response["data"] == {"data": None}

    def test_delete_instance(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = self.blindpay.instances.delete()

            assert response["error"] is None
            assert response["data"] == {"data": None}

    def test_delete_instance_member(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = self.blindpay.instances.delete_member("us_000000000000")

            assert response["error"] is None
            assert response["data"] == {"data": None}

    def test_update_instance_member_role(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = self.blindpay.instances.update_member_role("us_000000000000", "checker")

            assert response["error"] is None
            assert response["data"] == {"data": None}
