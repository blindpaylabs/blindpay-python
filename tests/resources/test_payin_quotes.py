from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestPayinQuotes:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_create_payin_quote(self):
        mocked_payin_quote = {
            "id": "qu_000000000000",
            "expires_at": 1712958191,
            "commercial_quotation": 495,
            "blindpay_quotation": 505,
            "receiver_amount": 1010,
            "sender_amount": 5240,
            "partner_fee_amount": 150,
            "flat_fee": 50,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payin_quote, "error": None}

            response = await self.blindpay.payins.quotes.create(
                {
                    "blockchain_wallet_id": "bw_000000000000",
                    "currency_type": "sender",
                    "cover_fees": True,
                    "request_amount": 1000,
                    "payment_method": "pix",
                    "token": "USDC",
                    "partner_fee_id": "pf_000000000000",
                    "payer_rules": {
                        "pix_allowed_tax_ids": ["149.476.037-68"],
                    },
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_payin_quote
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/payin-quotes",
                {
                    "blockchain_wallet_id": "bw_000000000000",
                    "currency_type": "sender",
                    "cover_fees": True,
                    "request_amount": 1000,
                    "payment_method": "pix",
                    "token": "USDC",
                    "partner_fee_id": "pf_000000000000",
                    "payer_rules": {
                        "pix_allowed_tax_ids": ["149.476.037-68"],
                    },
                },
            )

    @pytest.mark.asyncio
    async def test_get_fx_rate(self):
        mocked_fx_rate = {
            "commercial_quotation": 495,
            "blindpay_quotation": 505,
            "result_amount": 1,
            "instance_flat_fee": 50,
            "instance_percentage_fee": 0,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_fx_rate, "error": None}

            response = await self.blindpay.payins.quotes.get_fx_rate(
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
                "/instances/in_000000000000/payin-quotes/fx",
                {
                    "currency_type": "sender",
                    "from": "USD",
                    "to": "BRL",
                    "request_amount": 1000,
                },
            )


class TestPayinQuotesSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_create_payin_quote(self):
        mocked_payin_quote = {
            "id": "qu_000000000000",
            "expires_at": 1712958191,
            "commercial_quotation": 495,
            "blindpay_quotation": 505,
            "receiver_amount": 1010,
            "sender_amount": 5240,
            "partner_fee_amount": 150,
            "flat_fee": 50,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payin_quote, "error": None}

            response = self.blindpay.payins.quotes.create(
                {
                    "blockchain_wallet_id": "bw_000000000000",
                    "currency_type": "sender",
                    "cover_fees": True,
                    "request_amount": 1000,
                    "payment_method": "pix",
                    "token": "USDC",
                    "partner_fee_id": "pf_000000000000",
                    "payer_rules": {
                        "pix_allowed_tax_ids": ["149.476.037-68"],
                    },
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_payin_quote
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/payin-quotes",
                {
                    "blockchain_wallet_id": "bw_000000000000",
                    "currency_type": "sender",
                    "cover_fees": True,
                    "request_amount": 1000,
                    "payment_method": "pix",
                    "token": "USDC",
                    "partner_fee_id": "pf_000000000000",
                    "payer_rules": {
                        "pix_allowed_tax_ids": ["149.476.037-68"],
                    },
                },
            )

    def test_get_fx_rate(self):
        mocked_fx_rate = {
            "commercial_quotation": 495,
            "blindpay_quotation": 505,
            "result_amount": 1,
            "instance_flat_fee": 50,
            "instance_percentage_fee": 0,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_fx_rate, "error": None}

            response = self.blindpay.payins.quotes.get_fx_rate(
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
                "/instances/in_000000000000/payin-quotes/fx",
                {
                    "currency_type": "sender",
                    "from": "USD",
                    "to": "BRL",
                    "request_amount": 1000,
                },
            )
