from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestVirtualAccounts:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_update_virtual_account(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = await self.blindpay.virtual_accounts.update(
                {
                    "receiver_id": "re_000000000000",
                    "blockchain_wallet_id": "bw_000000000000",
                    "token": "USDC",
                }
            )

            assert response["error"] is None
            assert response["data"] == {"data": None}
            mock_request.assert_called_once_with(
                "PUT",
                "/instances/in_000000000000/receivers/re_000000000000/virtual-accounts",
                {"blockchain_wallet_id": "bw_000000000000", "token": "USDC"},
            )

    @pytest.mark.asyncio
    async def test_create_virtual_account(self):
        mocked_virtual_account = {
            "id": "va_000000000000",
            "us": {
                "ach": {
                    "routing_number": "123456789",
                    "account_number": "123456789",
                },
                "wire": {
                    "routing_number": "123456789",
                    "account_number": "123456789",
                },
                "rtp": {
                    "routing_number": "123456789",
                    "account_number": "123456789",
                },
                "swift_bic_code": "CHASUS33",
                "account_type": "Business checking",
                "beneficiary": {
                    "name": "Receiver Name",
                    "address_line_1": "8 The Green",
                    "address_line_2": "Dover, DE 19901",
                },
                "receiving_bank": {
                    "name": "JPMorgan Chase",
                    "address_line_1": "270 Park Ave",
                    "address_line_2": "New York, NY, 10017-2070",
                },
            },
            "token": "USDC",
            "blockchain_wallet_id": "bw_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_virtual_account, "error": None}

            response = await self.blindpay.virtual_accounts.create(
                {
                    "receiver_id": "re_000000000000",
                    "blockchain_wallet_id": "bw_000000000000",
                    "token": "USDC",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_virtual_account
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_000000000000/virtual-accounts",
                {"blockchain_wallet_id": "bw_000000000000", "token": "USDC"},
            )

    @pytest.mark.asyncio
    async def test_get_virtual_account(self):
        mocked_virtual_account = {
            "id": "va_000000000000",
            "us": {
                "ach": {
                    "routing_number": "123456789",
                    "account_number": "123456789",
                },
                "wire": {
                    "routing_number": "123456789",
                    "account_number": "123456789",
                },
                "rtp": {
                    "routing_number": "123456789",
                    "account_number": "123456789",
                },
                "swift_bic_code": "CHASUS33",
                "account_type": "Business checking",
                "beneficiary": {
                    "name": "Receiver Name",
                    "address_line_1": "8 The Green",
                    "address_line_2": "Dover, DE 19901",
                },
                "receiving_bank": {
                    "name": "JPMorgan Chase",
                    "address_line_1": "270 Park Ave",
                    "address_line_2": "New York, NY, 10017-2070",
                },
            },
            "token": "USDC",
            "blockchain_wallet_id": "bw_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_virtual_account, "error": None}

            response = await self.blindpay.virtual_accounts.get("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_virtual_account
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/virtual-accounts"
            )


class TestVirtualAccountsSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_update_virtual_account(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = self.blindpay.virtual_accounts.update(
                {
                    "receiver_id": "re_000000000000",
                    "blockchain_wallet_id": "bw_000000000000",
                    "token": "USDC",
                }
            )

            assert response["error"] is None
            assert response["data"] == {"data": None}
            mock_request.assert_called_once_with(
                "PUT",
                "/instances/in_000000000000/receivers/re_000000000000/virtual-accounts",
                {"blockchain_wallet_id": "bw_000000000000", "token": "USDC"},
            )

    def test_create_virtual_account(self):
        mocked_virtual_account = {
            "id": "va_000000000000",
            "us": {
                "ach": {
                    "routing_number": "123456789",
                    "account_number": "123456789",
                },
                "wire": {
                    "routing_number": "123456789",
                    "account_number": "123456789",
                },
                "rtp": {
                    "routing_number": "123456789",
                    "account_number": "123456789",
                },
                "swift_bic_code": "CHASUS33",
                "account_type": "Business checking",
                "beneficiary": {
                    "name": "Receiver Name",
                    "address_line_1": "8 The Green",
                    "address_line_2": "Dover, DE 19901",
                },
                "receiving_bank": {
                    "name": "JPMorgan Chase",
                    "address_line_1": "270 Park Ave",
                    "address_line_2": "New York, NY, 10017-2070",
                },
            },
            "token": "USDC",
            "blockchain_wallet_id": "bw_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_virtual_account, "error": None}

            response = self.blindpay.virtual_accounts.create(
                {
                    "receiver_id": "re_000000000000",
                    "blockchain_wallet_id": "bw_000000000000",
                    "token": "USDC",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_virtual_account
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_000000000000/virtual-accounts",
                {"blockchain_wallet_id": "bw_000000000000", "token": "USDC"},
            )

    def test_get_virtual_account(self):
        mocked_virtual_account = {
            "id": "va_000000000000",
            "us": {
                "ach": {
                    "routing_number": "123456789",
                    "account_number": "123456789",
                },
                "wire": {
                    "routing_number": "123456789",
                    "account_number": "123456789",
                },
                "rtp": {
                    "routing_number": "123456789",
                    "account_number": "123456789",
                },
                "swift_bic_code": "CHASUS33",
                "account_type": "Business checking",
                "beneficiary": {
                    "name": "Receiver Name",
                    "address_line_1": "8 The Green",
                    "address_line_2": "Dover, DE 19901",
                },
                "receiving_bank": {
                    "name": "JPMorgan Chase",
                    "address_line_1": "270 Park Ave",
                    "address_line_2": "New York, NY, 10017-2070",
                },
            },
            "token": "USDC",
            "blockchain_wallet_id": "bw_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_virtual_account, "error": None}

            response = self.blindpay.virtual_accounts.get("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_virtual_account
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/virtual-accounts"
            )
