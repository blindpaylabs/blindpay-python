from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestFees:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_get_fees(self):
        mocked_fees = {
            "ach": {
                "payin_flat": 0.0,
                "payin_percentage": 0.0,
                "payout_flat": 5.0,
                "payout_percentage": 0.0,
            },
            "domestic_wire": {
                "payin_flat": 0.0,
                "payin_percentage": 0.0,
                "payout_flat": 25.0,
                "payout_percentage": 0.0,
            },
            "pix": {
                "payin_flat": 0.0,
                "payin_percentage": 0.0,
                "payout_flat": 3.0,
                "payout_percentage": 0.5,
            },
            "solana": None,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_fees, "error": None}

            response = await self.blindpay.fees.get()

            assert response["error"] is None
            assert response["data"] is not None
            assert response["data"]["ach"] is not None
            assert response["data"]["ach"]["payout_flat"] == 5.0
            assert response["data"]["domestic_wire"] is not None
            assert response["data"]["domestic_wire"]["payout_flat"] == 25.0
            assert response["data"]["pix"] is not None
            assert response["data"]["pix"]["payout_flat"] == 3.0
            assert response["data"]["pix"]["payout_percentage"] == 0.5
            assert response["data"]["solana"] is None
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/billing/fees")


class TestFeesSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_get_fees(self):
        mocked_fees = {
            "ach": {
                "payin_flat": 0.0,
                "payin_percentage": 0.0,
                "payout_flat": 5.0,
                "payout_percentage": 0.0,
            },
            "domestic_wire": {
                "payin_flat": 0.0,
                "payin_percentage": 0.0,
                "payout_flat": 25.0,
                "payout_percentage": 0.0,
            },
            "pix": {
                "payin_flat": 0.0,
                "payin_percentage": 0.0,
                "payout_flat": 3.0,
                "payout_percentage": 0.5,
            },
            "solana": None,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_fees, "error": None}

            response = self.blindpay.fees.get()

            assert response["error"] is None
            assert response["data"] is not None
            assert response["data"]["ach"] is not None
            assert response["data"]["ach"]["payout_flat"] == 5.0
            assert response["data"]["solana"] is None
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/billing/fees")
