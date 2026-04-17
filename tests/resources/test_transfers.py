from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestTransfers:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_create_transfer_quote(self):
        mocked_quote = {
            "id": "tq_000000000000",
            "expires_at": 1700000000,
            "commercial_quotation": 1.0,
            "blindpay_quotation": 1.0,
            "receiver_amount": 100.0,
            "sender_amount": 100.5,
            "flat_fee": 0.5,
            "partner_fee_amount": None,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_quote, "error": None}

            response = await self.blindpay.transfers.create_quote(
                {
                    "wallet_id": "cw_source",
                    "sender_token": "USDC",
                    "receiver_wallet_address": "0x1234567890abcdef",
                    "receiver_token": "USDC",
                    "receiver_network": "base",
                    "request_amount": 100,
                    "amount_reference": "sender",
                }
            )

            assert response["error"] is None
            assert response["data"] is not None
            assert response["data"]["id"] == "tq_000000000000"
            assert response["data"]["receiver_amount"] == 100.0
            assert response["data"]["flat_fee"] == 0.5
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/transfer-quotes",
                {
                    "wallet_id": "cw_source",
                    "sender_token": "USDC",
                    "receiver_wallet_address": "0x1234567890abcdef",
                    "receiver_token": "USDC",
                    "receiver_network": "base",
                    "request_amount": 100,
                    "amount_reference": "sender",
                },
            )

    @pytest.mark.asyncio
    async def test_create_transfer(self):
        mocked_transfer = {
            "id": "tr_000000000000",
            "instance_id": "in_000000000000",
            "status": "processing",
            "transfer_quote_id": "tq_000000000000",
            "wallet_id": "cw_source",
            "sender_token": "USDC",
            "sender_amount": 100.5,
            "receiver_amount": 100.0,
            "receiver_token": "USDC",
            "receiver_network": "base",
            "receiver_wallet_address": "0x1234567890abcdef",
            "receiver_id": "rc_000000000000",
            "address": "0x1234567890abcdef",
            "network": "base",
            "tracking_transaction_monitoring": {"step": "pending", "estimated_time_of_arrival": None},
            "tracking_paymaster": {"step": "pending", "estimated_time_of_arrival": None},
            "tracking_bridge_swap": {"step": "pending", "estimated_time_of_arrival": None},
            "tracking_complete": {"step": "pending", "estimated_time_of_arrival": None},
            "tracking_partner_fee": {"step": "pending", "estimated_time_of_arrival": None},
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_transfer, "error": None}

            response = await self.blindpay.transfers.create({"transfer_quote_id": "tq_000000000000"})

            assert response["error"] is None
            assert response["data"] is not None
            assert response["data"]["id"] == "tr_000000000000"
            assert response["data"]["status"] == "processing"
            assert response["data"]["sender_amount"] == 100.5
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/transfers",
                {"transfer_quote_id": "tq_000000000000"},
            )

    @pytest.mark.asyncio
    async def test_get_transfer(self):
        mocked_transfer = {
            "id": "tr_000000000000",
            "instance_id": "in_000000000000",
            "status": "completed",
            "transfer_quote_id": "tq_000000000000",
            "wallet_id": "cw_source",
            "sender_token": "USDC",
            "sender_amount": 100.5,
            "receiver_amount": 100.0,
            "receiver_token": "USDC",
            "receiver_network": "base",
            "receiver_wallet_address": "0x1234567890abcdef",
            "receiver_id": "rc_000000000000",
            "address": "0x1234567890abcdef",
            "network": "base",
            "tracking_transaction_monitoring": {"step": "completed", "estimated_time_of_arrival": None},
            "tracking_paymaster": {"step": "completed", "estimated_time_of_arrival": None},
            "tracking_bridge_swap": {"step": "completed", "estimated_time_of_arrival": None},
            "tracking_complete": {"step": "completed", "estimated_time_of_arrival": None},
            "tracking_partner_fee": {"step": "completed", "estimated_time_of_arrival": None},
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_transfer, "error": None}

            response = await self.blindpay.transfers.get("tr_000000000000")

            assert response["error"] is None
            assert response["data"] is not None
            assert response["data"]["id"] == "tr_000000000000"
            assert response["data"]["status"] == "completed"
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/transfers/tr_000000000000")

    @pytest.mark.asyncio
    async def test_list_transfers(self):
        mocked_transfers = {
            "data": [
                {
                    "id": "tr_000000000000",
                    "instance_id": "in_000000000000",
                    "status": "completed",
                    "transfer_quote_id": "tq_000000000000",
                    "wallet_id": "cw_source",
                    "sender_token": "USDC",
                    "sender_amount": 100.5,
                    "receiver_amount": 100.0,
                    "receiver_token": "USDC",
                    "receiver_network": "base",
                    "receiver_wallet_address": "0x1234567890abcdef",
                    "receiver_id": "rc_000000000000",
                    "address": "0x1234567890abcdef",
                    "network": "base",
                    "tracking_transaction_monitoring": {"step": "completed", "estimated_time_of_arrival": None},
                    "tracking_paymaster": {"step": "completed", "estimated_time_of_arrival": None},
                    "tracking_bridge_swap": {"step": "completed", "estimated_time_of_arrival": None},
                    "tracking_complete": {"step": "completed", "estimated_time_of_arrival": None},
                    "tracking_partner_fee": {"step": "completed", "estimated_time_of_arrival": None},
                    "created_at": "2025-01-01T00:00:00Z",
                    "updated_at": "2025-01-01T00:00:00Z",
                },
            ],
            "pagination": {
                "has_more": False,
                "next_page": None,
                "prev_page": None,
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_transfers, "error": None}

            response = await self.blindpay.transfers.list()

            assert response["error"] is None
            assert response["data"] is not None
            assert len(response["data"]["data"]) == 1
            assert response["data"]["data"][0]["id"] == "tr_000000000000"
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/transfers")


class TestTransfersSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_create_transfer_quote(self):
        mocked_quote = {
            "id": "tq_000000000000",
            "expires_at": 1700000000,
            "commercial_quotation": 1.0,
            "blindpay_quotation": 1.0,
            "receiver_amount": 100.0,
            "sender_amount": 100.5,
            "flat_fee": 0.5,
            "partner_fee_amount": None,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_quote, "error": None}

            response = self.blindpay.transfers.create_quote(
                {
                    "wallet_id": "cw_source",
                    "sender_token": "USDC",
                    "receiver_wallet_address": "0x1234567890abcdef",
                    "receiver_token": "USDC",
                    "receiver_network": "base",
                    "request_amount": 100,
                    "amount_reference": "sender",
                }
            )

            assert response["error"] is None
            assert response["data"] is not None
            assert response["data"]["id"] == "tq_000000000000"
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/transfer-quotes",
                {
                    "wallet_id": "cw_source",
                    "sender_token": "USDC",
                    "receiver_wallet_address": "0x1234567890abcdef",
                    "receiver_token": "USDC",
                    "receiver_network": "base",
                    "request_amount": 100,
                    "amount_reference": "sender",
                },
            )

    def test_create_transfer(self):
        mocked_transfer = {
            "id": "tr_000000000000",
            "instance_id": "in_000000000000",
            "status": "processing",
            "transfer_quote_id": "tq_000000000000",
            "wallet_id": "cw_source",
            "sender_token": "USDC",
            "sender_amount": 100.5,
            "receiver_amount": 100.0,
            "receiver_token": "USDC",
            "receiver_network": "base",
            "receiver_wallet_address": "0x1234567890abcdef",
            "receiver_id": "rc_000000000000",
            "address": "0x1234567890abcdef",
            "network": "base",
            "tracking_transaction_monitoring": {"step": "pending", "estimated_time_of_arrival": None},
            "tracking_paymaster": {"step": "pending", "estimated_time_of_arrival": None},
            "tracking_bridge_swap": {"step": "pending", "estimated_time_of_arrival": None},
            "tracking_complete": {"step": "pending", "estimated_time_of_arrival": None},
            "tracking_partner_fee": {"step": "pending", "estimated_time_of_arrival": None},
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_transfer, "error": None}

            response = self.blindpay.transfers.create({"transfer_quote_id": "tq_000000000000"})

            assert response["error"] is None
            assert response["data"] is not None
            assert response["data"]["id"] == "tr_000000000000"
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/transfers",
                {"transfer_quote_id": "tq_000000000000"},
            )

    def test_get_transfer(self):
        mocked_transfer = {
            "id": "tr_000000000000",
            "instance_id": "in_000000000000",
            "status": "completed",
            "transfer_quote_id": "tq_000000000000",
            "wallet_id": "cw_source",
            "sender_token": "USDC",
            "sender_amount": 100.5,
            "receiver_amount": 100.0,
            "receiver_token": "USDC",
            "receiver_network": "base",
            "receiver_wallet_address": "0x1234567890abcdef",
            "receiver_id": "rc_000000000000",
            "address": "0x1234567890abcdef",
            "network": "base",
            "tracking_transaction_monitoring": {"step": "completed", "estimated_time_of_arrival": None},
            "tracking_paymaster": {"step": "completed", "estimated_time_of_arrival": None},
            "tracking_bridge_swap": {"step": "completed", "estimated_time_of_arrival": None},
            "tracking_complete": {"step": "completed", "estimated_time_of_arrival": None},
            "tracking_partner_fee": {"step": "completed", "estimated_time_of_arrival": None},
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_transfer, "error": None}

            response = self.blindpay.transfers.get("tr_000000000000")

            assert response["error"] is None
            assert response["data"] is not None
            assert response["data"]["id"] == "tr_000000000000"
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/transfers/tr_000000000000")

    def test_list_transfers(self):
        mocked_transfers = {
            "data": [
                {
                    "id": "tr_000000000000",
                    "instance_id": "in_000000000000",
                    "status": "completed",
                    "transfer_quote_id": "tq_000000000000",
                    "wallet_id": "cw_source",
                    "sender_token": "USDC",
                    "sender_amount": 100.5,
                    "receiver_amount": 100.0,
                    "receiver_token": "USDC",
                    "receiver_network": "base",
                    "receiver_wallet_address": "0x1234567890abcdef",
                    "receiver_id": "rc_000000000000",
                    "address": "0x1234567890abcdef",
                    "network": "base",
                    "tracking_transaction_monitoring": {"step": "completed", "estimated_time_of_arrival": None},
                    "tracking_paymaster": {"step": "completed", "estimated_time_of_arrival": None},
                    "tracking_bridge_swap": {"step": "completed", "estimated_time_of_arrival": None},
                    "tracking_complete": {"step": "completed", "estimated_time_of_arrival": None},
                    "tracking_partner_fee": {"step": "completed", "estimated_time_of_arrival": None},
                    "created_at": "2025-01-01T00:00:00Z",
                    "updated_at": "2025-01-01T00:00:00Z",
                },
            ],
            "pagination": {
                "has_more": False,
                "next_page": None,
                "prev_page": None,
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_transfers, "error": None}

            response = self.blindpay.transfers.list()

            assert response["error"] is None
            assert response["data"] is not None
            assert len(response["data"]["data"]) == 1
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/transfers")
