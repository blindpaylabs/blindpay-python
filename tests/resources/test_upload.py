from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestUpload:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_create(self):
        mocked_data = {"url": "https://example.com/upload/image.png"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_data, "error": None}

            response = await self.blindpay.upload.create({"bucket": "avatar", "file": "base64data"})

            assert response["error"] is None
            assert response["data"] == mocked_data
            mock_request.assert_called_once_with("POST", "/upload", {"bucket": "avatar", "file": "base64data"})


class TestUploadSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_create(self):
        mocked_data = {"url": "https://example.com/upload/image.png"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_data, "error": None}

            response = self.blindpay.upload.create({"bucket": "avatar", "file": "base64data"})

            assert response["error"] is None
            assert response["data"] == mocked_data
            mock_request.assert_called_once_with("POST", "/upload", {"bucket": "avatar", "file": "base64data"})
