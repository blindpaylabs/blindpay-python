from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestOfframpWallets:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_list_offramp_wallets(self):
        mocked_offramp_wallets = [
            {
                "id": "ow_000000000000",
                "external_id": "your_external_id",
                "instance_id": "in_000000000000",
                "receiver_id": "re_000000000000",
                "bank_account_id": "ba_000000000000",
                "network": "tron",
                "address": "TALJN9zTTEL9TVBb4WuTt6wLvPqJZr3hvb",
                "created_at": "2021-01-01T00:00:00Z",
                "updated_at": "2021-01-01T00:00:00Z",
            }
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_offramp_wallets, "error": None}

            response = await self.blindpay.wallets.offramp.list(
                {
                    "receiver_id": "re_000000000000",
                    "bank_account_id": "ba_000000000000",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_offramp_wallets
            mock_request.assert_called_once_with(
                "GET",
                "/instances/in_000000000000/receivers/re_000000000000/bank-accounts/ba_000000000000/offramp-wallets",
            )

    @pytest.mark.asyncio
    async def test_create_offramp_wallet(self):
        mocked_offramp_wallet = {
            "id": "ow_000000000000",
            "external_id": "your_external_id",
            "network": "tron",
            "address": "TALJN9zTTEL9TVBb4WuTt6wLvPqJZr3hvb",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_offramp_wallet, "error": None}

            response = await self.blindpay.wallets.offramp.create(
                {
                    "external_id": "your_external_id",
                    "network": "tron",
                    "receiver_id": "re_000000000000",
                    "bank_account_id": "ba_000000000000",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_offramp_wallet
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_000000000000/bank-accounts/ba_000000000000/offramp-wallets",
                {
                    "external_id": "your_external_id",
                    "network": "tron",
                },
            )

    @pytest.mark.asyncio
    async def test_get_offramp_wallet(self):
        mocked_offramp_wallet = {
            "id": "ow_000000000000",
            "external_id": "your_external_id",
            "instance_id": "in_000000000000",
            "receiver_id": "re_000000000000",
            "bank_account_id": "ba_000000000000",
            "network": "tron",
            "address": "TALJN9zTTEL9TVBb4WuTt6wLvPqJZr3hvb",
            "created_at": "2021-01-01T00:00:00Z",
            "updated_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_offramp_wallet, "error": None}

            response = await self.blindpay.wallets.offramp.get(
                {
                    "id": "ow_000000000000",
                    "bank_account_id": "ba_000000000000",
                    "receiver_id": "re_000000000000",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_offramp_wallet
            mock_request.assert_called_once_with(
                "GET",
                "/instances/in_000000000000/receivers/re_000000000000/bank-accounts/ba_000000000000/offramp-wallets/ow_000000000000",
            )


class TestOfframpWalletsSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_list_offramp_wallets(self):
        mocked_offramp_wallets = [
            {
                "id": "ow_000000000000",
                "external_id": "your_external_id",
                "instance_id": "in_000000000000",
                "receiver_id": "re_000000000000",
                "bank_account_id": "ba_000000000000",
                "network": "tron",
                "address": "TALJN9zTTEL9TVBb4WuTt6wLvPqJZr3hvb",
                "created_at": "2021-01-01T00:00:00Z",
                "updated_at": "2021-01-01T00:00:00Z",
            }
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_offramp_wallets, "error": None}

            response = self.blindpay.wallets.offramp.list(
                {
                    "receiver_id": "re_000000000000",
                    "bank_account_id": "ba_000000000000",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_offramp_wallets
            mock_request.assert_called_once_with(
                "GET",
                "/instances/in_000000000000/receivers/re_000000000000/bank-accounts/ba_000000000000/offramp-wallets",
            )

    def test_create_offramp_wallet(self):
        mocked_offramp_wallet = {
            "id": "ow_000000000000",
            "external_id": "your_external_id",
            "network": "tron",
            "address": "TALJN9zTTEL9TVBb4WuTt6wLvPqJZr3hvb",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_offramp_wallet, "error": None}

            response = self.blindpay.wallets.offramp.create(
                {
                    "external_id": "your_external_id",
                    "network": "tron",
                    "receiver_id": "re_000000000000",
                    "bank_account_id": "ba_000000000000",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_offramp_wallet
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_000000000000/bank-accounts/ba_000000000000/offramp-wallets",
                {
                    "external_id": "your_external_id",
                    "network": "tron",
                },
            )

    def test_get_offramp_wallet(self):
        mocked_offramp_wallet = {
            "id": "ow_000000000000",
            "external_id": "your_external_id",
            "instance_id": "in_000000000000",
            "receiver_id": "re_000000000000",
            "bank_account_id": "ba_000000000000",
            "network": "tron",
            "address": "TALJN9zTTEL9TVBb4WuTt6wLvPqJZr3hvb",
            "created_at": "2021-01-01T00:00:00Z",
            "updated_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_offramp_wallet, "error": None}

            response = self.blindpay.wallets.offramp.get(
                {
                    "id": "ow_000000000000",
                    "bank_account_id": "ba_000000000000",
                    "receiver_id": "re_000000000000",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_offramp_wallet
            mock_request.assert_called_once_with(
                "GET",
                "/instances/in_000000000000/receivers/re_000000000000/bank-accounts/ba_000000000000/offramp-wallets/ow_000000000000",
            )
