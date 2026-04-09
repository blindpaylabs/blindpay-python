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
            "amount": 100.00,
            "currency": "USD",
            "fee_amount": 1.50,
            "source_wallet_id": "cw_source",
            "destination_wallet_id": "cw_dest",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_quote, "error": None}

            response = await self.blindpay.transfers.create_quote(
                {
                    "source_wallet_id": "cw_source",
                    "destination_wallet_id": "cw_dest",
                    "amount": 100.00,
                }
            )

            assert response["error"] is None
            assert response["data"]["id"] == "tq_000000000000"
            assert response["data"]["amount"] == 100.00
            assert response["data"]["fee_amount"] == 1.50
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/transfer-quotes",
                {
                    "source_wallet_id": "cw_source",
                    "destination_wallet_id": "cw_dest",
                    "amount": 100.00,
                },
            )

    @pytest.mark.asyncio
    async def test_create_transfer(self):
        mocked_transfer = {
            "id": "tr_000000000000",
            "instance_id": "in_000000000000",
            "status": "processing",
            "quote_id": "tq_000000000000",
            "source_wallet_id": "cw_source",
            "destination_wallet_id": "cw_dest",
            "amount": 100.00,
            "currency": "USD",
            "tracking_transaction": {"status": "processing", "date": "2025-01-01T00:00:00Z"},
            "tracking_transaction_monitoring": {"status": "processing", "date": None},
            "tracking_complete": {"status": "processing", "date": None},
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_transfer, "error": None}

            response = await self.blindpay.transfers.create({"quote_id": "tq_000000000000"})

            assert response["error"] is None
            assert response["data"]["id"] == "tr_000000000000"
            assert response["data"]["status"] == "processing"
            assert response["data"]["amount"] == 100.00
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/transfers",
                {"quote_id": "tq_000000000000"},
            )

    @pytest.mark.asyncio
    async def test_get_transfer(self):
        mocked_transfer = {
            "id": "tr_000000000000",
            "instance_id": "in_000000000000",
            "status": "completed",
            "quote_id": "tq_000000000000",
            "source_wallet_id": "cw_source",
            "destination_wallet_id": "cw_dest",
            "amount": 100.00,
            "currency": "USD",
            "tracking_transaction": {"status": "completed", "date": "2025-01-01T00:00:00Z"},
            "tracking_transaction_monitoring": {"status": "completed", "date": "2025-01-01T00:00:00Z"},
            "tracking_complete": {"status": "completed", "date": "2025-01-01T00:00:00Z"},
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_transfer, "error": None}

            response = await self.blindpay.transfers.get("tr_000000000000")

            assert response["error"] is None
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
                    "quote_id": "tq_000000000000",
                    "source_wallet_id": "cw_source",
                    "destination_wallet_id": "cw_dest",
                    "amount": 100.00,
                    "currency": "USD",
                    "tracking_transaction": {"status": "completed", "date": "2025-01-01T00:00:00Z"},
                    "tracking_transaction_monitoring": {"status": "completed", "date": "2025-01-01T00:00:00Z"},
                    "tracking_complete": {"status": "completed", "date": "2025-01-01T00:00:00Z"},
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
            "amount": 100.00,
            "currency": "USD",
            "fee_amount": 1.50,
            "source_wallet_id": "cw_source",
            "destination_wallet_id": "cw_dest",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_quote, "error": None}

            response = self.blindpay.transfers.create_quote(
                {
                    "source_wallet_id": "cw_source",
                    "destination_wallet_id": "cw_dest",
                    "amount": 100.00,
                }
            )

            assert response["error"] is None
            assert response["data"]["id"] == "tq_000000000000"
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/transfer-quotes",
                {
                    "source_wallet_id": "cw_source",
                    "destination_wallet_id": "cw_dest",
                    "amount": 100.00,
                },
            )

    def test_create_transfer(self):
        mocked_transfer = {
            "id": "tr_000000000000",
            "instance_id": "in_000000000000",
            "status": "processing",
            "quote_id": "tq_000000000000",
            "source_wallet_id": "cw_source",
            "destination_wallet_id": "cw_dest",
            "amount": 100.00,
            "currency": "USD",
            "tracking_transaction": {"status": "processing", "date": "2025-01-01T00:00:00Z"},
            "tracking_transaction_monitoring": {"status": "processing", "date": None},
            "tracking_complete": {"status": "processing", "date": None},
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_transfer, "error": None}

            response = self.blindpay.transfers.create({"quote_id": "tq_000000000000"})

            assert response["error"] is None
            assert response["data"]["id"] == "tr_000000000000"
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/transfers",
                {"quote_id": "tq_000000000000"},
            )

    def test_get_transfer(self):
        mocked_transfer = {
            "id": "tr_000000000000",
            "instance_id": "in_000000000000",
            "status": "completed",
            "quote_id": "tq_000000000000",
            "source_wallet_id": "cw_source",
            "destination_wallet_id": "cw_dest",
            "amount": 100.00,
            "currency": "USD",
            "tracking_transaction": {"status": "completed", "date": "2025-01-01T00:00:00Z"},
            "tracking_transaction_monitoring": {"status": "completed", "date": "2025-01-01T00:00:00Z"},
            "tracking_complete": {"status": "completed", "date": "2025-01-01T00:00:00Z"},
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_transfer, "error": None}

            response = self.blindpay.transfers.get("tr_000000000000")

            assert response["error"] is None
            assert response["data"]["id"] == "tr_000000000000"
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/transfers/tr_000000000000")

    def test_list_transfers(self):
        mocked_transfers = {
            "data": [
                {
                    "id": "tr_000000000000",
                    "instance_id": "in_000000000000",
                    "status": "completed",
                    "quote_id": "tq_000000000000",
                    "source_wallet_id": "cw_source",
                    "destination_wallet_id": "cw_dest",
                    "amount": 100.00,
                    "currency": "USD",
                    "tracking_transaction": {"status": "completed", "date": "2025-01-01T00:00:00Z"},
                    "tracking_transaction_monitoring": {"status": "completed", "date": "2025-01-01T00:00:00Z"},
                    "tracking_complete": {"status": "completed", "date": "2025-01-01T00:00:00Z"},
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
            assert len(response["data"]["data"]) == 1
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/transfers")
