from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestPayins:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_list_payins(self):
        mocked_payins = {
            "data": [
                {
                    "receiver_id": "re_000000000000",
                    "id": "re_000000000000",
                    "pix_code": (
                        "00020101021226790014br.gov.bcb.pix2557brcode.starkinfra.com/v2/"
                        "bcf07f6c4110454e9fd6f120bab13e835204000053039865802BR5915Blind Pay, Inc."
                        "6010Vila Velha62070503***6304BCAB"
                    ),
                    "memo_code": "8K45GHBNT6BQ6462",
                    "clabe": "014027000000000008",
                    "status": "processing",
                    "payin_quote_id": "pq_000000000000",
                    "instance_id": "in_000000000000",
                    "tracking_transaction": {
                        "step": "processing",
                        "status": "failed",
                        "transaction_hash": "0x123...890",
                        "completed_at": "2011-10-05T14:48:00.000Z",
                    },
                    "tracking_payment": {
                        "step": "on_hold",
                        "provider_name": "blockchain",
                        "provider_transaction_id": "tx_123456789",
                        "provider_status": "confirmed",
                        "estimated_time_of_arrival": "2011-10-05T15:00:00.000Z",
                        "completed_at": "2011-10-05T14:48:00.000Z",
                    },
                    "tracking_complete": {
                        "step": "on_hold",
                        "status": "completed",
                        "transaction_hash": "0x123...890",
                        "completed_at": "2011-10-05T14:48:00.000Z",
                    },
                    "tracking_partner_fee": {
                        "step": "on_hold",
                        "transaction_hash": "0x123...890",
                        "completed_at": "2011-10-05T14:48:00.000Z",
                    },
                    "created_at": "2021-01-01T00:00:00Z",
                    "updated_at": "2021-01-01T00:00:00Z",
                    "image_url": "https://example.com/image.png",
                    "first_name": "John",
                    "last_name": "Doe",
                    "legal_name": "Company Name Inc.",
                    "type": "individual",
                    "payment_method": "pix",
                    "sender_amount": 5240,
                    "receiver_amount": 1010,
                    "token": "USDC",
                    "partner_fee_amount": 150,
                    "total_fee_amount": 1.53,
                    "commercial_quotation": 495,
                    "blindpay_quotation": 505,
                    "currency": "BRL",
                    "billing_fee": 100,
                    "name": "Wallet Display Name",
                    "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
                    "network": "polygon",
                    "blindpay_bank_details": {
                        "routing_number": "121145349",
                        "account_number": "621327727210181",
                        "account_type": "Business checking",
                        "swift_bic_code": "CHASUS33",
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
                        "beneficiary": {
                            "name": "BlindPay, Inc.",
                            "address_line_1": "8 The Green",
                            "address_line_2": "Dover, DE 19901",
                        },
                        "receiving_bank": {
                            "name": "Column NA - Brex",
                            "address_line_1": "1 Letterman Drive, Building A, Suite A4-700",
                            "address_line_2": "San Francisco, CA 94129",
                        },
                    },
                },
            ],
            "pagination": {
                "has_more": True,
                "next_page": 3,
                "prev_page": 1,
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payins, "error": None}

            response = await self.blindpay.payins.list()

            assert response["error"] is None
            assert response["data"] == mocked_payins
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/payins")

    @pytest.mark.asyncio
    async def test_get_payin(self):
        mocked_payin = {
            "receiver_id": "re_000000000000",
            "id": "re_000000000000",
            "pix_code": (
                "00020101021226790014br.gov.bcb.pix2557brcode.starkinfra.com/v2/"
                "bcf07f6c4110454e9fd6f120bab13e835204000053039865802BR5915Blind Pay, Inc."
                "6010Vila Velha62070503***6304BCAB"
            ),
            "memo_code": "8K45GHBNT6BQ6462",
            "clabe": "014027000000000008",
            "status": "processing",
            "payin_quote_id": "pq_000000000000",
            "instance_id": "in_000000000000",
            "tracking_transaction": {
                "step": "processing",
                "status": "failed",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_payment": {
                "step": "on_hold",
                "provider_name": "blockchain",
                "provider_transaction_id": "tx_123456789",
                "provider_status": "confirmed",
                "estimated_time_of_arrival": "2011-10-05T15:00:00.000Z",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_complete": {
                "step": "on_hold",
                "status": "completed",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_partner_fee": {
                "step": "on_hold",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "created_at": "2021-01-01T00:00:00Z",
            "updated_at": "2021-01-01T00:00:00Z",
            "image_url": "https://example.com/image.png",
            "first_name": "John",
            "last_name": "Doe",
            "legal_name": "Company Name Inc.",
            "type": "individual",
            "payment_method": "pix",
            "sender_amount": 5240,
            "receiver_amount": 1010,
            "token": "USDC",
            "partner_fee_amount": 150,
            "total_fee_amount": 1.53,
            "commercial_quotation": 495,
            "blindpay_quotation": 505,
            "currency": "BRL",
            "billing_fee": 100,
            "name": "Wallet Display Name",
            "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
            "network": "polygon",
            "blindpay_bank_details": {
                "routing_number": "121145349",
                "account_number": "621327727210181",
                "account_type": "Business checking",
                "swift_bic_code": "CHASUS33",
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
                "beneficiary": {
                    "name": "BlindPay, Inc.",
                    "address_line_1": "8 The Green",
                    "address_line_2": "Dover, DE 19901",
                },
                "receiving_bank": {
                    "name": "Column NA - Brex",
                    "address_line_1": "1 Letterman Drive, Building A, Suite A4-700",
                    "address_line_2": "San Francisco, CA 94129",
                },
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payin, "error": None}

            response = await self.blindpay.payins.get("pi_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_payin
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/payins/pi_000000000000")

    @pytest.mark.asyncio
    async def test_export_payins(self):
        mocked_export_payins = [
            {
                "receiver_id": "re_000000000000",
                "id": "re_000000000000",
                "pix_code": (
                    "00020101021226790014br.gov.bcb.pix2557brcode.starkinfra.com/v2/"
                    "bcf07f6c4110454e9fd6f120bab13e835204000053039865802BR5915Blind Pay, Inc."
                    "6010Vila Velha62070503***6304BCAB"
                ),
                "memo_code": "8K45GHBNT6BQ6462",
                "clabe": "014027000000000008",
                "status": "processing",
                "payin_quote_id": "pq_000000000000",
                "instance_id": "in_000000000000",
                "tracking_transaction": {
                    "step": "processing",
                    "status": "failed",
                    "transaction_hash": "0x123...890",
                    "completed_at": "2011-10-05T14:48:00.000Z",
                },
                "tracking_payment": {
                    "step": "on_hold",
                    "provider_name": "blockchain",
                    "provider_transaction_id": "tx_123456789",
                    "provider_status": "confirmed",
                    "estimated_time_of_arrival": "2011-10-05T15:00:00.000Z",
                    "completed_at": "2011-10-05T14:48:00.000Z",
                },
                "tracking_complete": {
                    "step": "on_hold",
                    "status": "completed",
                    "transaction_hash": "0x123...890",
                    "completed_at": "2011-10-05T14:48:00.000Z",
                },
                "tracking_partner_fee": {
                    "step": "on_hold",
                    "transaction_hash": "0x123...890",
                    "completed_at": "2011-10-05T14:48:00.000Z",
                },
                "created_at": "2021-01-01T00:00:00Z",
                "updated_at": "2021-01-01T00:00:00Z",
                "image_url": "https://example.com/image.png",
                "first_name": "John",
                "last_name": "Doe",
                "legal_name": "Company Name Inc.",
                "type": "individual",
                "payment_method": "pix",
                "sender_amount": 5240,
                "receiver_amount": 1010,
                "token": "USDC",
                "partner_fee_amount": 150,
                "total_fee_amount": 1.53,
                "commercial_quotation": 495,
                "blindpay_quotation": 505,
                "currency": "BRL",
                "billing_fee": 100,
                "name": "Wallet Display Name",
                "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
                "network": "polygon",
                "blindpay_bank_details": {
                    "routing_number": "121145349",
                    "account_number": "621327727210181",
                    "account_type": "Business checking",
                    "swift_bic_code": "CHASUS33",
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
                    "beneficiary": {
                        "name": "BlindPay, Inc.",
                        "address_line_1": "8 The Green",
                        "address_line_2": "Dover, DE 19901",
                    },
                    "receiving_bank": {
                        "name": "Column NA - Brex",
                        "address_line_1": "1 Letterman Drive, Building A, Suite A4-700",
                        "address_line_2": "San Francisco, CA 94129",
                    },
                },
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_export_payins, "error": None}

            response = await self.blindpay.payins.export(
                {
                    "status": "processing",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_export_payins
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/export/payins?status=processing")

    @pytest.mark.asyncio
    async def test_create_evm_payin(self):
        mocked_evm_payin = {
            "id": "pi_000000000000",
            "status": "processing",
            "pix_code": (
                "00020101021226790014br.gov.bcb.pix2557brcode.starkinfra.com/v2/"
                "bcf07f6c4110454e9fd6f120bab13e835204000053039865802BR5915Blind Pay, Inc."
                "6010Vila Velha62070503***6304BCAB"
            ),
            "memo_code": "8K45GHBNT6BQ6462",
            "clabe": "014027000000000008",
            "tracking_complete": {
                "step": "on_hold",
                "status": "completed",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_payment": {
                "step": "on_hold",
                "provider_name": "blockchain",
                "provider_transaction_id": "tx_123456789",
                "provider_status": "confirmed",
                "estimated_time_of_arrival": "2011-10-05T15:00:00.000Z",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_transaction": {
                "step": "processing",
                "status": "failed",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_partner_fee": {
                "step": "on_hold",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "blindpay_bank_details": {
                "routing_number": "121145349",
                "account_number": "621327727210181",
                "account_type": "Business checking",
                "swift_bic_code": "CHASUS33",
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
                "beneficiary": {
                    "name": "BlindPay, Inc.",
                    "address_line_1": "8 The Green",
                    "address_line_2": "Dover, DE 19901",
                },
                "receiving_bank": {
                    "name": "Column NA - Brex",
                    "address_line_1": "1 Letterman Drive, Building A, Suite A4-700",
                    "address_line_2": "San Francisco, CA 94129",
                },
            },
            "receiver_id": "re_000000000000",
            "receiver_amount": 1010,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_evm_payin, "error": None}

            response = await self.blindpay.payins.create_evm("pq_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_evm_payin
            mock_request.assert_called_once_with(
                "POST", "/instances/in_000000000000/payins/evm", {"payin_quote_id": "pq_000000000000"}
            )


class TestPayinsSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_list_payins(self):
        mocked_payins = {
            "data": [
                {
                    "receiver_id": "re_000000000000",
                    "id": "re_000000000000",
                    "pix_code": (
                        "00020101021226790014br.gov.bcb.pix2557brcode.starkinfra.com/v2/"
                        "bcf07f6c4110454e9fd6f120bab13e835204000053039865802BR5915Blind Pay, Inc."
                        "6010Vila Velha62070503***6304BCAB"
                    ),
                    "memo_code": "8K45GHBNT6BQ6462",
                    "clabe": "014027000000000008",
                    "status": "processing",
                    "payin_quote_id": "pq_000000000000",
                    "instance_id": "in_000000000000",
                    "tracking_transaction": {
                        "step": "processing",
                        "status": "failed",
                        "transaction_hash": "0x123...890",
                        "completed_at": "2011-10-05T14:48:00.000Z",
                    },
                    "tracking_payment": {
                        "step": "on_hold",
                        "provider_name": "blockchain",
                        "provider_transaction_id": "tx_123456789",
                        "provider_status": "confirmed",
                        "estimated_time_of_arrival": "2011-10-05T15:00:00.000Z",
                        "completed_at": "2011-10-05T14:48:00.000Z",
                    },
                    "tracking_complete": {
                        "step": "on_hold",
                        "status": "completed",
                        "transaction_hash": "0x123...890",
                        "completed_at": "2011-10-05T14:48:00.000Z",
                    },
                    "tracking_partner_fee": {
                        "step": "on_hold",
                        "transaction_hash": "0x123...890",
                        "completed_at": "2011-10-05T14:48:00.000Z",
                    },
                    "created_at": "2021-01-01T00:00:00Z",
                    "updated_at": "2021-01-01T00:00:00Z",
                    "image_url": "https://example.com/image.png",
                    "first_name": "John",
                    "last_name": "Doe",
                    "legal_name": "Company Name Inc.",
                    "type": "individual",
                    "payment_method": "pix",
                    "sender_amount": 5240,
                    "receiver_amount": 1010,
                    "token": "USDC",
                    "partner_fee_amount": 150,
                    "total_fee_amount": 1.53,
                    "commercial_quotation": 495,
                    "blindpay_quotation": 505,
                    "currency": "BRL",
                    "billing_fee": 100,
                    "name": "Wallet Display Name",
                    "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
                    "network": "polygon",
                    "blindpay_bank_details": {
                        "routing_number": "121145349",
                        "account_number": "621327727210181",
                        "account_type": "Business checking",
                        "swift_bic_code": "CHASUS33",
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
                        "beneficiary": {
                            "name": "BlindPay, Inc.",
                            "address_line_1": "8 The Green",
                            "address_line_2": "Dover, DE 19901",
                        },
                        "receiving_bank": {
                            "name": "Column NA - Brex",
                            "address_line_1": "1 Letterman Drive, Building A, Suite A4-700",
                            "address_line_2": "San Francisco, CA 94129",
                        },
                    },
                },
            ],
            "pagination": {
                "has_more": True,
                "next_page": 3,
                "prev_page": 1,
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payins, "error": None}

            response = self.blindpay.payins.list()

            assert response["error"] is None
            assert response["data"] == mocked_payins
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/payins")

    def test_get_payin(self):
        mocked_payin = {
            "receiver_id": "re_000000000000",
            "id": "re_000000000000",
            "pix_code": (
                "00020101021226790014br.gov.bcb.pix2557brcode.starkinfra.com/v2/"
                "bcf07f6c4110454e9fd6f120bab13e835204000053039865802BR5915Blind Pay, Inc."
                "6010Vila Velha62070503***6304BCAB"
            ),
            "memo_code": "8K45GHBNT6BQ6462",
            "clabe": "014027000000000008",
            "status": "processing",
            "payin_quote_id": "pq_000000000000",
            "instance_id": "in_000000000000",
            "tracking_transaction": {
                "step": "processing",
                "status": "failed",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_payment": {
                "step": "on_hold",
                "provider_name": "blockchain",
                "provider_transaction_id": "tx_123456789",
                "provider_status": "confirmed",
                "estimated_time_of_arrival": "2011-10-05T15:00:00.000Z",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_complete": {
                "step": "on_hold",
                "status": "completed",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_partner_fee": {
                "step": "on_hold",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "created_at": "2021-01-01T00:00:00Z",
            "updated_at": "2021-01-01T00:00:00Z",
            "image_url": "https://example.com/image.png",
            "first_name": "John",
            "last_name": "Doe",
            "legal_name": "Company Name Inc.",
            "type": "individual",
            "payment_method": "pix",
            "sender_amount": 5240,
            "receiver_amount": 1010,
            "token": "USDC",
            "partner_fee_amount": 150,
            "total_fee_amount": 1.53,
            "commercial_quotation": 495,
            "blindpay_quotation": 505,
            "currency": "BRL",
            "billing_fee": 100,
            "name": "Wallet Display Name",
            "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
            "network": "polygon",
            "blindpay_bank_details": {
                "routing_number": "121145349",
                "account_number": "621327727210181",
                "account_type": "Business checking",
                "swift_bic_code": "CHASUS33",
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
                "beneficiary": {
                    "name": "BlindPay, Inc.",
                    "address_line_1": "8 The Green",
                    "address_line_2": "Dover, DE 19901",
                },
                "receiving_bank": {
                    "name": "Column NA - Brex",
                    "address_line_1": "1 Letterman Drive, Building A, Suite A4-700",
                    "address_line_2": "San Francisco, CA 94129",
                },
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payin, "error": None}

            response = self.blindpay.payins.get("pi_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_payin
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/payins/pi_000000000000")

    def test_get_payin_track(self):
        mocked_payin_track = {
            "receiver_id": "re_000000000000",
            "id": "re_000000000000",
            "pix_code": (
                "00020101021226790014br.gov.bcb.pix2557brcode.starkinfra.com/v2/"
                "bcf07f6c4110454e9fd6f120bab13e835204000053039865802BR5915Blind Pay, Inc."
                "6010Vila Velha62070503***6304BCAB"
            ),
            "memo_code": "8K45GHBNT6BQ6462",
            "clabe": "014027000000000008",
            "status": "processing",
            "payin_quote_id": "pq_000000000000",
            "instance_id": "in_000000000000",
            "tracking_transaction": {
                "step": "processing",
                "status": "failed",
                "external_id": "12345678",
                "completed_at": "2011-10-05T14:48:00.000Z",
                "sender_name": "John Doe Smith",
                "sender_tax_id": "123.456.789-10",
                "sender_bank_code": "00416968",
                "sender_account_number": "1234567890",
                "trace_number": "1234567890",
                "transaction_reference": "1234567890",
                "description": "Payment from John Doe Smith",
            },
            "tracking_payment": {
                "step": "on_hold",
                "provider_name": "blockchain",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_complete": {
                "step": "on_hold",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_partner_fee": {
                "step": "on_hold",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "created_at": "2021-01-01T00:00:00Z",
            "updated_at": "2021-01-01T00:00:00Z",
            "image_url": "https://example.com/image.png",
            "first_name": "John",
            "last_name": "Doe",
            "legal_name": "Company Name Inc.",
            "type": "individual",
            "payment_method": "pix",
            "sender_amount": 5240,
            "receiver_amount": 1010,
            "token": "USDC",
            "partner_fee_amount": 150,
            "total_fee_amount": 1.53,
            "commercial_quotation": 495,
            "blindpay_quotation": 505,
            "currency": "BRL",
            "billing_fee": 100,
            "name": "Wallet Display Name",
            "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
            "network": "polygon",
            "blindpay_bank_details": {
                "routing_number": "121145349",
                "account_number": "621327727210181",
                "account_type": "Business checking",
                "swift_bic_code": "CHASUS33",
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
                "beneficiary": {
                    "name": "BlindPay, Inc.",
                    "address_line_1": "8 The Green",
                    "address_line_2": "Dover, DE 19901",
                },
                "receiving_bank": {
                    "name": "Column NA - Brex",
                    "address_line_1": "1 Letterman Drive, Building A, Suite A4-700",
                    "address_line_2": "San Francisco, CA 94129",
                },
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payin_track, "error": None}

            response = self.blindpay.payins.get_track("pi_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_payin_track
            mock_request.assert_called_once_with("GET", "/e/payins/pi_000000000000")

    def test_export_payins(self):
        mocked_export_payins = [
            {
                "receiver_id": "re_000000000000",
                "id": "re_000000000000",
                "pix_code": (
                    "00020101021226790014br.gov.bcb.pix2557brcode.starkinfra.com/v2/"
                    "bcf07f6c4110454e9fd6f120bab13e835204000053039865802BR5915Blind Pay, Inc."
                    "6010Vila Velha62070503***6304BCAB"
                ),
                "memo_code": "8K45GHBNT6BQ6462",
                "clabe": "014027000000000008",
                "status": "processing",
                "payin_quote_id": "pq_000000000000",
                "instance_id": "in_000000000000",
                "tracking_transaction": {
                    "step": "processing",
                    "status": "failed",
                    "transaction_hash": "0x123...890",
                    "completed_at": "2011-10-05T14:48:00.000Z",
                },
                "tracking_payment": {
                    "step": "on_hold",
                    "provider_name": "blockchain",
                    "provider_transaction_id": "tx_123456789",
                    "provider_status": "confirmed",
                    "estimated_time_of_arrival": "2011-10-05T15:00:00.000Z",
                    "completed_at": "2011-10-05T14:48:00.000Z",
                },
                "tracking_complete": {
                    "step": "on_hold",
                    "status": "completed",
                    "transaction_hash": "0x123...890",
                    "completed_at": "2011-10-05T14:48:00.000Z",
                },
                "tracking_partner_fee": {
                    "step": "on_hold",
                    "transaction_hash": "0x123...890",
                    "completed_at": "2011-10-05T14:48:00.000Z",
                },
                "created_at": "2021-01-01T00:00:00Z",
                "updated_at": "2021-01-01T00:00:00Z",
                "image_url": "https://example.com/image.png",
                "first_name": "John",
                "last_name": "Doe",
                "legal_name": "Company Name Inc.",
                "type": "individual",
                "payment_method": "pix",
                "sender_amount": 5240,
                "receiver_amount": 1010,
                "token": "USDC",
                "partner_fee_amount": 150,
                "total_fee_amount": 1.53,
                "commercial_quotation": 495,
                "blindpay_quotation": 505,
                "currency": "BRL",
                "billing_fee": 100,
                "name": "Wallet Display Name",
                "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
                "network": "polygon",
                "blindpay_bank_details": {
                    "routing_number": "121145349",
                    "account_number": "621327727210181",
                    "account_type": "Business checking",
                    "swift_bic_code": "CHASUS33",
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
                    "beneficiary": {
                        "name": "BlindPay, Inc.",
                        "address_line_1": "8 The Green",
                        "address_line_2": "Dover, DE 19901",
                    },
                    "receiving_bank": {
                        "name": "Column NA - Brex",
                        "address_line_1": "1 Letterman Drive, Building A, Suite A4-700",
                        "address_line_2": "San Francisco, CA 94129",
                    },
                },
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_export_payins, "error": None}

            response = self.blindpay.payins.export(
                {
                    "status": "processing",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_export_payins
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/export/payins?status=processing")

    def test_create_evm_payin(self):
        mocked_evm_payin = {
            "id": "pi_000000000000",
            "status": "processing",
            "pix_code": (
                "00020101021226790014br.gov.bcb.pix2557brcode.starkinfra.com/v2/"
                "bcf07f6c4110454e9fd6f120bab13e835204000053039865802BR5915Blind Pay, Inc."
                "6010Vila Velha62070503***6304BCAB"
            ),
            "memo_code": "8K45GHBNT6BQ6462",
            "clabe": "014027000000000008",
            "tracking_complete": {
                "step": "on_hold",
                "status": "completed",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_payment": {
                "step": "on_hold",
                "provider_name": "blockchain",
                "provider_transaction_id": "tx_123456789",
                "provider_status": "confirmed",
                "estimated_time_of_arrival": "2011-10-05T15:00:00.000Z",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_transaction": {
                "step": "processing",
                "status": "failed",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_partner_fee": {
                "step": "on_hold",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "blindpay_bank_details": {
                "routing_number": "121145349",
                "account_number": "621327727210181",
                "account_type": "Business checking",
                "swift_bic_code": "CHASUS33",
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
                "beneficiary": {
                    "name": "BlindPay, Inc.",
                    "address_line_1": "8 The Green",
                    "address_line_2": "Dover, DE 19901",
                },
                "receiving_bank": {
                    "name": "Column NA - Brex",
                    "address_line_1": "1 Letterman Drive, Building A, Suite A4-700",
                    "address_line_2": "San Francisco, CA 94129",
                },
            },
            "receiver_id": "re_000000000000",
            "receiver_amount": 1010,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_evm_payin, "error": None}

            response = self.blindpay.payins.create_evm("pq_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_evm_payin
            mock_request.assert_called_once_with(
                "POST", "/instances/in_000000000000/payins/evm", {"payin_quote_id": "pq_000000000000"}
            )
