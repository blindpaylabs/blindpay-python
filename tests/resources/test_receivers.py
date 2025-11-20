from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestReceivers:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_list_receivers(self):
        mocked_receivers = [
            {
                "id": "re_Euw7HN4OdxPn",
                "type": "individual",
                "kyc_type": "standard",
                "kyc_status": "verifying",
                "kyc_warnings": [
                    {
                        "code": None,
                        "message": None,
                        "resolution_status": None,
                        "warning_id": None,
                    },
                ],
                "email": "bernardo@gmail.com",
                "tax_id": "12345678900",
                "address_line_1": "Av. Paulista, 1000",
                "address_line_2": "Apto 101",
                "city": "São Paulo",
                "state_province_region": "SP",
                "country": "BR",
                "postal_code": "01310-100",
                "ip_address": "127.0.0.1",
                "image_url": "https://example.com/image.png",
                "phone_number": "+5511987654321",
                "proof_of_address_doc_type": "UTILITY_BILL",
                "proof_of_address_doc_file": "https://example.com/image.png",
                "first_name": "Bernardo",
                "last_name": "Simonassi",
                "date_of_birth": "1998-02-02T00:00:00.000Z",
                "id_doc_country": "BR",
                "id_doc_type": "PASSPORT",
                "id_doc_front_file": "https://example.com/image.png",
                "id_doc_back_file": "https://example.com/image.png",
                "aiprise_validation_key": "",
                "instance_id": "in_000000000000",
                "tos_id": "to_3ZZhllJkvo5Z",
                "created_at": "2021-01-01T00:00:00.000Z",
                "updated_at": "2021-01-01T00:00:00.000Z",
                "limit": {
                    "per_transaction": 100000,
                    "daily": 200000,
                    "monthly": 1000000,
                },
            },
            {
                "id": "re_YuaMcI2B8zbQ",
                "type": "individual",
                "kyc_type": "enhanced",
                "kyc_status": "approved",
                "kyc_warnings": None,
                "email": "alice.johnson@example.com",
                "tax_id": "98765432100",
                "address_line_1": "123 Main St",
                "address_line_2": None,
                "city": "New York",
                "state_province_region": "NY",
                "country": "US",
                "postal_code": "10001",
                "ip_address": "192.168.1.1",
                "image_url": None,
                "phone_number": "+15555555555",
                "proof_of_address_doc_type": "BANK_STATEMENT",
                "proof_of_address_doc_file": "https://example.com/image.png",
                "first_name": "Alice",
                "last_name": "Johnson",
                "date_of_birth": "1990-05-10T00:00:00.000Z",
                "id_doc_country": "US",
                "id_doc_type": "PASSPORT",
                "id_doc_front_file": "https://example.com/image.png",
                "id_doc_back_file": None,
                "aiprise_validation_key": "enhanced-key",
                "instance_id": "in_000000000001",
                "source_of_funds_doc_type": "salary",
                "source_of_funds_doc_file": "https://example.com/image.png",
                "individual_holding_doc_front_file": "https://example.com/image.png",
                "purpose_of_transactions": "investment_purposes",
                "purpose_of_transactions_explanation": "Investing in stocks",
                "tos_id": "to_nppX66ntvtHs",
                "created_at": "2022-02-02T00:00:00.000Z",
                "updated_at": "2022-02-02T00:00:00.000Z",
                "limit": {
                    "per_transaction": 50000,
                    "daily": 100000,
                    "monthly": 500000,
                },
            },
            {
                "id": "re_IOxAUL24LG7P",
                "type": "business",
                "kyc_type": "standard",
                "kyc_status": "pending",
                "kyc_warnings": None,
                "email": "business@example.com",
                "tax_id": "20096178000195",
                "address_line_1": "1 King St W",
                "address_line_2": "Suite 100",
                "city": "Toronto",
                "state_province_region": "ON",
                "country": "CA",
                "postal_code": "M5H 1A1",
                "ip_address": None,
                "image_url": None,
                "phone_number": "+14165555555",
                "proof_of_address_doc_type": "UTILITY_BILL",
                "proof_of_address_doc_file": "https://example.com/image.png",
                "legal_name": "Business Corp",
                "alternate_name": "BizCo",
                "formation_date": "2010-01-01T00:00:00.000Z",
                "website": "https://businesscorp.com",
                "owners": [
                    {
                        "role": "beneficial_owner",
                        "first_name": "Carlos",
                        "last_name": "Silva",
                        "date_of_birth": "1995-05-15T00:00:00.000Z",
                        "tax_id": "12345678901",
                        "address_line_1": "Rua Augusta, 1500",
                        "address_line_2": None,
                        "city": "São Paulo",
                        "state_province_region": "SP",
                        "country": "BR",
                        "postal_code": "01304-001",
                        "id_doc_country": "BR",
                        "id_doc_type": "PASSPORT",
                        "id_doc_front_file": "https://example.com/image.png",
                        "id_doc_back_file": "https://example.com/image.png",
                        "proof_of_address_doc_type": "UTILITY_BILL",
                        "proof_of_address_doc_file": "https://example.com/image.png",
                        "id": "ub_000000000000",
                        "instance_id": "in_000000000000",
                        "receiver_id": "re_IOxAUL24LG7P",
                    },
                ],
                "incorporation_doc_file": "https://example.com/image.png",
                "proof_of_ownership_doc_file": "https://example.com/image.png",
                "external_id": None,
                "instance_id": "in_000000000002",
                "tos_id": "to_nppX66ntvtHs",
                "aiprise_validation_key": "",
                "created_at": "2015-03-15T00:00:00.000Z",
                "updated_at": "2015-03-15T00:00:00.000Z",
                "limit": {
                    "per_transaction": 200000,
                    "daily": 400000,
                    "monthly": 2000000,
                },
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receivers, "error": None}

            response = await self.blindpay.receivers.list()

            assert response["error"] is None
            assert response["data"] == mocked_receivers
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/receivers")

    @pytest.mark.asyncio
    async def test_create_individual_with_standard_kyc(self):
        mocked_receiver = {
            "id": "re_Euw7HN4OdxPn",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receiver, "error": None}

            response = await self.blindpay.receivers.create_individual_with_standard_kyc(
                {
                    "email": "bernardo.simonassi@gmail.com",
                    "tax_id": "12345678900",
                    "address_line_1": "Av. Paulista, 1000",
                    "address_line_2": "Apto 101",
                    "city": "São Paulo",
                    "state_province_region": "SP",
                    "country": "BR",
                    "postal_code": "01310-100",
                    "phone_number": "+5511987654321",
                    "first_name": "Bernardo",
                    "last_name": "Simonassi",
                    "date_of_birth": "1998-02-02T00:00:00.000Z",
                    "id_doc_country": "BR",
                    "id_doc_type": "PASSPORT",
                    "id_doc_front_file": "https://example.com/image.png",
                    "id_doc_back_file": "https://example.com/image.png",
                    "proof_of_address_doc_type": "UTILITY_BILL",
                    "proof_of_address_doc_file": "https://example.com/image.png",
                    "tos_id": "to_tPiz4bM2nh5K",
                }
            )

            assert response["error"] is None
            assert response["data"] == {"id": "re_Euw7HN4OdxPn"}

    @pytest.mark.asyncio
    async def test_create_individual_with_enhanced_kyc(self):
        mocked_receiver = {
            "id": "re_YuaMcI2B8zbQ",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receiver, "error": None}

            response = await self.blindpay.receivers.create_individual_with_enhanced_kyc(
                {
                    "email": "bernardo.simonassi@gmail.com",
                    "tax_id": "12345678900",
                    "address_line_1": "Av. Paulista, 1000",
                    "address_line_2": "Apto 101",
                    "city": "São Paulo",
                    "state_province_region": "SP",
                    "country": "BR",
                    "postal_code": "01310-100",
                    "first_name": "Bernardo",
                    "last_name": "Simonassi",
                    "phone_number": "+5511987654321",
                    "date_of_birth": "1998-02-02T00:00:00.000Z",
                    "id_doc_country": "BR",
                    "id_doc_type": "PASSPORT",
                    "id_doc_front_file": "https://example.com/image.png",
                    "id_doc_back_file": "https://example.com/image.png",
                    "proof_of_address_doc_type": "UTILITY_BILL",
                    "proof_of_address_doc_file": "https://example.com/image.png",
                    "individual_holding_doc_front_file": "https://example.com/image.png",
                    "purpose_of_transactions": "personal_or_living_expenses",
                    "source_of_funds_doc_type": "savings",
                    "purpose_of_transactions_explanation": "I am receiving salary payments from my employer",
                    "source_of_funds_doc_file": "https://example.com/image.png",
                    "tos_id": "to_3ZZhllJkvo5Z",
                }
            )

            assert response["error"] is None
            assert response["data"] == {"id": "re_YuaMcI2B8zbQ"}

    @pytest.mark.asyncio
    async def test_create_business_with_standard_kyb(self):
        mocked_receiver = {
            "id": "re_IOxAUL24LG7P",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receiver, "error": None}

            response = await self.blindpay.receivers.create_business_with_standard_kyb(
                {
                    "email": "contato@empresa.com.br",
                    "tax_id": "20096178000195",
                    "address_line_1": "Av. Brigadeiro Faria Lima, 400",
                    "address_line_2": "Sala 1201",
                    "city": "São Paulo",
                    "state_province_region": "SP",
                    "country": "BR",
                    "postal_code": "04538-132",
                    "legal_name": "Empresa Exemplo Ltda",
                    "alternate_name": "Exemplo",
                    "formation_date": "2010-05-20T00:00:00.000Z",
                    "incorporation_doc_file": "https://example.com/image.png",
                    "proof_of_address_doc_type": "UTILITY_BILL",
                    "proof_of_address_doc_file": "https://example.com/image.png",
                    "proof_of_ownership_doc_file": "https://example.com/image.png",
                    "tos_id": "to_nppX66ntvtHs",
                    "website": "https://site.com/",
                    "owners": [
                        {
                            "role": "beneficial_owner",
                            "first_name": "Carlos",
                            "last_name": "Silva",
                            "date_of_birth": "1995-05-15T00:00:00.000Z",
                            "tax_id": "12345678901",
                            "address_line_1": "Rua Augusta, 1500",
                            "address_line_2": None,
                            "city": "São Paulo",
                            "state_province_region": "SP",
                            "country": "BR",
                            "postal_code": "01304-001",
                            "id_doc_country": "BR",
                            "id_doc_type": "PASSPORT",
                            "id_doc_front_file": "https://example.com/image.png",
                            "id_doc_back_file": "https://example.com/image.png",
                            "proof_of_address_doc_type": "UTILITY_BILL",
                            "proof_of_address_doc_file": "https://example.com/image.png",
                            "id": "ub_000000000000",
                            "instance_id": "in_000000000000",
                            "receiver_id": "re_IOxAUL24LG7P",
                        },
                    ],
                }
            )

            assert response["error"] is None
            assert response["data"] == {"id": "re_IOxAUL24LG7P"}

    @pytest.mark.asyncio
    async def test_get_receiver(self):
        mocked_receiver = {
            "id": "re_YuaMcI2B8zbQ",
            "type": "individual",
            "kyc_type": "enhanced",
            "kyc_status": "verifying",
            "kyc_warnings": [
                {
                    "code": None,
                    "message": None,
                    "resolution_status": None,
                    "warning_id": None,
                },
            ],
            "email": "bernardo.simonassi@gmail.com",
            "tax_id": "12345678900",
            "address_line_1": "Av. Paulista, 1000",
            "address_line_2": "Apto 101",
            "city": "São Paulo",
            "state_province_region": "SP",
            "country": "BR",
            "postal_code": "01310-100",
            "ip_address": "127.0.0.1",
            "image_url": "https://example.com/image.png",
            "phone_number": "+5511987654321",
            "proof_of_address_doc_type": "UTILITY_BILL",
            "proof_of_address_doc_file": "https://example.com/image.png",
            "first_name": "Bernardo",
            "last_name": "Simonassi",
            "date_of_birth": "1998-02-02T00:00:00.000Z",
            "id_doc_country": "BR",
            "id_doc_type": "PASSPORT",
            "id_doc_front_file": "https://example.com/image.png",
            "id_doc_back_file": "https://example.com/image.png",
            "aiprise_validation_key": "",
            "source_of_funds_doc_type": "savings",
            "source_of_funds_doc_file": "https://example.com/image.png",
            "individual_holding_doc_front_file": "https://example.com/image.png",
            "purpose_of_transactions": "personal_or_living_expenses",
            "purpose_of_transactions_explanation": "I am receiving salary payments from my employer",
            "instance_id": "in_000000000000",
            "tos_id": "to_3ZZhllJkvo5Z",
            "created_at": "2021-01-01T00:00:00.000Z",
            "updated_at": "2021-01-01T00:00:00.000Z",
            "limit": {
                "per_transaction": 100000,
                "daily": 200000,
                "monthly": 1000000,
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receiver, "error": None}

            response = await self.blindpay.receivers.get("re_YuaMcI2B8zbQ")

            assert response["error"] is None
            assert response["data"] == mocked_receiver
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/receivers/re_YuaMcI2B8zbQ")

    @pytest.mark.asyncio
    async def test_update_receiver(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = await self.blindpay.receivers.update(
                {
                    "receiver_id": "re_YuaMcI2B8zbQ",
                    "email": "bernardo.simonassi@gmail.com",
                    "tax_id": "12345678900",
                    "address_line_1": "Av. Paulista, 1000",
                    "address_line_2": "Apto 101",
                    "city": "São Paulo",
                    "state_province_region": "SP",
                    "country": "BR",
                    "postal_code": "01310-100",
                    "ip_address": "127.0.0.1",
                    "image_url": "https://example.com/image.png",
                    "phone_number": "+5511987654321",
                    "proof_of_address_doc_type": "UTILITY_BILL",
                    "proof_of_address_doc_file": "https://example.com/image.png",
                    "first_name": "Bernardo",
                    "last_name": "Simonassi",
                    "date_of_birth": "1998-02-02T00:00:00.000Z",
                    "id_doc_country": "BR",
                    "id_doc_type": "PASSPORT",
                    "id_doc_front_file": "https://example.com/image.png",
                    "id_doc_back_file": "https://example.com/image.png",
                    "alternate_name": "Exemplo",
                    "formation_date": "2010-05-20T00:00:00.000Z",
                    "website": "https://site.com",
                    "owners": [
                        {
                            "id": "ub_000000000000",
                            "first_name": "Carlos",
                            "last_name": "Silva",
                            "role": "beneficial_owner",
                            "date_of_birth": "1995-05-15T00:00:00.000Z",
                            "tax_id": "12345678901",
                            "address_line_1": "Rua Augusta, 1500",
                            "address_line_2": None,
                            "city": "São Paulo",
                            "state_province_region": "SP",
                            "country": "BR",
                            "postal_code": "01304-001",
                            "id_doc_country": "BR",
                            "id_doc_type": "PASSPORT",
                            "id_doc_front_file": "https://example.com/image.png",
                            "id_doc_back_file": "https://example.com/image.png",
                        },
                    ],
                    "incorporation_doc_file": "https://example.com/image.png",
                    "proof_of_ownership_doc_file": "https://example.com/image.png",
                    "source_of_funds_doc_type": "savings",
                    "source_of_funds_doc_file": "https://example.com/image.png",
                    "individual_holding_doc_front_file": "https://example.com/image.png",
                    "purpose_of_transactions": "personal_or_living_expenses",
                    "purpose_of_transactions_explanation": "I am receiving salary payments from my employer",
                    "external_id": "some-external-id",
                    "tos_id": "to_3ZZhllJkvo5Z",
                }
            )

            assert response["error"] is None
            assert response["data"] == {"data": None}

    @pytest.mark.asyncio
    async def test_delete_receiver(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = await self.blindpay.receivers.delete("re_YuaMcI2B8zbQ")

            assert response["error"] is None
            assert response["data"] == {"data": None}
            mock_request.assert_called_once_with("DELETE", "/instances/in_000000000000/receivers/re_YuaMcI2B8zbQ", None)

    @pytest.mark.asyncio
    async def test_get_receiver_limits(self):
        mocked_receiver_limits = {
            "limits": {
                "payin": {
                    "daily": 10000,
                    "monthly": 50000,
                },
                "payout": {
                    "daily": 20000,
                    "monthly": 100000,
                },
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receiver_limits, "error": None}

            response = await self.blindpay.receivers.get_limits("re_YuaMcI2B8zbQ")

            assert response["error"] is None
            assert response["data"] == mocked_receiver_limits
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/limits/receivers/re_YuaMcI2B8zbQ")

    @pytest.mark.asyncio
    async def test_get_limit_increase_requests(self):
        mocked_limit_increase_requests = [
            {
                "id": "rl_000000000000",
                "receiver_id": "re_YuaMcI2B8zbQ",
                "status": "in_review",
                "daily": 50000,
                "monthly": 250000,
                "per_transaction": 25000,
                "supporting_document_file": "https://example.com/bank-statement.pdf",
                "supporting_document_type": "individual_bank_statement",
                "created_at": "2025-01-15T10:30:00.000Z",
                "updated_at": "2025-01-15T10:30:00.000Z",
            },
            {
                "id": "rl_000000000000",
                "receiver_id": "re_YuaMcI2B8zbQ",
                "status": "approved",
                "daily": 30000,
                "monthly": 150000,
                "per_transaction": 15000,
                "supporting_document_file": "https://example.com/proof-of-income.pdf",
                "supporting_document_type": "individual_proof_of_income",
                "created_at": "2024-12-10T14:20:00.000Z",
                "updated_at": "2024-12-12T09:45:00.000Z",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_limit_increase_requests, "error": None}

            response = await self.blindpay.receivers.get_limit_increase_requests("re_YuaMcI2B8zbQ")

            assert response["error"] is None
            assert response["data"] == mocked_limit_increase_requests
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_YuaMcI2B8zbQ/limit-increase"
            )

    @pytest.mark.asyncio
    async def test_request_limit_increase(self):
        mocked_response = {
            "id": "rl_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_response, "error": None}

            response = await self.blindpay.receivers.request_limit_increase(
                {
                    "receiver_id": "re_YuaMcI2B8zbQ",
                    "daily": 100000,
                    "monthly": 500000,
                    "per_transaction": 50000,
                    "supporting_document_file": "https://example.com/tax-return.pdf",
                    "supporting_document_type": "individual_tax_return",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_response
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_YuaMcI2B8zbQ/limit-increase",
                {
                    "daily": 100000,
                    "monthly": 500000,
                    "per_transaction": 50000,
                    "supporting_document_file": "https://example.com/tax-return.pdf",
                    "supporting_document_type": "individual_tax_return",
                },
            )


class TestReceiversSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_list_receivers(self):
        mocked_receivers = [
            {
                "id": "re_Euw7HN4OdxPn",
                "type": "individual",
                "kyc_type": "standard",
                "kyc_status": "verifying",
                "kyc_warnings": [
                    {
                        "code": None,
                        "message": None,
                        "resolution_status": None,
                        "warning_id": None,
                    },
                ],
                "email": "bernardo@gmail.com",
                "tax_id": "12345678900",
                "address_line_1": "Av. Paulista, 1000",
                "address_line_2": "Apto 101",
                "city": "São Paulo",
                "state_province_region": "SP",
                "country": "BR",
                "postal_code": "01310-100",
                "ip_address": "127.0.0.1",
                "image_url": "https://example.com/image.png",
                "phone_number": "+5511987654321",
                "proof_of_address_doc_type": "UTILITY_BILL",
                "proof_of_address_doc_file": "https://example.com/image.png",
                "first_name": "Bernardo",
                "last_name": "Simonassi",
                "date_of_birth": "1998-02-02T00:00:00.000Z",
                "id_doc_country": "BR",
                "id_doc_type": "PASSPORT",
                "id_doc_front_file": "https://example.com/image.png",
                "id_doc_back_file": "https://example.com/image.png",
                "aiprise_validation_key": "",
                "instance_id": "in_000000000000",
                "tos_id": "to_3ZZhllJkvo5Z",
                "created_at": "2021-01-01T00:00:00.000Z",
                "updated_at": "2021-01-01T00:00:00.000Z",
                "limit": {
                    "per_transaction": 100000,
                    "daily": 200000,
                    "monthly": 1000000,
                },
            },
            {
                "id": "re_YuaMcI2B8zbQ",
                "type": "individual",
                "kyc_type": "enhanced",
                "kyc_status": "approved",
                "kyc_warnings": None,
                "email": "alice.johnson@example.com",
                "tax_id": "98765432100",
                "address_line_1": "123 Main St",
                "address_line_2": None,
                "city": "New York",
                "state_province_region": "NY",
                "country": "US",
                "postal_code": "10001",
                "ip_address": "192.168.1.1",
                "image_url": None,
                "phone_number": "+15555555555",
                "proof_of_address_doc_type": "BANK_STATEMENT",
                "proof_of_address_doc_file": "https://example.com/image.png",
                "first_name": "Alice",
                "last_name": "Johnson",
                "date_of_birth": "1990-05-10T00:00:00.000Z",
                "id_doc_country": "US",
                "id_doc_type": "PASSPORT",
                "id_doc_front_file": "https://example.com/image.png",
                "id_doc_back_file": None,
                "aiprise_validation_key": "enhanced-key",
                "instance_id": "in_000000000001",
                "source_of_funds_doc_type": "salary",
                "source_of_funds_doc_file": "https://example.com/image.png",
                "individual_holding_doc_front_file": "https://example.com/image.png",
                "purpose_of_transactions": "investment_purposes",
                "purpose_of_transactions_explanation": "Investing in stocks",
                "tos_id": "to_nppX66ntvtHs",
                "created_at": "2022-02-02T00:00:00.000Z",
                "updated_at": "2022-02-02T00:00:00.000Z",
                "limit": {
                    "per_transaction": 50000,
                    "daily": 100000,
                    "monthly": 500000,
                },
            },
            {
                "id": "re_IOxAUL24LG7P",
                "type": "business",
                "kyc_type": "standard",
                "kyc_status": "pending",
                "kyc_warnings": None,
                "email": "business@example.com",
                "tax_id": "20096178000195",
                "address_line_1": "1 King St W",
                "address_line_2": "Suite 100",
                "city": "Toronto",
                "state_province_region": "ON",
                "country": "CA",
                "postal_code": "M5H 1A1",
                "ip_address": None,
                "image_url": None,
                "phone_number": "+14165555555",
                "proof_of_address_doc_type": "UTILITY_BILL",
                "proof_of_address_doc_file": "https://example.com/image.png",
                "legal_name": "Business Corp",
                "alternate_name": "BizCo",
                "formation_date": "2010-01-01T00:00:00.000Z",
                "website": "https://businesscorp.com",
                "owners": [
                    {
                        "role": "beneficial_owner",
                        "first_name": "Carlos",
                        "last_name": "Silva",
                        "date_of_birth": "1995-05-15T00:00:00.000Z",
                        "tax_id": "12345678901",
                        "address_line_1": "Rua Augusta, 1500",
                        "address_line_2": None,
                        "city": "São Paulo",
                        "state_province_region": "SP",
                        "country": "BR",
                        "postal_code": "01304-001",
                        "id_doc_country": "BR",
                        "id_doc_type": "PASSPORT",
                        "id_doc_front_file": "https://example.com/image.png",
                        "id_doc_back_file": "https://example.com/image.png",
                        "proof_of_address_doc_type": "UTILITY_BILL",
                        "proof_of_address_doc_file": "https://example.com/image.png",
                        "id": "ub_000000000000",
                        "instance_id": "in_000000000000",
                        "receiver_id": "re_IOxAUL24LG7P",
                    },
                ],
                "incorporation_doc_file": "https://example.com/image.png",
                "proof_of_ownership_doc_file": "https://example.com/image.png",
                "external_id": None,
                "instance_id": "in_000000000002",
                "tos_id": "to_nppX66ntvtHs",
                "aiprise_validation_key": "",
                "created_at": "2015-03-15T00:00:00.000Z",
                "updated_at": "2015-03-15T00:00:00.000Z",
                "limit": {
                    "per_transaction": 200000,
                    "daily": 400000,
                    "monthly": 2000000,
                },
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receivers, "error": None}

            response = self.blindpay.receivers.list()

            assert response["error"] is None
            assert response["data"] == mocked_receivers
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/receivers")

    def test_create_individual_with_standard_kyc(self):
        mocked_receiver = {
            "id": "re_Euw7HN4OdxPn",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receiver, "error": None}

            response = self.blindpay.receivers.create_individual_with_standard_kyc(
                {
                    "email": "bernardo.simonassi@gmail.com",
                    "tax_id": "12345678900",
                    "address_line_1": "Av. Paulista, 1000",
                    "address_line_2": "Apto 101",
                    "city": "São Paulo",
                    "state_province_region": "SP",
                    "country": "BR",
                    "postal_code": "01310-100",
                    "phone_number": "+5511987654321",
                    "first_name": "Bernardo",
                    "last_name": "Simonassi",
                    "date_of_birth": "1998-02-02T00:00:00.000Z",
                    "id_doc_country": "BR",
                    "id_doc_type": "PASSPORT",
                    "id_doc_front_file": "https://example.com/image.png",
                    "id_doc_back_file": "https://example.com/image.png",
                    "proof_of_address_doc_type": "UTILITY_BILL",
                    "proof_of_address_doc_file": "https://example.com/image.png",
                    "tos_id": "to_tPiz4bM2nh5K",
                }
            )

            assert response["error"] is None
            assert response["data"] == {"id": "re_Euw7HN4OdxPn"}

    def test_create_individual_with_enhanced_kyc(self):
        mocked_receiver = {
            "id": "re_YuaMcI2B8zbQ",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receiver, "error": None}

            response = self.blindpay.receivers.create_individual_with_enhanced_kyc(
                {
                    "email": "bernardo.simonassi@gmail.com",
                    "tax_id": "12345678900",
                    "address_line_1": "Av. Paulista, 1000",
                    "address_line_2": "Apto 101",
                    "city": "São Paulo",
                    "state_province_region": "SP",
                    "country": "BR",
                    "postal_code": "01310-100",
                    "first_name": "Bernardo",
                    "last_name": "Simonassi",
                    "phone_number": "+5511987654321",
                    "date_of_birth": "1998-02-02T00:00:00.000Z",
                    "id_doc_country": "BR",
                    "id_doc_type": "PASSPORT",
                    "id_doc_front_file": "https://example.com/image.png",
                    "id_doc_back_file": "https://example.com/image.png",
                    "proof_of_address_doc_type": "UTILITY_BILL",
                    "proof_of_address_doc_file": "https://example.com/image.png",
                    "individual_holding_doc_front_file": "https://example.com/image.png",
                    "purpose_of_transactions": "personal_or_living_expenses",
                    "source_of_funds_doc_type": "savings",
                    "purpose_of_transactions_explanation": "I am receiving salary payments from my employer",
                    "source_of_funds_doc_file": "https://example.com/image.png",
                    "tos_id": "to_3ZZhllJkvo5Z",
                }
            )

            assert response["error"] is None
            assert response["data"] == {"id": "re_YuaMcI2B8zbQ"}

    def test_create_business_with_standard_kyb(self):
        mocked_receiver = {
            "id": "re_IOxAUL24LG7P",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receiver, "error": None}

            response = self.blindpay.receivers.create_business_with_standard_kyb(
                {
                    "email": "contato@empresa.com.br",
                    "tax_id": "20096178000195",
                    "address_line_1": "Av. Brigadeiro Faria Lima, 400",
                    "address_line_2": "Sala 1201",
                    "city": "São Paulo",
                    "state_province_region": "SP",
                    "country": "BR",
                    "postal_code": "04538-132",
                    "legal_name": "Empresa Exemplo Ltda",
                    "alternate_name": "Exemplo",
                    "formation_date": "2010-05-20T00:00:00.000Z",
                    "incorporation_doc_file": "https://example.com/image.png",
                    "proof_of_address_doc_type": "UTILITY_BILL",
                    "proof_of_address_doc_file": "https://example.com/image.png",
                    "proof_of_ownership_doc_file": "https://example.com/image.png",
                    "tos_id": "to_nppX66ntvtHs",
                    "website": "https://site.com/",
                    "owners": [
                        {
                            "role": "beneficial_owner",
                            "first_name": "Carlos",
                            "last_name": "Silva",
                            "date_of_birth": "1995-05-15T00:00:00.000Z",
                            "tax_id": "12345678901",
                            "address_line_1": "Rua Augusta, 1500",
                            "address_line_2": None,
                            "city": "São Paulo",
                            "state_province_region": "SP",
                            "country": "BR",
                            "postal_code": "01304-001",
                            "id_doc_country": "BR",
                            "id_doc_type": "PASSPORT",
                            "id_doc_front_file": "https://example.com/image.png",
                            "id_doc_back_file": "https://example.com/image.png",
                            "proof_of_address_doc_type": "UTILITY_BILL",
                            "proof_of_address_doc_file": "https://example.com/image.png",
                            "id": "ub_000000000000",
                            "instance_id": "in_000000000000",
                            "receiver_id": "re_IOxAUL24LG7P",
                        },
                    ],
                }
            )

            assert response["error"] is None
            assert response["data"] == {"id": "re_IOxAUL24LG7P"}

    def test_get_receiver(self):
        mocked_receiver = {
            "id": "re_YuaMcI2B8zbQ",
            "type": "individual",
            "kyc_type": "enhanced",
            "kyc_status": "verifying",
            "kyc_warnings": [
                {
                    "code": None,
                    "message": None,
                    "resolution_status": None,
                    "warning_id": None,
                },
            ],
            "email": "bernardo.simonassi@gmail.com",
            "tax_id": "12345678900",
            "address_line_1": "Av. Paulista, 1000",
            "address_line_2": "Apto 101",
            "city": "São Paulo",
            "state_province_region": "SP",
            "country": "BR",
            "postal_code": "01310-100",
            "ip_address": "127.0.0.1",
            "image_url": "https://example.com/image.png",
            "phone_number": "+5511987654321",
            "proof_of_address_doc_type": "UTILITY_BILL",
            "proof_of_address_doc_file": "https://example.com/image.png",
            "first_name": "Bernardo",
            "last_name": "Simonassi",
            "date_of_birth": "1998-02-02T00:00:00.000Z",
            "id_doc_country": "BR",
            "id_doc_type": "PASSPORT",
            "id_doc_front_file": "https://example.com/image.png",
            "id_doc_back_file": "https://example.com/image.png",
            "aiprise_validation_key": "",
            "source_of_funds_doc_type": "savings",
            "source_of_funds_doc_file": "https://example.com/image.png",
            "individual_holding_doc_front_file": "https://example.com/image.png",
            "purpose_of_transactions": "personal_or_living_expenses",
            "purpose_of_transactions_explanation": "I am receiving salary payments from my employer",
            "instance_id": "in_000000000000",
            "tos_id": "to_3ZZhllJkvo5Z",
            "created_at": "2021-01-01T00:00:00.000Z",
            "updated_at": "2021-01-01T00:00:00.000Z",
            "limit": {
                "per_transaction": 100000,
                "daily": 200000,
                "monthly": 1000000,
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receiver, "error": None}

            response = self.blindpay.receivers.get("re_YuaMcI2B8zbQ")

            assert response["error"] is None
            assert response["data"] == mocked_receiver
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/receivers/re_YuaMcI2B8zbQ")

    def test_update_receiver(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = self.blindpay.receivers.update(
                {
                    "receiver_id": "re_YuaMcI2B8zbQ",
                    "email": "bernardo.simonassi@gmail.com",
                    "tax_id": "12345678900",
                    "address_line_1": "Av. Paulista, 1000",
                    "address_line_2": "Apto 101",
                    "city": "São Paulo",
                    "state_province_region": "SP",
                    "country": "BR",
                    "postal_code": "01310-100",
                    "ip_address": "127.0.0.1",
                    "image_url": "https://example.com/image.png",
                    "phone_number": "+5511987654321",
                    "proof_of_address_doc_type": "UTILITY_BILL",
                    "proof_of_address_doc_file": "https://example.com/image.png",
                    "first_name": "Bernardo",
                    "last_name": "Simonassi",
                    "date_of_birth": "1998-02-02T00:00:00.000Z",
                    "id_doc_country": "BR",
                    "id_doc_type": "PASSPORT",
                    "id_doc_front_file": "https://example.com/image.png",
                    "id_doc_back_file": "https://example.com/image.png",
                    "alternate_name": "Exemplo",
                    "formation_date": "2010-05-20T00:00:00.000Z",
                    "website": "https://site.com",
                    "owners": [
                        {
                            "id": "ub_000000000000",
                            "first_name": "Carlos",
                            "last_name": "Silva",
                            "role": "beneficial_owner",
                            "date_of_birth": "1995-05-15T00:00:00.000Z",
                            "tax_id": "12345678901",
                            "address_line_1": "Rua Augusta, 1500",
                            "address_line_2": None,
                            "city": "São Paulo",
                            "state_province_region": "SP",
                            "country": "BR",
                            "postal_code": "01304-001",
                            "id_doc_country": "BR",
                            "id_doc_type": "PASSPORT",
                            "id_doc_front_file": "https://example.com/image.png",
                            "id_doc_back_file": "https://example.com/image.png",
                        },
                    ],
                    "incorporation_doc_file": "https://example.com/image.png",
                    "proof_of_ownership_doc_file": "https://example.com/image.png",
                    "source_of_funds_doc_type": "savings",
                    "source_of_funds_doc_file": "https://example.com/image.png",
                    "individual_holding_doc_front_file": "https://example.com/image.png",
                    "purpose_of_transactions": "personal_or_living_expenses",
                    "purpose_of_transactions_explanation": "I am receiving salary payments from my employer",
                    "external_id": "some-external-id",
                    "tos_id": "to_3ZZhllJkvo5Z",
                }
            )

            assert response["error"] is None
            assert response["data"] == {"data": None}

    def test_delete_receiver(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = self.blindpay.receivers.delete("re_YuaMcI2B8zbQ")

            assert response["error"] is None
            assert response["data"] == {"data": None}
            mock_request.assert_called_once_with("DELETE", "/instances/in_000000000000/receivers/re_YuaMcI2B8zbQ", None)

    def test_get_receiver_limits(self):
        mocked_receiver_limits = {
            "limits": {
                "payin": {
                    "daily": 10000,
                    "monthly": 50000,
                },
                "payout": {
                    "daily": 20000,
                    "monthly": 100000,
                },
            },
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receiver_limits, "error": None}

            response = self.blindpay.receivers.get_limits("re_YuaMcI2B8zbQ")

            assert response["error"] is None
            assert response["data"] == mocked_receiver_limits
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/limits/receivers/re_YuaMcI2B8zbQ")

    def test_get_limit_increase_requests(self):
        mocked_limit_increase_requests = [
            {
                "id": "rl_000000000000",
                "receiver_id": "re_YuaMcI2B8zbQ",
                "status": "in_review",
                "daily": 50000,
                "monthly": 250000,
                "per_transaction": 25000,
                "supporting_document_file": "https://example.com/bank-statement.pdf",
                "supporting_document_type": "individual_bank_statement",
                "created_at": "2025-01-15T10:30:00.000Z",
                "updated_at": "2025-01-15T10:30:00.000Z",
            },
            {
                "id": "rl_000000000000",
                "receiver_id": "re_YuaMcI2B8zbQ",
                "status": "approved",
                "daily": 30000,
                "monthly": 150000,
                "per_transaction": 15000,
                "supporting_document_file": "https://example.com/proof-of-income.pdf",
                "supporting_document_type": "individual_proof_of_income",
                "created_at": "2024-12-10T14:20:00.000Z",
                "updated_at": "2024-12-12T09:45:00.000Z",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_limit_increase_requests, "error": None}

            response = self.blindpay.receivers.get_limit_increase_requests("re_YuaMcI2B8zbQ")

            assert response["error"] is None
            assert response["data"] == mocked_limit_increase_requests
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_YuaMcI2B8zbQ/limit-increase"
            )

    def test_request_limit_increase(self):
        mocked_response = {
            "id": "rl_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_response, "error": None}

            response = self.blindpay.receivers.request_limit_increase(
                {
                    "receiver_id": "re_YuaMcI2B8zbQ",
                    "daily": 100000,
                    "monthly": 500000,
                    "per_transaction": 50000,
                    "supporting_document_file": "https://example.com/tax-return.pdf",
                    "supporting_document_type": "individual_tax_return",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_response
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_YuaMcI2B8zbQ/limit-increase",
                {
                    "daily": 100000,
                    "monthly": 500000,
                    "per_transaction": 50000,
                    "supporting_document_file": "https://example.com/tax-return.pdf",
                    "supporting_document_type": "individual_tax_return",
                },
            )
