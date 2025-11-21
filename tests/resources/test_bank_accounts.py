from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestBankAccounts:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_create_pix_bank_account(self):
        mocked_pix_account = {
            "id": "ba_000000000000",
            "type": "pix",
            "name": "PIX Account",
            "pix_key": "14947677768",
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_pix_account, "error": None}

            response = await self.blindpay.receivers.bank_accounts.create_pix(
                {
                    "receiver_id": "re_000000000000",
                    "name": "PIX Account",
                    "pix_key": "14947677768",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_pix_account

    @pytest.mark.asyncio
    async def test_create_argentina_transfers_bank_account(self):
        mocked_argentina_transfers_account = {
            "id": "ba_000000000000",
            "type": "transfers_bitso",
            "name": "Argentina Transfers Account",
            "beneficiary_name": "Individual full name or business name",
            "transfers_type": "CVU",
            "transfers_account": "BM123123123123",
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_argentina_transfers_account, "error": None}

            response = await self.blindpay.receivers.bank_accounts.create_argentina_transfers(
                {
                    "receiver_id": "re_000000000000",
                    "name": "Argentina Transfers Account",
                    "beneficiary_name": "Individual full name or business name",
                    "transfers_type": "CVU",
                    "transfers_account": "BM123123123123",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_argentina_transfers_account

    @pytest.mark.asyncio
    async def test_create_spei_bank_account(self):
        mocked_spei_account = {
            "id": "ba_000000000000",
            "type": "spei_bitso",
            "name": "SPEI Account",
            "beneficiary_name": "Individual full name or business name",
            "spei_protocol": "clabe",
            "spei_institution_code": "40002",
            "spei_clabe": "5482347403740546",
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_spei_account, "error": None}

            response = await self.blindpay.receivers.bank_accounts.create_spei(
                {
                    "receiver_id": "re_000000000000",
                    "name": "SPEI Account",
                    "beneficiary_name": "Individual full name or business name",
                    "spei_protocol": "clabe",
                    "spei_institution_code": "40002",
                    "spei_clabe": "5482347403740546",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_spei_account

    @pytest.mark.asyncio
    async def test_create_colombia_ach_bank_account(self):
        mocked_colombia_ach_account = {
            "id": "ba_000000000000",
            "type": "ach_cop_bitso",
            "name": "Colombia ACH Account",
            "account_type": "checking",
            "ach_cop_beneficiary_first_name": "Fernando",
            "ach_cop_beneficiary_last_name": "Guzman Alarcón",
            "ach_cop_document_id": "1661105408",
            "ach_cop_document_type": "CC",
            "ach_cop_email": "fernando.guzman@gmail.com",
            "ach_cop_bank_code": "051",
            "ach_cop_bank_account": "12345678",
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_colombia_ach_account, "error": None}

            response = await self.blindpay.receivers.bank_accounts.create_colombia_ach(
                {
                    "receiver_id": "re_000000000000",
                    "name": "Colombia ACH Account",
                    "account_type": "checking",
                    "ach_cop_beneficiary_first_name": "Fernando",
                    "ach_cop_beneficiary_last_name": "Guzman Alarcón",
                    "ach_cop_document_id": "1661105408",
                    "ach_cop_document_type": "CC",
                    "ach_cop_email": "fernando.guzman@gmail.com",
                    "ach_cop_bank_code": "051",
                    "ach_cop_bank_account": "12345678",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_colombia_ach_account

    @pytest.mark.asyncio
    async def test_create_ach_bank_account(self):
        mocked_ach_account = {
            "id": "ba_000000000000",
            "type": "ach",
            "name": "ACH Account",
            "beneficiary_name": "Individual full name or business name",
            "routing_number": "012345678",
            "account_number": "1001001234",
            "account_type": "checking",
            "account_class": "individual",
            "address_line_1": None,
            "address_line_2": None,
            "city": None,
            "state_province_region": None,
            "country": None,
            "postal_code": None,
            "ach_cop_beneficiary_first_name": None,
            "ach_cop_beneficiary_last_name": None,
            "ach_cop_document_id": None,
            "ach_cop_document_type": None,
            "ach_cop_email": None,
            "ach_cop_bank_code": None,
            "ach_cop_bank_account": None,
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_ach_account, "error": None}

            response = await self.blindpay.receivers.bank_accounts.create_ach(
                {
                    "receiver_id": "re_000000000000",
                    "name": "ACH Account",
                    "account_class": "individual",
                    "account_number": "1001001234",
                    "account_type": "checking",
                    "beneficiary_name": "Individual full name or business name",
                    "routing_number": "012345678",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_ach_account

    @pytest.mark.asyncio
    async def test_create_wire_bank_account(self):
        mocked_wire_account = {
            "id": "ba_000000000000",
            "type": "wire",
            "name": "Wire Account",
            "beneficiary_name": "Individual full name or business name",
            "routing_number": "012345678",
            "account_number": "1001001234",
            "address_line_1": "Address line 1",
            "address_line_2": "Address line 2",
            "city": "City",
            "state_province_region": "State/Province/Region",
            "country": "US",
            "postal_code": "Postal code",
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wire_account, "error": None}

            response = await self.blindpay.receivers.bank_accounts.create_wire(
                {
                    "receiver_id": "re_000000000000",
                    "name": "Wire Account",
                    "account_number": "1001001234",
                    "beneficiary_name": "Individual full name or business name",
                    "routing_number": "012345678",
                    "address_line_1": "Address line 1",
                    "address_line_2": "Address line 2",
                    "city": "City",
                    "state_province_region": "State/Province/Region",
                    "country": "US",
                    "postal_code": "Postal code",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_wire_account

    @pytest.mark.asyncio
    async def test_create_international_swift_bank_account(self):
        mocked_international_swift_account = {
            "id": "ba_000000000000",
            "type": "international_swift",
            "name": "International Swift Account",
            "beneficiary_name": None,
            "address_line_1": None,
            "address_line_2": None,
            "city": None,
            "state_province_region": None,
            "country": None,
            "postal_code": None,
            "swift_code_bic": "123456789",
            "swift_account_holder_name": "John Doe",
            "swift_account_number_iban": "123456789",
            "swift_beneficiary_address_line_1": ("123 Main Street, Suite 100, Downtown District, City Center CP 12345"),
            "swift_beneficiary_address_line_2": None,
            "swift_beneficiary_country": "MX",
            "swift_beneficiary_city": "City",
            "swift_beneficiary_state_province_region": "District",
            "swift_beneficiary_postal_code": "11530",
            "swift_bank_name": "Banco Regional SA",
            "swift_bank_address_line_1": "123 Main Street, Suite 100, Downtown District, City Center CP 12345",
            "swift_bank_address_line_2": None,
            "swift_bank_country": "MX",
            "swift_bank_city": "City",
            "swift_bank_state_province_region": "District",
            "swift_bank_postal_code": "11530",
            "swift_intermediary_bank_swift_code_bic": None,
            "swift_intermediary_bank_account_number_iban": None,
            "swift_intermediary_bank_name": None,
            "swift_intermediary_bank_country": None,
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_international_swift_account, "error": None}

            response = await self.blindpay.receivers.bank_accounts.create_international_swift(
                {
                    "receiver_id": "re_000000000000",
                    "name": "International Swift Account",
                    "swift_account_holder_name": "John Doe",
                    "swift_account_number_iban": "123456789",
                    "swift_bank_address_line_1": "123 Main Street, Suite 100, Downtown District, City Center CP 12345",
                    "swift_bank_address_line_2": None,
                    "swift_bank_city": "City",
                    "swift_bank_country": "MX",
                    "swift_bank_name": "Banco Regional SA",
                    "swift_bank_postal_code": "11530",
                    "swift_bank_state_province_region": "District",
                    "swift_beneficiary_address_line_1": (
                        "123 Main Street, Suite 100, Downtown District, City Center CP 12345"
                    ),
                    "swift_beneficiary_address_line_2": None,
                    "swift_beneficiary_city": "City",
                    "swift_beneficiary_country": "MX",
                    "swift_beneficiary_postal_code": "11530",
                    "swift_beneficiary_state_province_region": "District",
                    "swift_code_bic": "123456789",
                    "swift_intermediary_bank_account_number_iban": None,
                    "swift_intermediary_bank_country": None,
                    "swift_intermediary_bank_name": None,
                    "swift_intermediary_bank_swift_code_bic": None,
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_international_swift_account

    @pytest.mark.asyncio
    async def test_create_rtp_bank_account(self):
        mocked_rtp_account = {
            "id": "ba_JW5ZtlKMlgS1",
            "type": "rtp",
            "name": "John Doe RTP",
            "beneficiary_name": "John Doe",
            "routing_number": "121000358",
            "account_number": "325203027578",
            "address_line_1": "Street of the fools",
            "address_line_2": None,
            "city": "Fools City",
            "state_province_region": "FL",
            "country": "US",
            "postal_code": "22599",
            "created_at": "2025-09-30T04:23:30.823Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_rtp_account, "error": None}

            response = await self.blindpay.receivers.bank_accounts.create_rtp(
                {
                    "receiver_id": "re_000000000000",
                    "name": "John Doe RTP",
                    "beneficiary_name": "John Doe",
                    "routing_number": "121000358",
                    "account_number": "325203027578",
                    "address_line_1": "Street of the fools",
                    "address_line_2": None,
                    "city": "Fools City",
                    "state_province_region": "FL",
                    "country": "US",
                    "postal_code": "22599",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_rtp_account

    @pytest.mark.asyncio
    async def test_get_bank_account(self):
        mocked_bank_account = {
            "id": "ba_000000000000",
            "receiver_id": "rcv_123",
            "account_holder_name": "Individual full name or business name",
            "account_number": "1001001234",
            "routing_number": "012345678",
            "account_type": "checking",
            "bank_name": "Bank Name",
            "swift_code": "123456789",
            "iban": None,
            "is_primary": False,
            "created_at": "2021-01-01T00:00:00Z",
            "updated_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_bank_account, "error": None}

            response = await self.blindpay.receivers.bank_accounts.get("re_000000000000", "ba_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_bank_account

    @pytest.mark.asyncio
    async def test_list_bank_accounts(self):
        mocked_bank_accounts = {
            "data": [
                {
                    "id": "ba_000000000000",
                    "type": "wire",
                    "name": "Bank Account Name",
                    "pix_key": "14947677768",
                    "beneficiary_name": "Individual full name or business name",
                    "routing_number": "012345678",
                    "account_number": "1001001234",
                    "account_type": "checking",
                    "account_class": "individual",
                    "address_line_1": "Address line 1",
                    "address_line_2": "Address line 2",
                    "city": "City",
                    "state_province_region": "State/Province/Region",
                    "country": "US",
                    "postal_code": "Postal code",
                    "spei_protocol": "clabe",
                    "spei_institution_code": "40002",
                    "spei_clabe": "5482347403740546",
                    "transfers_type": "CVU",
                    "transfers_account": "BM123123123123",
                    "ach_cop_beneficiary_first_name": "Fernando",
                    "ach_cop_beneficiary_last_name": "Guzman Alarcón",
                    "ach_cop_document_id": "1661105408",
                    "ach_cop_document_type": "CC",
                    "ach_cop_email": "fernando.guzman@gmail.com",
                    "ach_cop_bank_code": "051",
                    "ach_cop_bank_account": "12345678",
                    "swift_code_bic": "123456789",
                    "swift_account_holder_name": "John Doe",
                    "swift_account_number_iban": "123456789",
                    "swift_beneficiary_address_line_1": (
                        "123 Main Street, Suite 100, Downtown District, City Center CP 12345"
                    ),
                    "swift_beneficiary_address_line_2": (
                        "456 Oak Avenue, Building 7, Financial District, Business Center CP 54321"
                    ),
                    "swift_beneficiary_country": "MX",
                    "swift_beneficiary_city": "City",
                    "swift_beneficiary_state_province_region": "District",
                    "swift_beneficiary_postal_code": "11530",
                    "swift_bank_name": "Banco Regional SA",
                    "swift_bank_address_line_1": (
                        "123 Main Street, Suite 100, Downtown District, City Center CP 12345"
                    ),
                    "swift_bank_address_line_2": (
                        "456 Oak Avenue, Building 7, Financial District, Business Center CP 54321"
                    ),
                    "swift_bank_country": "MX",
                    "swift_bank_city": "City",
                    "swift_bank_state_province_region": "District",
                    "swift_bank_postal_code": "11530",
                    "swift_intermediary_bank_swift_code_bic": "AEIBARB1",
                    "swift_intermediary_bank_account_number_iban": "123456789",
                    "swift_intermediary_bank_name": "Banco Regional SA",
                    "swift_intermediary_bank_country": "US",
                    "tron_wallet_hash": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
                    "offramp_wallets": [
                        {
                            "address": "TALJN9zTTEL9TVBb4WuTt6wLvPqJZr3hvb",
                            "id": "ow_000000000000",
                            "network": "tron",
                            "external_id": "your_external_id",
                        },
                    ],
                    "created_at": "2021-01-01T00:00:00Z",
                },
            ],
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_bank_accounts, "error": None}

            response = await self.blindpay.receivers.bank_accounts.list("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_bank_accounts

    @pytest.mark.asyncio
    async def test_delete_bank_account(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = await self.blindpay.receivers.bank_accounts.delete("re_000000000000", "ba_000000000000")

            assert response["error"] is None
            assert response["data"] == {"data": None}


class TestBankAccountsSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_create_pix_bank_account(self):
        mocked_pix_account = {
            "id": "ba_000000000000",
            "type": "pix",
            "name": "PIX Account",
            "pix_key": "14947677768",
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_pix_account, "error": None}

            response = self.blindpay.receivers.bank_accounts.create_pix(
                {
                    "receiver_id": "re_000000000000",
                    "name": "PIX Account",
                    "pix_key": "14947677768",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_pix_account

    def test_create_argentina_transfers_bank_account(self):
        mocked_argentina_transfers_account = {
            "id": "ba_000000000000",
            "type": "transfers_bitso",
            "name": "Argentina Transfers Account",
            "beneficiary_name": "Individual full name or business name",
            "transfers_type": "CVU",
            "transfers_account": "BM123123123123",
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_argentina_transfers_account, "error": None}

            response = self.blindpay.receivers.bank_accounts.create_argentina_transfers(
                {
                    "receiver_id": "re_000000000000",
                    "name": "Argentina Transfers Account",
                    "beneficiary_name": "Individual full name or business name",
                    "transfers_type": "CVU",
                    "transfers_account": "BM123123123123",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_argentina_transfers_account

    def test_create_spei_bank_account(self):
        mocked_spei_account = {
            "id": "ba_000000000000",
            "type": "spei_bitso",
            "name": "SPEI Account",
            "beneficiary_name": "Individual full name or business name",
            "spei_protocol": "clabe",
            "spei_institution_code": "40002",
            "spei_clabe": "5482347403740546",
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_spei_account, "error": None}

            response = self.blindpay.receivers.bank_accounts.create_spei(
                {
                    "receiver_id": "re_000000000000",
                    "name": "SPEI Account",
                    "beneficiary_name": "Individual full name or business name",
                    "spei_protocol": "clabe",
                    "spei_institution_code": "40002",
                    "spei_clabe": "5482347403740546",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_spei_account

    def test_create_colombia_ach_bank_account(self):
        mocked_colombia_ach_account = {
            "id": "ba_000000000000",
            "type": "ach_cop_bitso",
            "name": "Colombia ACH Account",
            "account_type": "checking",
            "ach_cop_beneficiary_first_name": "Fernando",
            "ach_cop_beneficiary_last_name": "Guzman Alarcón",
            "ach_cop_document_id": "1661105408",
            "ach_cop_document_type": "CC",
            "ach_cop_email": "fernando.guzman@gmail.com",
            "ach_cop_bank_code": "051",
            "ach_cop_bank_account": "12345678",
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_colombia_ach_account, "error": None}

            response = self.blindpay.receivers.bank_accounts.create_colombia_ach(
                {
                    "receiver_id": "re_000000000000",
                    "name": "Colombia ACH Account",
                    "account_type": "checking",
                    "ach_cop_beneficiary_first_name": "Fernando",
                    "ach_cop_beneficiary_last_name": "Guzman Alarcón",
                    "ach_cop_document_id": "1661105408",
                    "ach_cop_document_type": "CC",
                    "ach_cop_email": "fernando.guzman@gmail.com",
                    "ach_cop_bank_code": "051",
                    "ach_cop_bank_account": "12345678",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_colombia_ach_account

    def test_create_ach_bank_account(self):
        mocked_ach_account = {
            "id": "ba_000000000000",
            "type": "ach",
            "name": "ACH Account",
            "beneficiary_name": "Individual full name or business name",
            "routing_number": "012345678",
            "account_number": "1001001234",
            "account_type": "checking",
            "account_class": "individual",
            "address_line_1": None,
            "address_line_2": None,
            "city": None,
            "state_province_region": None,
            "country": None,
            "postal_code": None,
            "ach_cop_beneficiary_first_name": None,
            "ach_cop_beneficiary_last_name": None,
            "ach_cop_document_id": None,
            "ach_cop_document_type": None,
            "ach_cop_email": None,
            "ach_cop_bank_code": None,
            "ach_cop_bank_account": None,
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_ach_account, "error": None}

            response = self.blindpay.receivers.bank_accounts.create_ach(
                {
                    "receiver_id": "re_000000000000",
                    "name": "ACH Account",
                    "account_class": "individual",
                    "account_number": "1001001234",
                    "account_type": "checking",
                    "beneficiary_name": "Individual full name or business name",
                    "routing_number": "012345678",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_ach_account

    def test_create_wire_bank_account(self):
        mocked_wire_account = {
            "id": "ba_000000000000",
            "type": "wire",
            "name": "Wire Account",
            "beneficiary_name": "Individual full name or business name",
            "routing_number": "012345678",
            "account_number": "1001001234",
            "address_line_1": "Address line 1",
            "address_line_2": "Address line 2",
            "city": "City",
            "state_province_region": "State/Province/Region",
            "country": "US",
            "postal_code": "Postal code",
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wire_account, "error": None}

            response = self.blindpay.receivers.bank_accounts.create_wire(
                {
                    "receiver_id": "re_000000000000",
                    "name": "Wire Account",
                    "account_number": "1001001234",
                    "beneficiary_name": "Individual full name or business name",
                    "routing_number": "012345678",
                    "address_line_1": "Address line 1",
                    "address_line_2": "Address line 2",
                    "city": "City",
                    "state_province_region": "State/Province/Region",
                    "country": "US",
                    "postal_code": "Postal code",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_wire_account

    def test_create_international_swift_bank_account(self):
        mocked_international_swift_account = {
            "id": "ba_000000000000",
            "type": "international_swift",
            "name": "International Swift Account",
            "beneficiary_name": None,
            "address_line_1": None,
            "address_line_2": None,
            "city": None,
            "state_province_region": None,
            "country": None,
            "postal_code": None,
            "swift_code_bic": "123456789",
            "swift_account_holder_name": "John Doe",
            "swift_account_number_iban": "123456789",
            "swift_beneficiary_address_line_1": ("123 Main Street, Suite 100, Downtown District, City Center CP 12345"),
            "swift_beneficiary_address_line_2": None,
            "swift_beneficiary_country": "MX",
            "swift_beneficiary_city": "City",
            "swift_beneficiary_state_province_region": "District",
            "swift_beneficiary_postal_code": "11530",
            "swift_bank_name": "Banco Regional SA",
            "swift_bank_address_line_1": "123 Main Street, Suite 100, Downtown District, City Center CP 12345",
            "swift_bank_address_line_2": None,
            "swift_bank_country": "MX",
            "swift_bank_city": "City",
            "swift_bank_state_province_region": "District",
            "swift_bank_postal_code": "11530",
            "swift_intermediary_bank_swift_code_bic": None,
            "swift_intermediary_bank_account_number_iban": None,
            "swift_intermediary_bank_name": None,
            "swift_intermediary_bank_country": None,
            "created_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_international_swift_account, "error": None}

            response = self.blindpay.receivers.bank_accounts.create_international_swift(
                {
                    "receiver_id": "re_000000000000",
                    "name": "International Swift Account",
                    "swift_account_holder_name": "John Doe",
                    "swift_account_number_iban": "123456789",
                    "swift_bank_address_line_1": "123 Main Street, Suite 100, Downtown District, City Center CP 12345",
                    "swift_bank_address_line_2": None,
                    "swift_bank_city": "City",
                    "swift_bank_country": "MX",
                    "swift_bank_name": "Banco Regional SA",
                    "swift_bank_postal_code": "11530",
                    "swift_bank_state_province_region": "District",
                    "swift_beneficiary_address_line_1": (
                        "123 Main Street, Suite 100, Downtown District, City Center CP 12345"
                    ),
                    "swift_beneficiary_address_line_2": None,
                    "swift_beneficiary_city": "City",
                    "swift_beneficiary_country": "MX",
                    "swift_beneficiary_postal_code": "11530",
                    "swift_beneficiary_state_province_region": "District",
                    "swift_code_bic": "123456789",
                    "swift_intermediary_bank_account_number_iban": None,
                    "swift_intermediary_bank_country": None,
                    "swift_intermediary_bank_name": None,
                    "swift_intermediary_bank_swift_code_bic": None,
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_international_swift_account

    def test_create_rtp_bank_account(self):
        mocked_rtp_account = {
            "id": "ba_JW5ZtlKMlgS1",
            "type": "rtp",
            "name": "John Doe RTP",
            "beneficiary_name": "John Doe",
            "routing_number": "121000358",
            "account_number": "325203027578",
            "address_line_1": "Street of the fools",
            "address_line_2": None,
            "city": "Fools City",
            "state_province_region": "FL",
            "country": "US",
            "postal_code": "22599",
            "created_at": "2025-09-30T04:23:30.823Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_rtp_account, "error": None}

            response = self.blindpay.receivers.bank_accounts.create_rtp(
                {
                    "receiver_id": "re_000000000000",
                    "name": "John Doe RTP",
                    "beneficiary_name": "John Doe",
                    "routing_number": "121000358",
                    "account_number": "325203027578",
                    "address_line_1": "Street of the fools",
                    "address_line_2": None,
                    "city": "Fools City",
                    "state_province_region": "FL",
                    "country": "US",
                    "postal_code": "22599",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_rtp_account

    def test_get_bank_account(self):
        mocked_bank_account = {
            "id": "ba_000000000000",
            "receiver_id": "rcv_123",
            "account_holder_name": "Individual full name or business name",
            "account_number": "1001001234",
            "routing_number": "012345678",
            "account_type": "checking",
            "bank_name": "Bank Name",
            "swift_code": "123456789",
            "iban": None,
            "is_primary": False,
            "created_at": "2021-01-01T00:00:00Z",
            "updated_at": "2021-01-01T00:00:00Z",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_bank_account, "error": None}

            response = self.blindpay.receivers.bank_accounts.get("re_000000000000", "ba_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_bank_account

    def test_list_bank_accounts(self):
        mocked_bank_accounts = {
            "data": [
                {
                    "id": "ba_000000000000",
                    "type": "wire",
                    "name": "Bank Account Name",
                    "pix_key": "14947677768",
                    "beneficiary_name": "Individual full name or business name",
                    "routing_number": "012345678",
                    "account_number": "1001001234",
                    "account_type": "checking",
                    "account_class": "individual",
                    "address_line_1": "Address line 1",
                    "address_line_2": "Address line 2",
                    "city": "City",
                    "state_province_region": "State/Province/Region",
                    "country": "US",
                    "postal_code": "Postal code",
                    "spei_protocol": "clabe",
                    "spei_institution_code": "40002",
                    "spei_clabe": "5482347403740546",
                    "transfers_type": "CVU",
                    "transfers_account": "BM123123123123",
                    "ach_cop_beneficiary_first_name": "Fernando",
                    "ach_cop_beneficiary_last_name": "Guzman Alarcón",
                    "ach_cop_document_id": "1661105408",
                    "ach_cop_document_type": "CC",
                    "ach_cop_email": "fernando.guzman@gmail.com",
                    "ach_cop_bank_code": "051",
                    "ach_cop_bank_account": "12345678",
                    "swift_code_bic": "123456789",
                    "swift_account_holder_name": "John Doe",
                    "swift_account_number_iban": "123456789",
                    "swift_beneficiary_address_line_1": (
                        "123 Main Street, Suite 100, Downtown District, City Center CP 12345"
                    ),
                    "swift_beneficiary_address_line_2": (
                        "456 Oak Avenue, Building 7, Financial District, Business Center CP 54321"
                    ),
                    "swift_beneficiary_country": "MX",
                    "swift_beneficiary_city": "City",
                    "swift_beneficiary_state_province_region": "District",
                    "swift_beneficiary_postal_code": "11530",
                    "swift_bank_name": "Banco Regional SA",
                    "swift_bank_address_line_1": (
                        "123 Main Street, Suite 100, Downtown District, City Center CP 12345"
                    ),
                    "swift_bank_address_line_2": (
                        "456 Oak Avenue, Building 7, Financial District, Business Center CP 54321"
                    ),
                    "swift_bank_country": "MX",
                    "swift_bank_city": "City",
                    "swift_bank_state_province_region": "District",
                    "swift_bank_postal_code": "11530",
                    "swift_intermediary_bank_swift_code_bic": "AEIBARB1",
                    "swift_intermediary_bank_account_number_iban": "123456789",
                    "swift_intermediary_bank_name": "Banco Regional SA",
                    "swift_intermediary_bank_country": "US",
                    "tron_wallet_hash": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t",
                    "offramp_wallets": [
                        {
                            "address": "TALJN9zTTEL9TVBb4WuTt6wLvPqJZr3hvb",
                            "id": "ow_000000000000",
                            "network": "tron",
                            "external_id": "your_external_id",
                        },
                    ],
                    "created_at": "2021-01-01T00:00:00Z",
                },
            ],
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_bank_accounts, "error": None}

            response = self.blindpay.receivers.bank_accounts.list("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_bank_accounts

    def test_delete_bank_account(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = self.blindpay.receivers.bank_accounts.delete("re_000000000000", "ba_000000000000")

            assert response["error"] is None
            assert response["data"] == {"data": None}
