from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestAvailable:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_get_bank_details(self):
        mocked_bank_details = [
            {
                "label": "Account Type",
                "regex": "",
                "key": "account_type",
                "items": [
                    {
                        "label": "Checking",
                        "value": "checking",
                    },
                    {
                        "label": "Savings",
                        "value": "saving",
                    },
                ],
                "required": True,
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_bank_details, "error": None}

            response = await self.blindpay.available.get_bank_details("pix")

            assert response["error"] is None
            assert response["data"] == mocked_bank_details
            mock_request.assert_called_once_with("GET", "/available/bank-details?rail=pix")

    @pytest.mark.asyncio
    async def test_get_rails(self):
        mocked_rails = [
            {
                "label": "Domestic Wire",
                "value": "wire",
                "country": "US",
            },
            {
                "label": "ACH",
                "value": "ach",
                "country": "US",
            },
            {
                "label": "PIX",
                "value": "pix",
                "country": "BR",
            },
            {
                "label": "SPEI",
                "value": "spei_bitso",
                "country": "MX",
            },
            {
                "label": "Transfers 3.0",
                "value": "transfers_bitso",
                "country": "AR",
            },
            {
                "label": "ACH Colombia",
                "value": "ach_cop_bitso",
                "country": "CO",
            },
            {
                "label": "International Swift",
                "value": "international_swift",
                "country": "US",
            },
            {
                "label": "RTP",
                "value": "rtp",
                "country": "US",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_rails, "error": None}

            response = await self.blindpay.available.get_rails()

            assert response["error"] is None
            assert response["data"] == mocked_rails
            mock_request.assert_called_once_with("GET", "/available/rails")

    @pytest.mark.asyncio
    async def test_get_swift_code_bank_details(self):
        mocked_bank_details = [
            {
                "id": "416",
                "bank": "BANK OF AMERICA, N.A.",
                "city": "NEW JERSEY",
                "branch": "LENDING SERVICES AND OPERATIONS (LSOP)",
                "swiftCode": "BOFAUS3NLMA",
                "swiftCodeLink": "https://bank.codes/swift-code/united-states/bofaus3nlma/",
                "country": "United States",
                "countrySlug": "united-states",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_bank_details, "error": None}

            response = await self.blindpay.available.get_swift_code_bank_details("BOFAUS3NLMA")

            assert response["error"] is None
            assert response["data"] == mocked_bank_details
            mock_request.assert_called_once_with("GET", "/available/swift/BOFAUS3NLMA")


class TestAvailableSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_get_bank_details(self):
        mocked_bank_details = [
            {
                "label": "Account Type",
                "regex": "",
                "key": "account_type",
                "items": [
                    {
                        "label": "Checking",
                        "value": "checking",
                    },
                    {
                        "label": "Savings",
                        "value": "saving",
                    },
                ],
                "required": True,
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_bank_details, "error": None}

            response = self.blindpay.available.get_bank_details("pix")

            assert response["error"] is None
            assert response["data"] == mocked_bank_details
            mock_request.assert_called_once_with("GET", "/available/bank-details?rail=pix")

    def test_get_rails(self):
        mocked_rails = [
            {
                "label": "Domestic Wire",
                "value": "wire",
                "country": "US",
            },
            {
                "label": "ACH",
                "value": "ach",
                "country": "US",
            },
            {
                "label": "PIX",
                "value": "pix",
                "country": "BR",
            },
            {
                "label": "SPEI",
                "value": "spei_bitso",
                "country": "MX",
            },
            {
                "label": "Transfers 3.0",
                "value": "transfers_bitso",
                "country": "AR",
            },
            {
                "label": "ACH Colombia",
                "value": "ach_cop_bitso",
                "country": "CO",
            },
            {
                "label": "International Swift",
                "value": "international_swift",
                "country": "US",
            },
            {
                "label": "RTP",
                "value": "rtp",
                "country": "US",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_rails, "error": None}

            response = self.blindpay.available.get_rails()

            assert response["error"] is None
            assert response["data"] == mocked_rails
            mock_request.assert_called_once_with("GET", "/available/rails")

    def test_get_swift_code_bank_details(self):
        mocked_bank_details = [
            {
                "id": "416",
                "bank": "BANK OF AMERICA, N.A.",
                "city": "NEW JERSEY",
                "branch": "LENDING SERVICES AND OPERATIONS (LSOP)",
                "swiftCode": "BOFAUS3NLMA",
                "swiftCodeLink": "https://bank.codes/swift-code/united-states/bofaus3nlma/",
                "country": "United States",
                "countrySlug": "united-states",
            },
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_bank_details, "error": None}

            response = self.blindpay.available.get_swift_code_bank_details("BOFAUS3NLMA")

            assert response["error"] is None
            assert response["data"] == mocked_bank_details
            mock_request.assert_called_once_with("GET", "/available/swift/BOFAUS3NLMA")
