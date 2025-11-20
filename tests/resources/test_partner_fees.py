from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestPartnerFees:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_list_partner_fees(self):
        mocked_list = [
            {
                "id": "fe_000000000000",
                "instance_id": "in_000000000000",
                "name": "Display Name",
                "payout_percentage_fee": 0,
                "payout_flat_fee": 0,
                "payin_percentage_fee": 0,
                "payin_flat_fee": 0,
                "evm_wallet_address": "0x1234567890123456789012345678901234567890",
                "stellar_wallet_address": "GAB22222222222222222222222222222222222222222222222222222222222222",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_list, "error": None}

            response = await self.blindpay.partner_fees.list()

            assert response["error"] is None
            assert response["data"] == mocked_list

    @pytest.mark.asyncio
    async def test_create_partner_fee(self):
        mock_partner_fee = {
            "id": "fe_000000000000",
            "instance_id": "in_000000000000",
            "name": "Display Name",
            "payout_percentage_fee": 0,
            "payout_flat_fee": 0,
            "payin_percentage_fee": 0,
            "payin_flat_fee": 0,
            "evm_wallet_address": "0x1234567890123456789012345678901234567890",
            "stellar_wallet_address": "GAB22222222222222222222222222222222222222222222222222222222222222",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mock_partner_fee, "error": None}

            response = await self.blindpay.partner_fees.create(
                {
                    "name": "Display Name",
                    "payout_percentage_fee": 0,
                    "payout_flat_fee": 0,
                    "payin_percentage_fee": 0,
                    "payin_flat_fee": 0,
                    "evm_wallet_address": "0x1234567890123456789012345678901234567890",
                    "stellar_wallet_address": "GAB22222222222222222222222222222222222222222222222222222222222222",
                    "virtual_account_set": False,
                }
            )

            assert response["error"] is None
            assert response["data"] == mock_partner_fee

    @pytest.mark.asyncio
    async def test_get_partner_fee(self):
        mocked_fee = {
            "id": "fe_000000000000",
            "instance_id": "in_000000000000",
            "name": "Display Name",
            "payout_percentage_fee": 0,
            "payout_flat_fee": 0,
            "payin_percentage_fee": 0,
            "payin_flat_fee": 0,
            "evm_wallet_address": "0x1234567890123456789012345678901234567890",
            "stellar_wallet_address": "GAB22222222222222222222222222222222222222222222222222222222222222",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_fee, "error": None}

            response = await self.blindpay.partner_fees.get("fe_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_fee

    @pytest.mark.asyncio
    async def test_delete_partner_fee(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = await self.blindpay.partner_fees.delete("fe_000000000000")

            assert response["error"] is None
            assert response["data"] == {"data": None}


class TestPartnerFeesSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_list_partner_fees(self):
        mocked_list = [
            {
                "id": "fe_000000000000",
                "instance_id": "in_000000000000",
                "name": "Display Name",
                "payout_percentage_fee": 0,
                "payout_flat_fee": 0,
                "payin_percentage_fee": 0,
                "payin_flat_fee": 0,
                "evm_wallet_address": "0x1234567890123456789012345678901234567890",
                "stellar_wallet_address": "GAB22222222222222222222222222222222222222222222222222222222222222",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_list, "error": None}

            response = self.blindpay.partner_fees.list()

            assert response["error"] is None
            assert response["data"] == mocked_list

    def test_create_partner_fee(self):
        mock_partner_fee = {
            "id": "fe_000000000000",
            "instance_id": "in_000000000000",
            "name": "Display Name",
            "payout_percentage_fee": 0,
            "payout_flat_fee": 0,
            "payin_percentage_fee": 0,
            "payin_flat_fee": 0,
            "evm_wallet_address": "0x1234567890123456789012345678901234567890",
            "stellar_wallet_address": "GAB22222222222222222222222222222222222222222222222222222222222222",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mock_partner_fee, "error": None}

            response = self.blindpay.partner_fees.create(
                {
                    "name": "Display Name",
                    "payout_percentage_fee": 0,
                    "payout_flat_fee": 0,
                    "payin_percentage_fee": 0,
                    "payin_flat_fee": 0,
                    "evm_wallet_address": "0x1234567890123456789012345678901234567890",
                    "stellar_wallet_address": "GAB22222222222222222222222222222222222222222222222222222222222222",
                    "virtual_account_set": False,
                }
            )

            assert response["error"] is None
            assert response["data"] == mock_partner_fee

    def test_get_partner_fee(self):
        mocked_fee = {
            "id": "fe_000000000000",
            "instance_id": "in_000000000000",
            "name": "Display Name",
            "payout_percentage_fee": 0,
            "payout_flat_fee": 0,
            "payin_percentage_fee": 0,
            "payin_flat_fee": 0,
            "evm_wallet_address": "0x1234567890123456789012345678901234567890",
            "stellar_wallet_address": "GAB22222222222222222222222222222222222222222222222222222222222222",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_fee, "error": None}

            response = self.blindpay.partner_fees.get("fe_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_fee

    def test_delete_partner_fee(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = self.blindpay.partner_fees.delete("fe_000000000000")

            assert response["error"] is None
            assert response["data"] == {"data": None}
