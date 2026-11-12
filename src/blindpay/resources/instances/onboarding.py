from typing import List, Optional, Union

from typing_extensions import Literal, NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions
from ...types import BlindpayApiResponse, Country

OnboardingEntityType = Literal[
    "cooperative", "corporation", "company", "partnership", "sole_proprietor", "trust", "other"
]
OnboardingScenario = Literal["custodial", "custodial_mtl", "non_custodial", "other"]
OnboardingBusinessIndustry = Literal[
    "wallet", "exchange", "dapp", "neo_bank", "gaming", "marketplace", "saas", "social", "infra", "gambling", "other"
]
OnboardingEstimatedVolume = Literal["up_to_100", "up_to_500", "up_to_1000", "up_to_10000", "more_than_10000"]
OnboardingProofOfAddressDocType = Literal[
    "UTILITY_BILL", "BANK_STATEMENT", "RENTAL_AGREEMENT", "TAX_DOCUMENT", "GOVERNMENT_CORRESPONDENCE"
]
OnboardingOwnerRole = Literal["beneficial_controlling", "beneficial_owner", "controlling_person"]
OnboardingIdDocType = Literal["PASSPORT", "ID_CARD", "DRIVERS"]


class OnboardingBusinessDetails(TypedDict):
    legal_name: NotRequired[str]
    tax_id: NotRequired[str]
    formation_date: NotRequired[str]
    trading_names: NotRequired[List[str]]
    address_line_1: NotRequired[str]
    address_line_2: NotRequired[Optional[str]]
    city: NotRequired[str]
    state_province_region: NotRequired[str]
    postal_code: NotRequired[str]
    country: NotRequired[Union[Country, str]]
    entity_type: NotRequired[Union[OnboardingEntityType, str]]
    state_of_incorporation: NotRequired[str]


class OnboardingBusinessProfile(TypedDict):
    scenario: NotRequired[Union[OnboardingScenario, str]]
    scenario_description: NotRequired[Optional[str]]
    has_kyc_screening: NotRequired[Optional[bool]]
    is_regulated: NotRequired[Optional[bool]]
    business_industry: NotRequired[Union[OnboardingBusinessIndustry, str]]
    website: NotRequired[Optional[str]]
    top_volume_by_country: NotRequired[List[Union[Country, str]]]
    estimated_volume_per_month: NotRequired[Union[OnboardingEstimatedVolume, str]]


class OnboardingOwner(TypedDict):
    id: NotRequired[str]
    instance_id: NotRequired[str]
    role: NotRequired[Union[OnboardingOwnerRole, str]]
    first_name: NotRequired[str]
    last_name: NotRequired[str]
    ownership_percentage: NotRequired[Optional[float]]
    date_of_birth: NotRequired[str]
    tax_id: NotRequired[str]
    address_line_1: NotRequired[str]
    address_line_2: NotRequired[Optional[str]]
    city: NotRequired[str]
    state_province_region: NotRequired[str]
    country: NotRequired[Union[Country, str]]
    postal_code: NotRequired[str]
    id_doc_country: NotRequired[Union[Country, str]]
    id_doc_type: NotRequired[Union[OnboardingIdDocType, str]]
    id_doc_front_file: NotRequired[Optional[str]]
    id_doc_back_file: NotRequired[Optional[str]]
    proof_of_address_doc_type: NotRequired[Optional[Union[OnboardingProofOfAddressDocType, str]]]
    proof_of_address_doc_file: NotRequired[Optional[str]]


class OnboardingOwnershipDocuments(TypedDict):
    incorporation_doc_file: NotRequired[Optional[str]]
    proof_of_ownership_doc_file: NotRequired[Optional[str]]
    proof_of_address_doc_type: NotRequired[Optional[Union[OnboardingProofOfAddressDocType, str]]]
    proof_of_address_doc_file: NotRequired[Optional[str]]
    owners: NotRequired[Optional[List[OnboardingOwner]]]


class OnboardingResource:
    """Read the instance's own onboarding answers (what the dashboard's onboarding flow collected)."""

    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def get_business_details(
        self, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[OnboardingBusinessDetails]:
        return await self._client.get(f"/instances/{self._instance_id}/onboarding/business_details", options=options)

    async def get_business_profile(
        self, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[OnboardingBusinessProfile]:
        return await self._client.get(f"/instances/{self._instance_id}/onboarding/business_profile", options=options)

    async def get_ownership_documents(
        self, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[OnboardingOwnershipDocuments]:
        return await self._client.get(f"/instances/{self._instance_id}/onboarding/ownership_documents", options=options)


class OnboardingResourceSync:
    """Read the instance's own onboarding answers (what the dashboard's onboarding flow collected)."""

    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def get_business_details(
        self, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[OnboardingBusinessDetails]:
        return self._client.get(f"/instances/{self._instance_id}/onboarding/business_details", options=options)

    def get_business_profile(
        self, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[OnboardingBusinessProfile]:
        return self._client.get(f"/instances/{self._instance_id}/onboarding/business_profile", options=options)

    def get_ownership_documents(
        self, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[OnboardingOwnershipDocuments]:
        return self._client.get(f"/instances/{self._instance_id}/onboarding/ownership_documents", options=options)


def create_onboarding_resource(instance_id: str, client: InternalApiClient) -> OnboardingResource:
    return OnboardingResource(instance_id, client)


def create_onboarding_resource_sync(instance_id: str, client: InternalApiClientSync) -> OnboardingResourceSync:
    return OnboardingResourceSync(instance_id, client)
