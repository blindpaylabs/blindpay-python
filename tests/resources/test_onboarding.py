from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync
from blindpay.resources.instances import (
    OnboardingBusinessDetails,
    OnboardingBusinessProfile,
    OnboardingOwnershipDocuments,
)
from tests.spec_fixtures import assert_matches_spec, response_variants

BASE = "/v1/instances/{instance_id}/onboarding/"
DETAILS = response_variants("GET " + BASE + "business_details")
PROFILE = response_variants("GET " + BASE + "business_profile")
DOCUMENTS = response_variants("GET " + BASE + "ownership_documents")


class TestOnboarding:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test_key", instance_id="in_000000000000")

    def test_types_match_the_spec(self):
        assert_matches_spec(OnboardingBusinessDetails, DETAILS)
        assert_matches_spec(OnboardingBusinessProfile, PROFILE)
        assert_matches_spec(OnboardingOwnershipDocuments, DOCUMENTS)

    @pytest.mark.asyncio
    async def test_getters(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": DETAILS["full"], "error": None}

            await self.blindpay.instances.onboarding.get_business_details()
            await self.blindpay.instances.onboarding.get_business_profile()
            await self.blindpay.instances.onboarding.get_ownership_documents()

            assert [c.args for c in mock_request.call_args_list] == [
                ("GET", "/instances/in_000000000000/onboarding/business_details"),
                ("GET", "/instances/in_000000000000/onboarding/business_profile"),
                ("GET", "/instances/in_000000000000/onboarding/ownership_documents"),
            ]


class TestOnboardingSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test_key", instance_id="in_000000000000")

    def test_get_ownership_documents(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": DOCUMENTS["full"], "error": None}

            response = self.blindpay.instances.onboarding.get_ownership_documents()

            assert response["data"] == DOCUMENTS["full"]
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/onboarding/ownership_documents")
