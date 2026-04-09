from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestCustodialWallets:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_create_custodial_wallet(self):
        mocked_wallet = {
            "id": "cw_000000000000",
            "receiver_id": "re_000000000000",
            "instance_id": "in_000000000000",
            "network": "solana",
            "address": "So1ana1234567890",
            "created_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = await self.blindpay.wallets.custodial.create(
                {
                    "receiver_id": "re_000000000000",
                    "network": "solana",
                }
            )

            assert response["error"] is None
            assert response["data"]["id"] == "cw_000000000000"
            assert response["data"]["network"] == "solana"
            assert response["data"]["address"] == "So1ana1234567890"
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_000000000000/wallets",
                {"network": "solana"},
            )

    @pytest.mark.asyncio
    async def test_list_custodial_wallets(self):
        mocked_wallets = [
            {
                "id": "cw_000000000000",
                "receiver_id": "re_000000000000",
                "instance_id": "in_000000000000",
                "network": "solana",
                "address": "So1ana1234567890",
                "created_at": "2025-01-01T00:00:00Z",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallets, "error": None}

            response = await self.blindpay.wallets.custodial.list("re_000000000000")

            assert response["error"] is None
            assert len(response["data"]) == 1
            assert response["data"][0]["id"] == "cw_000000000000"
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/receivers/re_000000000000/wallets")

    @pytest.mark.asyncio
    async def test_get_custodial_wallet(self):
        mocked_wallet = {
            "id": "cw_000000000000",
            "receiver_id": "re_000000000000",
            "instance_id": "in_000000000000",
            "network": "solana",
            "address": "So1ana1234567890",
            "created_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = await self.blindpay.wallets.custodial.get(
                {"receiver_id": "re_000000000000", "id": "cw_000000000000"}
            )

            assert response["error"] is None
            assert response["data"]["id"] == "cw_000000000000"
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/wallets/cw_000000000000"
            )

    @pytest.mark.asyncio
    async def test_get_custodial_wallet_balance(self):
        mocked_balance = {
            "usdc": {
                "amount": 150.50,
                "token": "USDC",
                "address": "So1ana1234567890",
            },
            "usdt": {
                "amount": 0.0,
                "token": "USDT",
                "address": "So1ana1234567890",
            },
            "usdb": None,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_balance, "error": None}

            response = await self.blindpay.wallets.custodial.get_balance(
                {"receiver_id": "re_000000000000", "id": "cw_000000000000"}
            )

            assert response["error"] is None
            assert response["data"]["usdc"]["amount"] == 150.50
            assert response["data"]["usdt"]["amount"] == 0.0
            assert response["data"]["usdb"] is None
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/wallets/cw_000000000000/balance"
            )

    @pytest.mark.asyncio
    async def test_delete_custodial_wallet(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": None, "error": None}

            response = await self.blindpay.wallets.custodial.delete(
                {"receiver_id": "re_000000000000", "id": "cw_000000000000"}
            )

            assert response["error"] is None
            mock_request.assert_called_once_with(
                "DELETE", "/instances/in_000000000000/receivers/re_000000000000/wallets/cw_000000000000", None
            )


class TestCustodialWalletsSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_create_custodial_wallet(self):
        mocked_wallet = {
            "id": "cw_000000000000",
            "receiver_id": "re_000000000000",
            "instance_id": "in_000000000000",
            "network": "solana",
            "address": "So1ana1234567890",
            "created_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = self.blindpay.wallets.custodial.create(
                {
                    "receiver_id": "re_000000000000",
                    "network": "solana",
                }
            )

            assert response["error"] is None
            assert response["data"]["id"] == "cw_000000000000"
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_000000000000/wallets",
                {"network": "solana"},
            )

    def test_list_custodial_wallets(self):
        mocked_wallets = [
            {
                "id": "cw_000000000000",
                "receiver_id": "re_000000000000",
                "instance_id": "in_000000000000",
                "network": "solana",
                "address": "So1ana1234567890",
                "created_at": "2025-01-01T00:00:00Z",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallets, "error": None}

            response = self.blindpay.wallets.custodial.list("re_000000000000")

            assert response["error"] is None
            assert len(response["data"]) == 1
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/receivers/re_000000000000/wallets")

    def test_get_custodial_wallet(self):
        mocked_wallet = {
            "id": "cw_000000000000",
            "receiver_id": "re_000000000000",
            "instance_id": "in_000000000000",
            "network": "solana",
            "address": "So1ana1234567890",
            "created_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = self.blindpay.wallets.custodial.get({"receiver_id": "re_000000000000", "id": "cw_000000000000"})

            assert response["error"] is None
            assert response["data"]["id"] == "cw_000000000000"
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/wallets/cw_000000000000"
            )

    def test_get_custodial_wallet_balance(self):
        mocked_balance = {
            "usdc": {
                "amount": 150.50,
                "token": "USDC",
                "address": "So1ana1234567890",
            },
            "usdt": {
                "amount": 0.0,
                "token": "USDT",
                "address": "So1ana1234567890",
            },
            "usdb": None,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_balance, "error": None}

            response = self.blindpay.wallets.custodial.get_balance(
                {"receiver_id": "re_000000000000", "id": "cw_000000000000"}
            )

            assert response["error"] is None
            assert response["data"]["usdc"]["amount"] == 150.50
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/wallets/cw_000000000000/balance"
            )

    def test_delete_custodial_wallet(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": None, "error": None}

            response = self.blindpay.wallets.custodial.delete(
                {"receiver_id": "re_000000000000", "id": "cw_000000000000"}
            )

            assert response["error"] is None
            mock_request.assert_called_once_with(
                "DELETE", "/instances/in_000000000000/receivers/re_000000000000/wallets/cw_000000000000", None
            )
