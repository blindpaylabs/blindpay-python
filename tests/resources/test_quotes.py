from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync
from blindpay.resources.quotes.quotes import CreateQuoteResponse


class TestQuotes:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_create_quote(self):
        mocked_quote: CreateQuoteResponse = {
            "id": "qu_000000000000",
            "expires_at": 1712958191,
            "commercial_quotation": 495,
            "blindpay_quotation": 485,
            "receiver_amount": 5240,
            "sender_amount": 1010,
            "partner_fee_amount": 150,
            "flat_fee": 50,
            "contract": {
                "abi": [{}],
                "address": "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
                "functionName": "approve",
                "blindpayContractAddress": "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
                "amount": "1000000000000000000",
                "network": {
                    "name": "Ethereum",
                    "chainId": 1,
                },
            },
            "receiver_local_amount": 1000,
            "description": "Memo code or description, only works with USD and BRL",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_quote, "error": None}

            response = await self.blindpay.quotes.create(
                {
                    "bank_account_id": "ba_000000000000",
                    "currency_type": "sender",
                    "network": "sepolia",
                    "request_amount": 1000,
                    "token": "USDC",
                    "cover_fees": True,
                    "description": "Memo code or description, only works with USD and BRL",
                    "partner_fee_id": "pf_000000000000",
                    "transaction_document_file": None,
                    "transaction_document_id": None,
                    "transaction_document_type": "invoice",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_quote
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/quotes",
                {
                    "bank_account_id": "ba_000000000000",
                    "currency_type": "sender",
                    "network": "sepolia",
                    "request_amount": 1000,
                    "token": "USDC",
                    "cover_fees": True,
                    "description": "Memo code or description, only works with USD and BRL",
                    "partner_fee_id": "pf_000000000000",
                    "transaction_document_file": None,
                    "transaction_document_id": None,
                    "transaction_document_type": "invoice",
                },
            )

    @pytest.mark.asyncio
    async def test_get_fx_rate(self):
        mocked_fx_rate = {
            "commercial_quotation": 495,
            "blindpay_quotation": 485,
            "result_amount": 1,
            "instance_flat_fee": 50,
            "instance_percentage_fee": 0,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_fx_rate, "error": None}

            response = await self.blindpay.quotes.get_fx_rate(
                {
                    "currency_type": "sender",
                    "from_currency": "USD",
                    "to": "BRL",
                    "request_amount": 1000,
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_fx_rate
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/quotes/fx",
                {
                    "currency_type": "sender",
                    "from": "USD",
                    "to": "BRL",
                    "request_amount": 1000,
                },
            )


class TestQuotesSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_create_quote(self):
        mocked_quote: CreateQuoteResponse = {
            "id": "qu_000000000000",
            "expires_at": 1712958191,
            "commercial_quotation": 495,
            "blindpay_quotation": 485,
            "receiver_amount": 5240,
            "sender_amount": 1010,
            "partner_fee_amount": 150,
            "flat_fee": 50,
            "contract": {
                "abi": [{}],
                "address": "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
                "functionName": "approve",
                "blindpayContractAddress": "0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238",
                "amount": "1000000000000000000",
                "network": {
                    "name": "Ethereum",
                    "chainId": 1,
                },
            },
            "receiver_local_amount": 1000,
            "description": "Memo code or description, only works with USD and BRL",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_quote, "error": None}

            response = self.blindpay.quotes.create(
                {
                    "bank_account_id": "ba_000000000000",
                    "currency_type": "sender",
                    "network": "sepolia",
                    "request_amount": 1000,
                    "token": "USDC",
                    "cover_fees": True,
                    "description": "Memo code or description, only works with USD and BRL",
                    "partner_fee_id": "pf_000000000000",
                    "transaction_document_file": None,
                    "transaction_document_id": None,
                    "transaction_document_type": "invoice",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_quote
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/quotes",
                {
                    "bank_account_id": "ba_000000000000",
                    "currency_type": "sender",
                    "network": "sepolia",
                    "request_amount": 1000,
                    "token": "USDC",
                    "cover_fees": True,
                    "description": "Memo code or description, only works with USD and BRL",
                    "partner_fee_id": "pf_000000000000",
                    "transaction_document_file": None,
                    "transaction_document_id": None,
                    "transaction_document_type": "invoice",
                },
            )

    def test_get_fx_rate(self):
        mocked_fx_rate = {
            "commercial_quotation": 495,
            "blindpay_quotation": 485,
            "result_amount": 1,
            "instance_flat_fee": 50,
            "instance_percentage_fee": 0,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_fx_rate, "error": None}

            response = self.blindpay.quotes.get_fx_rate(
                {
                    "currency_type": "sender",
                    "from_currency": "USD",
                    "to": "BRL",
                    "request_amount": 1000,
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_fx_rate
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/quotes/fx",
                {
                    "currency_type": "sender",
                    "from": "USD",
                    "to": "BRL",
                    "request_amount": 1000,
                },
            )
