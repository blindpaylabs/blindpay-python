from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync
from blindpay.resources.custodial_wallets import CustodialWalletBalance
from tests.spec_fixtures import assert_matches_spec, response_variants

# The API keys balances by uppercase token symbol (USDC/USDT/USDB, plus EURC/EURB where held).
BALANCE = response_variants("GET /v1/instances/{instance_id}/customers/{customer_id}/wallets/{id}/balance")
BALANCE_PATH = "/instances/in_000000000000/customers/cu_000000000000/wallets/wa_000000000000/balance"


class TestCustodialWallets:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_create_custodial_wallet(self):
        mocked_wallet = {
            "id": "cw_000000000000",
            "customer_id": "re_000000000000",
            "instance_id": "in_000000000000",
            "network": "solana",
            "address": "So1ana1234567890",
            "created_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = await self.blindpay.wallets.custodial.create(
                {
                    "customer_id": "re_000000000000",
                    "network": "solana",
                    "name": "My Solana Wallet",
                }
            )

            assert response["error"] is None
            assert response["data"] is not None
            assert response["data"]["id"] == "cw_000000000000"
            assert response["data"]["network"] == "solana"
            assert response["data"]["address"] == "So1ana1234567890"
            # `name` is required on the wire (CreateWalletIn.required includes it);
            # the create() body must actually carry it, not just the type.
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/customers/re_000000000000/wallets",
                {"network": "solana", "name": "My Solana Wallet"},
            )

    @pytest.mark.asyncio
    async def test_create_custodial_wallet_with_external_id(self):
        """external_id is optional on the wire; proves it flows through when
        supplied and that name alone (without external_id) still type-checks."""
        mocked_wallet = {
            "id": "cw_000000000000",
            "customer_id": "re_000000000000",
            "instance_id": "in_000000000000",
            "network": "solana",
            "address": "So1ana1234567890",
            "created_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = await self.blindpay.wallets.custodial.create(
                {
                    "customer_id": "re_000000000000",
                    "network": "solana",
                    "name": "My Solana Wallet",
                    "external_id": "your-database-id",
                }
            )

            assert response["error"] is None
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/customers/re_000000000000/wallets",
                {"network": "solana", "name": "My Solana Wallet", "external_id": "your-database-id"},
            )

    @pytest.mark.asyncio
    async def test_list_custodial_wallets(self):
        mocked_wallets = [
            {
                "id": "cw_000000000000",
                "customer_id": "re_000000000000",
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
            assert response["data"] is not None
            assert len(response["data"]) == 1
            assert response["data"][0]["id"] == "cw_000000000000"
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/customers/re_000000000000/wallets")

    @pytest.mark.asyncio
    async def test_get_custodial_wallet(self):
        mocked_wallet = {
            "id": "cw_000000000000",
            "customer_id": "re_000000000000",
            "instance_id": "in_000000000000",
            "network": "solana",
            "address": "So1ana1234567890",
            "created_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = await self.blindpay.wallets.custodial.get(
                {"customer_id": "re_000000000000", "id": "cw_000000000000"}
            )

            assert response["error"] is None
            assert response["data"] is not None
            assert response["data"]["id"] == "cw_000000000000"
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/customers/re_000000000000/wallets/cw_000000000000"
            )

    @pytest.mark.asyncio
    async def test_delete_custodial_wallet(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": None, "error": None}

            response = await self.blindpay.wallets.custodial.delete(
                {"customer_id": "re_000000000000", "id": "cw_000000000000"}
            )

            assert response["error"] is None
            mock_request.assert_called_once_with(
                "DELETE", "/instances/in_000000000000/customers/re_000000000000/wallets/cw_000000000000", None
            )

    def test_balance_types_match_spec(self):
        assert_matches_spec(CustodialWalletBalance, BALANCE)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("variant", ["full", "required_only", "decimals"])
    async def test_get_custodial_wallet_balance(self, variant: str):
        payload = BALANCE[variant]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": payload, "error": None}

            response = await self.blindpay.wallets.custodial.get_balance(
                {"customer_id": "cu_000000000000", "id": "wa_000000000000"}
            )

            data = response["data"]
            assert response["error"] is None
            assert data is not None
            assert data == payload
            assert data["USDC"]["amount"] == payload["USDC"]["amount"]
            assert data["USDB"]["total_amount"] == payload["USDB"]["total_amount"]
            mock_request.assert_called_once_with("GET", BALANCE_PATH)


class TestCustodialWalletsSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_create_custodial_wallet(self):
        mocked_wallet = {
            "id": "cw_000000000000",
            "customer_id": "re_000000000000",
            "instance_id": "in_000000000000",
            "network": "solana",
            "address": "So1ana1234567890",
            "created_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = self.blindpay.wallets.custodial.create(
                {
                    "customer_id": "re_000000000000",
                    "network": "solana",
                    "name": "My Solana Wallet",
                }
            )

            assert response["error"] is None
            assert response["data"] is not None
            assert response["data"]["id"] == "cw_000000000000"
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/customers/re_000000000000/wallets",
                {"network": "solana", "name": "My Solana Wallet"},
            )

    def test_create_custodial_wallet_with_external_id(self):
        mocked_wallet = {
            "id": "cw_000000000000",
            "customer_id": "re_000000000000",
            "instance_id": "in_000000000000",
            "network": "solana",
            "address": "So1ana1234567890",
            "created_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = self.blindpay.wallets.custodial.create(
                {
                    "customer_id": "re_000000000000",
                    "network": "solana",
                    "name": "My Solana Wallet",
                    "external_id": "your-database-id",
                }
            )

            assert response["error"] is None
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/customers/re_000000000000/wallets",
                {"network": "solana", "name": "My Solana Wallet", "external_id": "your-database-id"},
            )

    def test_list_custodial_wallets(self):
        mocked_wallets = [
            {
                "id": "cw_000000000000",
                "customer_id": "re_000000000000",
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
            assert response["data"] is not None
            assert len(response["data"]) == 1
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/customers/re_000000000000/wallets")

    def test_get_custodial_wallet(self):
        mocked_wallet = {
            "id": "cw_000000000000",
            "customer_id": "re_000000000000",
            "instance_id": "in_000000000000",
            "network": "solana",
            "address": "So1ana1234567890",
            "created_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = self.blindpay.wallets.custodial.get({"customer_id": "re_000000000000", "id": "cw_000000000000"})

            assert response["error"] is None
            assert response["data"] is not None
            assert response["data"]["id"] == "cw_000000000000"
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/customers/re_000000000000/wallets/cw_000000000000"
            )

    def test_delete_custodial_wallet(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": None, "error": None}

            response = self.blindpay.wallets.custodial.delete(
                {"customer_id": "re_000000000000", "id": "cw_000000000000"}
            )

            assert response["error"] is None
            mock_request.assert_called_once_with(
                "DELETE", "/instances/in_000000000000/customers/re_000000000000/wallets/cw_000000000000", None
            )

    def test_get_custodial_wallet_balance(self):
        payload = BALANCE["full"]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": payload, "error": None}

            response = self.blindpay.wallets.custodial.get_balance(
                {"customer_id": "cu_000000000000", "id": "wa_000000000000"}
            )

            data = response["data"]
            assert response["error"] is None
            assert data is not None
            assert data == payload
            assert data["USDT"]["symbol"] == payload["USDT"]["symbol"]
            assert data.get("EURC") == payload.get("EURC")
            mock_request.assert_called_once_with("GET", BALANCE_PATH)
