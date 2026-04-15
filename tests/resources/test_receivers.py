from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestReceivers:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_list(self):
        mocked_data = [{"id": "re_000000000000"}]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": mocked_data, "pagination": {"has_more": False}}, "error": None}

            response = await self.blindpay.receivers.list()

            assert response["error"] is None
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/receivers")

    @pytest.mark.asyncio
    async def test_list_with_params(self):
        mocked_data = [{"id": "re_000000000000"}]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": mocked_data, "pagination": {"has_more": False}}, "error": None}

            response = await self.blindpay.receivers.list({"status": "approved", "limit": "10"})

            assert response["error"] is None
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers?status=approved&limit=10"
            )

    @pytest.mark.asyncio
    async def test_create(self):
        mocked_response = {"id": "re_000000000000"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_response, "error": None}

            response = await self.blindpay.receivers.create(
                {
                    "type": "individual",
                    "kyc_type": "standard",
                    "email": "test@example.com",
                    "country": "BR",
                    "first_name": "John",
                    "last_name": "Doe",
                    "date_of_birth": "1990-01-01T00:00:00.000Z",
                    "tax_id": "12345678900",
                    "address_line_1": "Av. Paulista, 1000",
                    "address_line_2": None,
                    "city": "São Paulo",
                    "state_province_region": "SP",
                    "postal_code": "01310-100",
                    "id_doc_country": "BR",
                    "id_doc_type": "PASSPORT",
                    "id_doc_front_file": "https://example.com/front.png",
                    "id_doc_back_file": None,
                    "proof_of_address_doc_type": "UTILITY_BILL",
                    "proof_of_address_doc_file": "https://example.com/proof.png",
                    "tos_id": "to_000000000000",
                    "phone_number": None,
                    "ip_address": None,
                    "image_url": None,
                    "selfie_file": None,
                    "source_of_funds_doc_type": None,
                    "source_of_funds_doc_file": None,
                    "purpose_of_transactions": None,
                    "purpose_of_transactions_explanation": None,
                    "account_purpose": None,
                    "account_purpose_other": None,
                    "business_type": None,
                    "business_description": None,
                    "business_industry": None,
                    "estimated_annual_revenue": None,
                    "source_of_wealth": None,
                    "publicly_traded": None,
                    "occupation": None,
                    "external_id": None,
                    "legal_name": None,
                    "alternate_name": None,
                    "formation_date": None,
                    "website": None,
                    "owners": None,
                    "incorporation_doc_file": None,
                    "proof_of_ownership_doc_file": None,
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_response

    @pytest.mark.asyncio
    async def test_get(self):
        mocked_receiver = {
            "id": "re_000000000000",
            "type": "individual",
            "kyc_type": "standard",
            "kyc_status": "approved",
            "kyc_warnings": None,
            "fraud_warnings": None,
            "email": "test@example.com",
            "tax_id": "12345678900",
            "address_line_1": "Av. Paulista, 1000",
            "address_line_2": None,
            "city": "São Paulo",
            "state_province_region": "SP",
            "country": "BR",
            "postal_code": "01310-100",
            "ip_address": None,
            "image_url": None,
            "phone_number": None,
            "proof_of_address_doc_type": "UTILITY_BILL",
            "proof_of_address_doc_file": "https://example.com/proof.png",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01T00:00:00.000Z",
            "id_doc_country": "BR",
            "id_doc_type": "PASSPORT",
            "id_doc_front_file": "https://example.com/front.png",
            "id_doc_back_file": None,
            "legal_name": None,
            "alternate_name": None,
            "formation_date": None,
            "website": None,
            "owners": None,
            "incorporation_doc_file": None,
            "proof_of_ownership_doc_file": None,
            "source_of_funds_doc_type": None,
            "source_of_funds_doc_file": None,
            "selfie_file": None,
            "purpose_of_transactions": None,
            "purpose_of_transactions_explanation": None,
            "is_fbo": None,
            "account_purpose": None,
            "account_purpose_other": None,
            "business_type": None,
            "business_description": None,
            "business_industry": None,
            "estimated_annual_revenue": None,
            "source_of_wealth": None,
            "publicly_traded": None,
            "occupation": None,
            "external_id": None,
            "instance_id": "in_000000000000",
            "tos_id": "to_000000000000",
            "aml_status": None,
            "aml_hits": None,
            "created_at": "2021-01-01T00:00:00.000Z",
            "updated_at": "2021-01-01T00:00:00.000Z",
            "limit": {"per_transaction": 100000, "daily": 200000, "monthly": 1000000},
            "is_tos_accepted": None,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receiver, "error": None}

            response = await self.blindpay.receivers.get("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_receiver
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/receivers/re_000000000000")

    @pytest.mark.asyncio
    async def test_update(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": None, "error": None}

            response = await self.blindpay.receivers.update(
                {
                    "receiver_id": "re_000000000000",
                    "email": "updated@example.com",
                    "country": "BR",
                    "first_name": "John",
                    "last_name": "Doe",
                    "tax_id": None,
                    "address_line_1": None,
                    "address_line_2": None,
                    "city": None,
                    "state_province_region": None,
                    "postal_code": None,
                    "ip_address": None,
                    "image_url": None,
                    "phone_number": None,
                    "proof_of_address_doc_type": None,
                    "proof_of_address_doc_file": None,
                    "date_of_birth": None,
                    "id_doc_country": None,
                    "id_doc_type": None,
                    "id_doc_front_file": None,
                    "id_doc_back_file": None,
                    "legal_name": None,
                    "alternate_name": None,
                    "formation_date": None,
                    "website": None,
                    "owners": None,
                    "incorporation_doc_file": None,
                    "proof_of_ownership_doc_file": None,
                    "source_of_funds_doc_type": None,
                    "source_of_funds_doc_file": None,
                    "selfie_file": None,
                    "purpose_of_transactions": None,
                    "purpose_of_transactions_explanation": None,
                    "account_purpose": None,
                    "account_purpose_other": None,
                    "business_type": None,
                    "business_description": None,
                    "business_industry": None,
                    "estimated_annual_revenue": None,
                    "source_of_wealth": None,
                    "publicly_traded": None,
                    "occupation": None,
                    "external_id": None,
                    "tos_id": None,
                }
            )

            assert response["error"] is None
            mock_request.assert_called_once_with(
                "PUT",
                "/instances/in_000000000000/receivers/re_000000000000",
                {
                    "email": "updated@example.com",
                    "country": "BR",
                    "first_name": "John",
                    "last_name": "Doe",
                    "tax_id": None,
                    "address_line_1": None,
                    "address_line_2": None,
                    "city": None,
                    "state_province_region": None,
                    "postal_code": None,
                    "ip_address": None,
                    "image_url": None,
                    "phone_number": None,
                    "proof_of_address_doc_type": None,
                    "proof_of_address_doc_file": None,
                    "date_of_birth": None,
                    "id_doc_country": None,
                    "id_doc_type": None,
                    "id_doc_front_file": None,
                    "id_doc_back_file": None,
                    "legal_name": None,
                    "alternate_name": None,
                    "formation_date": None,
                    "website": None,
                    "owners": None,
                    "incorporation_doc_file": None,
                    "proof_of_ownership_doc_file": None,
                    "source_of_funds_doc_type": None,
                    "source_of_funds_doc_file": None,
                    "selfie_file": None,
                    "purpose_of_transactions": None,
                    "purpose_of_transactions_explanation": None,
                    "account_purpose": None,
                    "account_purpose_other": None,
                    "business_type": None,
                    "business_description": None,
                    "business_industry": None,
                    "estimated_annual_revenue": None,
                    "source_of_wealth": None,
                    "publicly_traded": None,
                    "occupation": None,
                    "external_id": None,
                    "tos_id": None,
                },
            )

    @pytest.mark.asyncio
    async def test_delete(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": None, "error": None}

            response = await self.blindpay.receivers.delete("re_000000000000")

            assert response["error"] is None
            mock_request.assert_called_once_with("DELETE", "/instances/in_000000000000/receivers/re_000000000000", None)

    @pytest.mark.asyncio
    async def test_get_limits(self):
        mocked_limits = {
            "limits": {
                "payin": {"daily": 10000, "monthly": 50000},
                "payout": {"daily": 20000, "monthly": 100000},
            }
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_limits, "error": None}

            response = await self.blindpay.receivers.get_limits("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_limits
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/limits/receivers/re_000000000000"
            )

    @pytest.mark.asyncio
    async def test_get_limit_increase_requests(self):
        mocked_requests = [
            {
                "id": "rl_000000000000",
                "receiver_id": "re_000000000000",
                "status": "in_review",
                "daily": 50000,
                "monthly": 250000,
                "per_transaction": 25000,
                "supporting_document_file": "https://example.com/doc.pdf",
                "supporting_document_type": "individual_bank_statement",
                "created_at": "2025-01-01T00:00:00.000Z",
                "updated_at": "2025-01-01T00:00:00.000Z",
            }
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_requests, "error": None}

            response = await self.blindpay.receivers.get_limit_increase_requests("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_requests
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/limit-increase"
            )

    @pytest.mark.asyncio
    async def test_request_limit_increase(self):
        mocked_response = {"id": "rl_000000000000"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_response, "error": None}

            response = await self.blindpay.receivers.request_limit_increase(
                {
                    "receiver_id": "re_000000000000",
                    "daily": 100000,
                    "monthly": 500000,
                    "per_transaction": 50000,
                    "supporting_document_file": "https://example.com/doc.pdf",
                    "supporting_document_type": "individual_bank_statement",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_response
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_000000000000/limit-increase",
                {
                    "daily": 100000,
                    "monthly": 500000,
                    "per_transaction": 50000,
                    "supporting_document_file": "https://example.com/doc.pdf",
                    "supporting_document_type": "individual_bank_statement",
                },
            )


class TestReceiversSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_list(self):
        mocked_data = [{"id": "re_000000000000"}]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": mocked_data, "pagination": {"has_more": False}}, "error": None}

            response = self.blindpay.receivers.list()

            assert response["error"] is None
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/receivers")

    def test_list_with_params(self):
        mocked_data = [{"id": "re_000000000000"}]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": mocked_data, "pagination": {"has_more": False}}, "error": None}

            response = self.blindpay.receivers.list({"status": "approved", "limit": "10"})

            assert response["error"] is None
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers?status=approved&limit=10"
            )

    def test_create(self):
        mocked_response = {"id": "re_000000000000"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_response, "error": None}

            response = self.blindpay.receivers.create(
                {
                    "type": "individual",
                    "kyc_type": "standard",
                    "email": "test@example.com",
                    "country": "BR",
                    "first_name": "John",
                    "last_name": "Doe",
                    "date_of_birth": "1990-01-01T00:00:00.000Z",
                    "tax_id": "12345678900",
                    "address_line_1": "Av. Paulista, 1000",
                    "address_line_2": None,
                    "city": "São Paulo",
                    "state_province_region": "SP",
                    "postal_code": "01310-100",
                    "id_doc_country": "BR",
                    "id_doc_type": "PASSPORT",
                    "id_doc_front_file": "https://example.com/front.png",
                    "id_doc_back_file": None,
                    "proof_of_address_doc_type": "UTILITY_BILL",
                    "proof_of_address_doc_file": "https://example.com/proof.png",
                    "tos_id": "to_000000000000",
                    "phone_number": None,
                    "ip_address": None,
                    "image_url": None,
                    "selfie_file": None,
                    "source_of_funds_doc_type": None,
                    "source_of_funds_doc_file": None,
                    "purpose_of_transactions": None,
                    "purpose_of_transactions_explanation": None,
                    "account_purpose": None,
                    "account_purpose_other": None,
                    "business_type": None,
                    "business_description": None,
                    "business_industry": None,
                    "estimated_annual_revenue": None,
                    "source_of_wealth": None,
                    "publicly_traded": None,
                    "occupation": None,
                    "external_id": None,
                    "legal_name": None,
                    "alternate_name": None,
                    "formation_date": None,
                    "website": None,
                    "owners": None,
                    "incorporation_doc_file": None,
                    "proof_of_ownership_doc_file": None,
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_response

    def test_get(self):
        mocked_receiver = {
            "id": "re_000000000000",
            "type": "individual",
            "kyc_type": "standard",
            "kyc_status": "approved",
            "kyc_warnings": None,
            "fraud_warnings": None,
            "email": "test@example.com",
            "tax_id": "12345678900",
            "address_line_1": "Av. Paulista, 1000",
            "address_line_2": None,
            "city": "São Paulo",
            "state_province_region": "SP",
            "country": "BR",
            "postal_code": "01310-100",
            "ip_address": None,
            "image_url": None,
            "phone_number": None,
            "proof_of_address_doc_type": "UTILITY_BILL",
            "proof_of_address_doc_file": "https://example.com/proof.png",
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01T00:00:00.000Z",
            "id_doc_country": "BR",
            "id_doc_type": "PASSPORT",
            "id_doc_front_file": "https://example.com/front.png",
            "id_doc_back_file": None,
            "legal_name": None,
            "alternate_name": None,
            "formation_date": None,
            "website": None,
            "owners": None,
            "incorporation_doc_file": None,
            "proof_of_ownership_doc_file": None,
            "source_of_funds_doc_type": None,
            "source_of_funds_doc_file": None,
            "selfie_file": None,
            "purpose_of_transactions": None,
            "purpose_of_transactions_explanation": None,
            "is_fbo": None,
            "account_purpose": None,
            "account_purpose_other": None,
            "business_type": None,
            "business_description": None,
            "business_industry": None,
            "estimated_annual_revenue": None,
            "source_of_wealth": None,
            "publicly_traded": None,
            "occupation": None,
            "external_id": None,
            "instance_id": "in_000000000000",
            "tos_id": "to_000000000000",
            "aml_status": None,
            "aml_hits": None,
            "created_at": "2021-01-01T00:00:00.000Z",
            "updated_at": "2021-01-01T00:00:00.000Z",
            "limit": {"per_transaction": 100000, "daily": 200000, "monthly": 1000000},
            "is_tos_accepted": None,
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_receiver, "error": None}

            response = self.blindpay.receivers.get("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_receiver
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/receivers/re_000000000000")

    def test_update(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": None, "error": None}

            response = self.blindpay.receivers.update(
                {
                    "receiver_id": "re_000000000000",
                    "email": "updated@example.com",
                    "country": "BR",
                    "first_name": "John",
                    "last_name": "Doe",
                    "tax_id": None,
                    "address_line_1": None,
                    "address_line_2": None,
                    "city": None,
                    "state_province_region": None,
                    "postal_code": None,
                    "ip_address": None,
                    "image_url": None,
                    "phone_number": None,
                    "proof_of_address_doc_type": None,
                    "proof_of_address_doc_file": None,
                    "date_of_birth": None,
                    "id_doc_country": None,
                    "id_doc_type": None,
                    "id_doc_front_file": None,
                    "id_doc_back_file": None,
                    "legal_name": None,
                    "alternate_name": None,
                    "formation_date": None,
                    "website": None,
                    "owners": None,
                    "incorporation_doc_file": None,
                    "proof_of_ownership_doc_file": None,
                    "source_of_funds_doc_type": None,
                    "source_of_funds_doc_file": None,
                    "selfie_file": None,
                    "purpose_of_transactions": None,
                    "purpose_of_transactions_explanation": None,
                    "account_purpose": None,
                    "account_purpose_other": None,
                    "business_type": None,
                    "business_description": None,
                    "business_industry": None,
                    "estimated_annual_revenue": None,
                    "source_of_wealth": None,
                    "publicly_traded": None,
                    "occupation": None,
                    "external_id": None,
                    "tos_id": None,
                }
            )

            assert response["error"] is None

    def test_delete(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": None, "error": None}

            response = self.blindpay.receivers.delete("re_000000000000")

            assert response["error"] is None
            mock_request.assert_called_once_with("DELETE", "/instances/in_000000000000/receivers/re_000000000000", None)

    def test_get_limits(self):
        mocked_limits = {
            "limits": {
                "payin": {"daily": 10000, "monthly": 50000},
                "payout": {"daily": 20000, "monthly": 100000},
            }
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_limits, "error": None}

            response = self.blindpay.receivers.get_limits("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_limits
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/limits/receivers/re_000000000000"
            )

    def test_get_limit_increase_requests(self):
        mocked_requests = [
            {
                "id": "rl_000000000000",
                "receiver_id": "re_000000000000",
                "status": "in_review",
                "daily": 50000,
                "monthly": 250000,
                "per_transaction": 25000,
                "supporting_document_file": "https://example.com/doc.pdf",
                "supporting_document_type": "individual_bank_statement",
                "created_at": "2025-01-01T00:00:00.000Z",
                "updated_at": "2025-01-01T00:00:00.000Z",
            }
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_requests, "error": None}

            response = self.blindpay.receivers.get_limit_increase_requests("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_requests
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/limit-increase"
            )

    def test_request_limit_increase(self):
        mocked_response = {"id": "rl_000000000000"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_response, "error": None}

            response = self.blindpay.receivers.request_limit_increase(
                {
                    "receiver_id": "re_000000000000",
                    "daily": 100000,
                    "monthly": 500000,
                    "per_transaction": 50000,
                    "supporting_document_file": "https://example.com/doc.pdf",
                    "supporting_document_type": "individual_bank_statement",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_response
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_000000000000/limit-increase",
                {
                    "daily": 100000,
                    "monthly": 500000,
                    "per_transaction": 50000,
                    "supporting_document_file": "https://example.com/doc.pdf",
                    "supporting_document_type": "individual_bank_statement",
                },
            )
