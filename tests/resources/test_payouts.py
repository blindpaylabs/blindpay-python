from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestPayouts:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_list_payouts(self):
        mocked_payouts = {
            "data": [
                {
                    "receiver_id": "re_000000000000",
                    "id": "pa_000000000000",
                    "status": "processing",
                    "sender_wallet_address": "0x123...890",
                    "signed_transaction": "AAA...Zey8y0A",
                    "quote_id": "qu_000000000000",
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
                        "provider_transaction_id": "0x123...890",
                        "provider_status": "canceled",
                        "estimated_time_of_arrival": "5_min",
                        "completed_at": "2011-10-05T14:48:00.000Z",
                    },
                    "tracking_liquidity": {
                        "step": "processing",
                        "provider_transaction_id": "0x123...890",
                        "provider_status": "deposited",
                        "estimated_time_of_arrival": "1_business_day",
                        "completed_at": "2011-10-05T14:48:00.000Z",
                    },
                    "tracking_complete": {
                        "step": "on_hold",
                        "status": "tokens_refunded",
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
                    "network": "sepolia",
                    "token": "USDC",
                    "description": "Memo code or description, only works with USD and BRL",
                    "sender_amount": 1010,
                    "receiver_amount": 5240,
                    "partner_fee_amount": 150,
                    "commercial_quotation": 495,
                    "blindpay_quotation": 485,
                    "total_fee_amount": 1.5,
                    "receiver_local_amount": 1000,
                    "currency": "BRL",
                    "transaction_document_file": "https://example.com/image.png",
                    "transaction_document_type": "invoice",
                    "transaction_document_id": "1234567890",
                    "name": "Bank Account Name",
                    "type": "wire",
                    "pix_key": "14947677768",
                    "account_number": "1001001234",
                    "routing_number": "012345678",
                    "country": "US",
                    "account_class": "individual",
                    "address_line_1": "Address line 1",
                    "address_line_2": "Address line 2",
                    "city": "City",
                    "state_province_region": "State/Province/Region",
                    "postal_code": "Postal code",
                    "account_type": "checking",
                    "ach_cop_beneficiary_first_name": "Fernando",
                    "ach_cop_bank_account": "12345678",
                    "ach_cop_bank_code": "051",
                    "ach_cop_beneficiary_last_name": "Guzman Alarcón",
                    "ach_cop_document_id": "1661105408",
                    "ach_cop_document_type": "CC",
                    "ach_cop_email": "fernando.guzman@gmail.com",
                    "beneficiary_name": "Individual full name or business name",
                    "spei_clabe": "5482347403740546",
                    "spei_protocol": "clabe",
                    "spei_institution_code": "40002",
                    "swift_beneficiary_country": "MX",
                    "swift_code_bic": "123456789",
                    "swift_account_holder_name": "John Doe",
                    "swift_account_number_iban": "123456789",
                    "transfers_account": "BM123123123123",
                    "transfers_type": "CVU",
                    "has_virtual_account": True,
                },
            ],
            "pagination": {
                "has_more": True,
                "next_page": 3,
                "prev_page": 1,
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payouts, "error": None}

            response = await self.blindpay.payouts.list()

            assert response["error"] is None
            assert response["data"] == mocked_payouts
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/payouts")

    @pytest.mark.asyncio
    async def test_get_payout(self):
        mocked_payout = {
            "receiver_id": "re_000000000000",
            "id": "pa_000000000000",
            "status": "processing",
            "sender_wallet_address": "0x123...890",
            "signed_transaction": "AAA...Zey8y0A",
            "quote_id": "qu_000000000000",
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
                "provider_transaction_id": "0x123...890",
                "provider_status": "canceled",
                "estimated_time_of_arrival": "5_min",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_liquidity": {
                "step": "processing",
                "provider_transaction_id": "0x123...890",
                "provider_status": "deposited",
                "estimated_time_of_arrival": "1_business_day",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_complete": {
                "step": "on_hold",
                "status": "tokens_refunded",
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
            "network": "sepolia",
            "token": "USDC",
            "description": "Memo code or description, only works with USD and BRL",
            "sender_amount": 1010,
            "receiver_amount": 5240,
            "partner_fee_amount": 150,
            "commercial_quotation": 495,
            "blindpay_quotation": 485,
            "total_fee_amount": 1.5,
            "receiver_local_amount": 1000,
            "currency": "BRL",
            "transaction_document_file": "https://example.com/image.png",
            "transaction_document_type": "invoice",
            "transaction_document_id": "1234567890",
            "name": "Bank Account Name",
            "type": "wire",
            "pix_key": "14947677768",
            "account_number": "1001001234",
            "routing_number": "012345678",
            "country": "US",
            "account_class": "individual",
            "address_line_1": "Address line 1",
            "address_line_2": "Address line 2",
            "city": "City",
            "state_province_region": "State/Province/Region",
            "postal_code": "Postal code",
            "account_type": "checking",
            "ach_cop_beneficiary_first_name": "Fernando",
            "ach_cop_bank_account": "12345678",
            "ach_cop_bank_code": "051",
            "ach_cop_beneficiary_last_name": "Guzman Alarcón",
            "ach_cop_document_id": "1661105408",
            "ach_cop_document_type": "CC",
            "ach_cop_email": "fernando.guzman@gmail.com",
            "beneficiary_name": "Individual full name or business name",
            "spei_clabe": "5482347403740546",
            "spei_protocol": "clabe",
            "spei_institution_code": "40002",
            "swift_beneficiary_country": "MX",
            "swift_code_bic": "123456789",
            "swift_account_holder_name": "John Doe",
            "swift_account_number_iban": "123456789",
            "transfers_account": "BM123123123123",
            "transfers_type": "CVU",
            "has_virtual_account": True,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payout, "error": None}

            response = await self.blindpay.payouts.get("pa_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_payout
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/payouts/pa_000000000000")

    @pytest.mark.asyncio
    async def test_export_payouts(self):
        mocked_export_payouts = [
            {
                "receiver_id": "re_000000000000",
                "id": "pa_000000000000",
                "status": "processing",
                "sender_wallet_address": "0x123...890",
                "signed_transaction": "AAA...Zey8y0A",
                "quote_id": "qu_000000000000",
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
                    "provider_transaction_id": "0x123...890",
                    "provider_status": "canceled",
                    "estimated_time_of_arrival": "5_min",
                    "completed_at": "2011-10-05T14:48:00.000Z",
                },
                "tracking_liquidity": {
                    "step": "processing",
                    "provider_transaction_id": "0x123...890",
                    "provider_status": "deposited",
                    "estimated_time_of_arrival": "1_business_day",
                    "completed_at": "2011-10-05T14:48:00.000Z",
                },
                "tracking_complete": {
                    "step": "on_hold",
                    "status": "tokens_refunded",
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
                "network": "sepolia",
                "token": "USDC",
                "description": "Memo code or description, only works with USD and BRL",
                "sender_amount": 1010,
                "receiver_amount": 5240,
                "partner_fee_amount": 150,
                "commercial_quotation": 495,
                "blindpay_quotation": 485,
                "total_fee_amount": 1.5,
                "receiver_local_amount": 1000,
                "currency": "BRL",
                "transaction_document_file": "https://example.com/image.png",
                "transaction_document_type": "invoice",
                "transaction_document_id": "1234567890",
                "name": "Bank Account Name",
                "type": "wire",
                "pix_key": "14947677768",
                "account_number": "1001001234",
                "routing_number": "012345678",
                "country": "US",
                "account_class": "individual",
                "address_line_1": "Address line 1",
                "address_line_2": "Address line 2",
                "city": "City",
                "state_province_region": "State/Province/Region",
                "postal_code": "Postal code",
                "account_type": "checking",
                "ach_cop_beneficiary_first_name": "Fernando",
                "ach_cop_bank_account": "12345678",
                "ach_cop_bank_code": "051",
                "ach_cop_beneficiary_last_name": "Guzman Alarcón",
                "ach_cop_document_id": "1661105408",
                "ach_cop_document_type": "CC",
                "ach_cop_email": "fernando.guzman@gmail.com",
                "beneficiary_name": "Individual full name or business name",
                "spei_clabe": "5482347403740546",
                "spei_protocol": "clabe",
                "spei_institution_code": "40002",
                "swift_beneficiary_country": "MX",
                "swift_code_bic": "123456789",
                "swift_account_holder_name": "John Doe",
                "swift_account_number_iban": "123456789",
                "transfers_account": "BM123123123123",
                "transfers_type": "CVU",
                "has_virtual_account": True,
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_export_payouts, "error": None}

            response = await self.blindpay.payouts.export()

            assert response["error"] is None
            assert response["data"] == mocked_export_payouts
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/export/payouts")

    @pytest.mark.asyncio
    async def test_get_payout_track(self):
        mocked_payout_track = {
            "receiver_id": "re_000000000000",
            "id": "pa_000000000000",
            "status": "processing",
            "sender_wallet_address": "0x123...890",
            "signed_transaction": "AAA...Zey8y0A",
            "quote_id": "qu_000000000000",
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
                "provider_transaction_id": "0x123...890",
                "provider_status": "canceled",
                "estimated_time_of_arrival": "5_min",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_liquidity": {
                "step": "processing",
                "provider_transaction_id": "0x123...890",
                "provider_status": "deposited",
                "estimated_time_of_arrival": "1_business_day",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_complete": {
                "step": "on_hold",
                "status": "tokens_refunded",
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
            "network": "sepolia",
            "token": "USDC",
            "description": "Memo code or description, only works with USD and BRL",
            "sender_amount": 1010,
            "receiver_amount": 5240,
            "partner_fee_amount": 150,
            "commercial_quotation": 495,
            "blindpay_quotation": 485,
            "total_fee_amount": 1.5,
            "receiver_local_amount": 1000,
            "currency": "BRL",
            "transaction_document_file": "https://example.com/image.png",
            "transaction_document_type": "invoice",
            "transaction_document_id": "1234567890",
            "name": "Bank Account Name",
            "type": "wire",
            "pix_key": "14947677768",
            "account_number": "1001001234",
            "routing_number": "012345678",
            "country": "US",
            "account_class": "individual",
            "address_line_1": "Address line 1",
            "address_line_2": "Address line 2",
            "city": "City",
            "state_province_region": "State/Province/Region",
            "postal_code": "Postal code",
            "account_type": "checking",
            "ach_cop_beneficiary_first_name": "Fernando",
            "ach_cop_bank_account": "12345678",
            "ach_cop_bank_code": "051",
            "ach_cop_beneficiary_last_name": "Guzman Alarcón",
            "ach_cop_document_id": "1661105408",
            "ach_cop_document_type": "CC",
            "ach_cop_email": "fernando.guzman@gmail.com",
            "beneficiary_name": "Individual full name or business name",
            "spei_clabe": "5482347403740546",
            "spei_protocol": "clabe",
            "spei_institution_code": "40002",
            "swift_beneficiary_country": "MX",
            "swift_code_bic": "123456789",
            "swift_account_holder_name": "John Doe",
            "swift_account_number_iban": "123456789",
            "transfers_account": "BM123123123123",
            "transfers_type": "CVU",
            "has_virtual_account": True,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payout_track, "error": None}

            response = await self.blindpay.payouts.get_track("pa_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_payout_track
            mock_request.assert_called_once_with("GET", "/e/payouts/pa_000000000000")

    @pytest.mark.asyncio
    async def test_authorize_stellar_token(self):
        mocked_authorize_token = {
            "transaction_hash": "string",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_authorize_token, "error": None}

            response = await self.blindpay.payouts.authorize_stellar_token(
                {
                    "quote_id": "qu_000000000000",
                    "sender_wallet_address": "0x123...890",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_authorize_token
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/payouts/stellar/authorize",
                {
                    "quote_id": "qu_000000000000",
                    "sender_wallet_address": "0x123...890",
                },
            )

    @pytest.mark.asyncio
    async def test_create_stellar_payout(self):
        mocked_stellar_payout = {
            "id": "pa_000000000000",
            "status": "processing",
            "sender_wallet_address": "0x123...890",
            "tracking_complete": {
                "step": "on_hold",
                "status": "tokens_refunded",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_payment": {
                "step": "on_hold",
                "provider_name": "blockchain",
                "provider_transaction_id": "0x123...890",
                "provider_status": "canceled",
                "estimated_time_of_arrival": "5_min",
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
            "tracking_liquidity": {
                "step": "processing",
                "provider_transaction_id": "0x123...890",
                "provider_status": "deposited",
                "estimated_time_of_arrival": "1_business_day",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "receiver_id": "re_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_stellar_payout, "error": None}

            response = await self.blindpay.payouts.create_stellar(
                {
                    "quote_id": "qu_000000000000",
                    "sender_wallet_address": "0x123...890",
                    "signed_transaction": "signed_xdr_string",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_stellar_payout
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/payouts/stellar",
                {
                    "quote_id": "qu_000000000000",
                    "sender_wallet_address": "0x123...890",
                    "signed_transaction": "signed_xdr_string",
                },
            )

    @pytest.mark.asyncio
    async def test_create_evm_payout(self):
        mocked_evm_payout = {
            "id": "pa_000000000000",
            "status": "processing",
            "sender_wallet_address": "0x123...890",
            "tracking_complete": {
                "step": "on_hold",
                "status": "tokens_refunded",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_payment": {
                "step": "on_hold",
                "provider_name": "blockchain",
                "provider_transaction_id": "0x123...890",
                "provider_status": "canceled",
                "estimated_time_of_arrival": "5_min",
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
            "tracking_liquidity": {
                "step": "processing",
                "provider_transaction_id": "0x123...890",
                "provider_status": "deposited",
                "estimated_time_of_arrival": "1_business_day",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "receiver_id": "re_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_evm_payout, "error": None}

            response = await self.blindpay.payouts.create_evm(
                {
                    "quote_id": "qu_000000000000",
                    "sender_wallet_address": "0x123...890",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_evm_payout
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/payouts/evm",
                {
                    "quote_id": "qu_000000000000",
                    "sender_wallet_address": "0x123...890",
                },
            )


class TestPayoutsSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_list_payouts(self):
        mocked_payouts = {
            "data": [
                {
                    "receiver_id": "re_000000000000",
                    "id": "pa_000000000000",
                    "status": "processing",
                    "sender_wallet_address": "0x123...890",
                    "signed_transaction": "AAA...Zey8y0A",
                    "quote_id": "qu_000000000000",
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
                        "provider_transaction_id": "0x123...890",
                        "provider_status": "canceled",
                        "estimated_time_of_arrival": "5_min",
                        "completed_at": "2011-10-05T14:48:00.000Z",
                    },
                    "tracking_liquidity": {
                        "step": "processing",
                        "provider_transaction_id": "0x123...890",
                        "provider_status": "deposited",
                        "estimated_time_of_arrival": "1_business_day",
                        "completed_at": "2011-10-05T14:48:00.000Z",
                    },
                    "tracking_complete": {
                        "step": "on_hold",
                        "status": "tokens_refunded",
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
                    "network": "sepolia",
                    "token": "USDC",
                    "description": "Memo code or description, only works with USD and BRL",
                    "sender_amount": 1010,
                    "receiver_amount": 5240,
                    "partner_fee_amount": 150,
                    "commercial_quotation": 495,
                    "blindpay_quotation": 485,
                    "total_fee_amount": 1.5,
                    "receiver_local_amount": 1000,
                    "currency": "BRL",
                    "transaction_document_file": "https://example.com/image.png",
                    "transaction_document_type": "invoice",
                    "transaction_document_id": "1234567890",
                    "name": "Bank Account Name",
                    "type": "wire",
                    "pix_key": "14947677768",
                    "account_number": "1001001234",
                    "routing_number": "012345678",
                    "country": "US",
                    "account_class": "individual",
                    "address_line_1": "Address line 1",
                    "address_line_2": "Address line 2",
                    "city": "City",
                    "state_province_region": "State/Province/Region",
                    "postal_code": "Postal code",
                    "account_type": "checking",
                    "ach_cop_beneficiary_first_name": "Fernando",
                    "ach_cop_bank_account": "12345678",
                    "ach_cop_bank_code": "051",
                    "ach_cop_beneficiary_last_name": "Guzman Alarcón",
                    "ach_cop_document_id": "1661105408",
                    "ach_cop_document_type": "CC",
                    "ach_cop_email": "fernando.guzman@gmail.com",
                    "beneficiary_name": "Individual full name or business name",
                    "spei_clabe": "5482347403740546",
                    "spei_protocol": "clabe",
                    "spei_institution_code": "40002",
                    "swift_beneficiary_country": "MX",
                    "swift_code_bic": "123456789",
                    "swift_account_holder_name": "John Doe",
                    "swift_account_number_iban": "123456789",
                    "transfers_account": "BM123123123123",
                    "transfers_type": "CVU",
                    "has_virtual_account": True,
                },
            ],
            "pagination": {
                "has_more": True,
                "next_page": 3,
                "prev_page": 1,
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payouts, "error": None}

            response = self.blindpay.payouts.list()

            assert response["error"] is None
            assert response["data"] == mocked_payouts
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/payouts")

    def test_get_payout(self):
        mocked_payout = {
            "receiver_id": "re_000000000000",
            "id": "pa_000000000000",
            "status": "processing",
            "sender_wallet_address": "0x123...890",
            "signed_transaction": "AAA...Zey8y0A",
            "quote_id": "qu_000000000000",
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
                "provider_transaction_id": "0x123...890",
                "provider_status": "canceled",
                "estimated_time_of_arrival": "5_min",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_liquidity": {
                "step": "processing",
                "provider_transaction_id": "0x123...890",
                "provider_status": "deposited",
                "estimated_time_of_arrival": "1_business_day",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_complete": {
                "step": "on_hold",
                "status": "tokens_refunded",
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
            "network": "sepolia",
            "token": "USDC",
            "description": "Memo code or description, only works with USD and BRL",
            "sender_amount": 1010,
            "receiver_amount": 5240,
            "partner_fee_amount": 150,
            "commercial_quotation": 495,
            "blindpay_quotation": 485,
            "total_fee_amount": 1.5,
            "receiver_local_amount": 1000,
            "currency": "BRL",
            "transaction_document_file": "https://example.com/image.png",
            "transaction_document_type": "invoice",
            "transaction_document_id": "1234567890",
            "name": "Bank Account Name",
            "type": "wire",
            "pix_key": "14947677768",
            "account_number": "1001001234",
            "routing_number": "012345678",
            "country": "US",
            "account_class": "individual",
            "address_line_1": "Address line 1",
            "address_line_2": "Address line 2",
            "city": "City",
            "state_province_region": "State/Province/Region",
            "postal_code": "Postal code",
            "account_type": "checking",
            "ach_cop_beneficiary_first_name": "Fernando",
            "ach_cop_bank_account": "12345678",
            "ach_cop_bank_code": "051",
            "ach_cop_beneficiary_last_name": "Guzman Alarcón",
            "ach_cop_document_id": "1661105408",
            "ach_cop_document_type": "CC",
            "ach_cop_email": "fernando.guzman@gmail.com",
            "beneficiary_name": "Individual full name or business name",
            "spei_clabe": "5482347403740546",
            "spei_protocol": "clabe",
            "spei_institution_code": "40002",
            "swift_beneficiary_country": "MX",
            "swift_code_bic": "123456789",
            "swift_account_holder_name": "John Doe",
            "swift_account_number_iban": "123456789",
            "transfers_account": "BM123123123123",
            "transfers_type": "CVU",
            "has_virtual_account": True,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payout, "error": None}

            response = self.blindpay.payouts.get("pa_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_payout
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/payouts/pa_000000000000")

    def test_export_payouts(self):
        mocked_export_payouts = [
            {
                "receiver_id": "re_000000000000",
                "id": "pa_000000000000",
                "status": "processing",
                "sender_wallet_address": "0x123...890",
                "signed_transaction": "AAA...Zey8y0A",
                "quote_id": "qu_000000000000",
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
                    "provider_transaction_id": "0x123...890",
                    "provider_status": "canceled",
                    "estimated_time_of_arrival": "5_min",
                    "completed_at": "2011-10-05T14:48:00.000Z",
                },
                "tracking_liquidity": {
                    "step": "processing",
                    "provider_transaction_id": "0x123...890",
                    "provider_status": "deposited",
                    "estimated_time_of_arrival": "1_business_day",
                    "completed_at": "2011-10-05T14:48:00.000Z",
                },
                "tracking_complete": {
                    "step": "on_hold",
                    "status": "tokens_refunded",
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
                "network": "sepolia",
                "token": "USDC",
                "description": "Memo code or description, only works with USD and BRL",
                "sender_amount": 1010,
                "receiver_amount": 5240,
                "partner_fee_amount": 150,
                "commercial_quotation": 495,
                "blindpay_quotation": 485,
                "total_fee_amount": 1.5,
                "receiver_local_amount": 1000,
                "currency": "BRL",
                "transaction_document_file": "https://example.com/image.png",
                "transaction_document_type": "invoice",
                "transaction_document_id": "1234567890",
                "name": "Bank Account Name",
                "type": "wire",
                "pix_key": "14947677768",
                "account_number": "1001001234",
                "routing_number": "012345678",
                "country": "US",
                "account_class": "individual",
                "address_line_1": "Address line 1",
                "address_line_2": "Address line 2",
                "city": "City",
                "state_province_region": "State/Province/Region",
                "postal_code": "Postal code",
                "account_type": "checking",
                "ach_cop_beneficiary_first_name": "Fernando",
                "ach_cop_bank_account": "12345678",
                "ach_cop_bank_code": "051",
                "ach_cop_beneficiary_last_name": "Guzman Alarcón",
                "ach_cop_document_id": "1661105408",
                "ach_cop_document_type": "CC",
                "ach_cop_email": "fernando.guzman@gmail.com",
                "beneficiary_name": "Individual full name or business name",
                "spei_clabe": "5482347403740546",
                "spei_protocol": "clabe",
                "spei_institution_code": "40002",
                "swift_beneficiary_country": "MX",
                "swift_code_bic": "123456789",
                "swift_account_holder_name": "John Doe",
                "swift_account_number_iban": "123456789",
                "transfers_account": "BM123123123123",
                "transfers_type": "CVU",
                "has_virtual_account": True,
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_export_payouts, "error": None}

            response = self.blindpay.payouts.export()

            assert response["error"] is None
            assert response["data"] == mocked_export_payouts
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/export/payouts")

    def test_get_payout_track(self):
        mocked_payout_track = {
            "receiver_id": "re_000000000000",
            "id": "pa_000000000000",
            "status": "processing",
            "sender_wallet_address": "0x123...890",
            "signed_transaction": "AAA...Zey8y0A",
            "quote_id": "qu_000000000000",
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
                "provider_transaction_id": "0x123...890",
                "provider_status": "canceled",
                "estimated_time_of_arrival": "5_min",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_liquidity": {
                "step": "processing",
                "provider_transaction_id": "0x123...890",
                "provider_status": "deposited",
                "estimated_time_of_arrival": "1_business_day",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_complete": {
                "step": "on_hold",
                "status": "tokens_refunded",
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
            "network": "sepolia",
            "token": "USDC",
            "description": "Memo code or description, only works with USD and BRL",
            "sender_amount": 1010,
            "receiver_amount": 5240,
            "partner_fee_amount": 150,
            "commercial_quotation": 495,
            "blindpay_quotation": 485,
            "total_fee_amount": 1.5,
            "receiver_local_amount": 1000,
            "currency": "BRL",
            "transaction_document_file": "https://example.com/image.png",
            "transaction_document_type": "invoice",
            "transaction_document_id": "1234567890",
            "name": "Bank Account Name",
            "type": "wire",
            "pix_key": "14947677768",
            "account_number": "1001001234",
            "routing_number": "012345678",
            "country": "US",
            "account_class": "individual",
            "address_line_1": "Address line 1",
            "address_line_2": "Address line 2",
            "city": "City",
            "state_province_region": "State/Province/Region",
            "postal_code": "Postal code",
            "account_type": "checking",
            "ach_cop_beneficiary_first_name": "Fernando",
            "ach_cop_bank_account": "12345678",
            "ach_cop_bank_code": "051",
            "ach_cop_beneficiary_last_name": "Guzman Alarcón",
            "ach_cop_document_id": "1661105408",
            "ach_cop_document_type": "CC",
            "ach_cop_email": "fernando.guzman@gmail.com",
            "beneficiary_name": "Individual full name or business name",
            "spei_clabe": "5482347403740546",
            "spei_protocol": "clabe",
            "spei_institution_code": "40002",
            "swift_beneficiary_country": "MX",
            "swift_code_bic": "123456789",
            "swift_account_holder_name": "John Doe",
            "swift_account_number_iban": "123456789",
            "transfers_account": "BM123123123123",
            "transfers_type": "CVU",
            "has_virtual_account": True,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_payout_track, "error": None}

            response = self.blindpay.payouts.get_track("pa_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_payout_track
            mock_request.assert_called_once_with("GET", "/e/payouts/pa_000000000000")

    def test_authorize_stellar_token(self):
        mocked_authorize_token = {
            "transaction_hash": "string",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_authorize_token, "error": None}

            response = self.blindpay.payouts.authorize_stellar_token(
                {
                    "quote_id": "qu_000000000000",
                    "sender_wallet_address": "0x123...890",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_authorize_token
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/payouts/stellar/authorize",
                {
                    "quote_id": "qu_000000000000",
                    "sender_wallet_address": "0x123...890",
                },
            )

    def test_create_stellar_payout(self):
        mocked_stellar_payout = {
            "id": "pa_000000000000",
            "status": "processing",
            "sender_wallet_address": "0x123...890",
            "tracking_complete": {
                "step": "on_hold",
                "status": "tokens_refunded",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_payment": {
                "step": "on_hold",
                "provider_name": "blockchain",
                "provider_transaction_id": "0x123...890",
                "provider_status": "canceled",
                "estimated_time_of_arrival": "5_min",
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
            "tracking_liquidity": {
                "step": "processing",
                "provider_transaction_id": "0x123...890",
                "provider_status": "deposited",
                "estimated_time_of_arrival": "1_business_day",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "receiver_id": "re_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_stellar_payout, "error": None}

            response = self.blindpay.payouts.create_stellar(
                {
                    "quote_id": "qu_000000000000",
                    "sender_wallet_address": "0x123...890",
                    "signed_transaction": "signed_xdr_string",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_stellar_payout
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/payouts/stellar",
                {
                    "quote_id": "qu_000000000000",
                    "sender_wallet_address": "0x123...890",
                    "signed_transaction": "signed_xdr_string",
                },
            )

    def test_create_evm_payout(self):
        mocked_evm_payout = {
            "id": "pa_000000000000",
            "status": "processing",
            "sender_wallet_address": "0x123...890",
            "tracking_complete": {
                "step": "on_hold",
                "status": "tokens_refunded",
                "transaction_hash": "0x123...890",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "tracking_payment": {
                "step": "on_hold",
                "provider_name": "blockchain",
                "provider_transaction_id": "0x123...890",
                "provider_status": "canceled",
                "estimated_time_of_arrival": "5_min",
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
            "tracking_liquidity": {
                "step": "processing",
                "provider_transaction_id": "0x123...890",
                "provider_status": "deposited",
                "estimated_time_of_arrival": "1_business_day",
                "completed_at": "2011-10-05T14:48:00.000Z",
            },
            "receiver_id": "re_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_evm_payout, "error": None}

            response = self.blindpay.payouts.create_evm(
                {
                    "quote_id": "qu_000000000000",
                    "sender_wallet_address": "0x123...890",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_evm_payout
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/payouts/evm",
                {
                    "quote_id": "qu_000000000000",
                    "sender_wallet_address": "0x123...890",
                },
            )
