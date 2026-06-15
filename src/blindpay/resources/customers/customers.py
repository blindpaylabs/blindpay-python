from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

from typing_extensions import Literal, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse, Country, PaginationMetadata, PaginationParams

# Customer Types
CustomerType = Literal["individual", "business"]
KycType = Literal["light", "standard", "enhanced"]

ProofOfAddressDocType = Literal[
    "UTILITY_BILL", "BANK_STATEMENT", "RENTAL_AGREEMENT", "TAX_DOCUMENT", "GOVERNMENT_CORRESPONDENCE"
]

IdDocType = Literal["PASSPORT", "ID_CARD", "DRIVERS"]

PurposeOfTransactions = Literal[
    "business_transactions",
    "charitable_donations",
    "investment_purposes",
    "payments_to_friends_or_family_abroad",
    "personal_or_living_expenses",
    "protect_wealth",
    "purchase_good_and_services",
    "receive_payment_for_freelancing",
    "receive_salary",
    "other",
]

AccountPurpose = Literal[
    "charitable_donations",
    "ecommerce_retail_payments",
    "investment_purposes",
    "business_expenses",
    "payments_to_friends_or_family_abroad",
    "personal_or_living_expenses",
    "protect_wealth",
    "purchase_goods_and_services",
    "receive_payments_for_goods_and_services",
    "tax_optimization",
    "third_party_money_transmission",
    "payroll",
    "treasury_management",
    "other",
]

BusinessType = Literal["corporation", "llc", "partnership", "sole_proprietorship", "trust", "non_profit"]

EstimatedAnnualRevenue = Literal[
    "0_99999", "100000_999999", "1000000_9999999", "10000000_49999999", "50000000_249999999", "250000000_plus"
]

SourceOfWealth = Literal[
    "business_dividends_or_profits",
    "investments",
    "asset_sales",
    "client_investor_contributions",
    "gambling",
    "charitable_contributions",
    "inheritance",
    "affiliate_or_royalty_income",
]

# Business Industry - abbreviated list (144 values mentioned in changelog)
BusinessIndustry = Literal[
    "technology",
    "finance",
    "healthcare",
    "retail",
    "manufacturing",
    "agriculture",
    "education",
    "transportation",
    "real_estate",
    "consulting",
    # ... (This would need to be expanded with all 144 values)
]


# Additional Info Item
class AdditionalInfoItem(TypedDict):
    key: str
    value: str


# Main Customer TypedDict
class Customer(TypedDict):
    id: str
    customer_id: str
    type: CustomerType
    kyc_type: KycType
    email: str
    tax_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Country
    postal_code: Optional[str]
    ip_address: Optional[str]
    image_url: Optional[str]
    phone_number: Optional[str]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    proof_of_address_doc_file: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[str]  # Using str for unknown type
    id_doc_country: Optional[Country]
    id_doc_type: Optional[IdDocType]
    id_doc_front_file: Optional[str]
    id_doc_back_file: Optional[str]
    legal_name: Optional[str]
    alternate_name: Optional[str]
    formation_date: Optional[str]  # Using str for date-time
    website: Optional[str]
    owners: Optional[List[Dict[str, Any]]]  # Array of objects
    incorporation_doc_file: Optional[str]
    proof_of_ownership_doc_file: Optional[str]
    source_of_funds_doc_file: Optional[str]
    selfie_file: Optional[str]
    purpose_of_transactions: Optional[PurposeOfTransactions]
    purpose_of_transactions_explanation: Optional[str]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[BusinessType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]
    external_id: Optional[str]
    tos_id: Optional[str]
    additional_info: Optional[List[AdditionalInfoItem]]


# Input/Output Types
class CreateCustomerInput(TypedDict):
    type: CustomerType
    kyc_type: KycType
    email: str
    tax_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Country
    postal_code: Optional[str]
    ip_address: Optional[str]
    image_url: Optional[str]
    phone_number: Optional[str]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    proof_of_address_doc_file: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[str]
    id_doc_country: Optional[Country]
    id_doc_type: Optional[IdDocType]
    id_doc_front_file: Optional[str]
    id_doc_back_file: Optional[str]
    legal_name: Optional[str]
    alternate_name: Optional[str]
    formation_date: Optional[str]
    website: Optional[str]
    owners: Optional[List[Dict[str, Any]]]
    incorporation_doc_file: Optional[str]
    proof_of_ownership_doc_file: Optional[str]
    source_of_funds_doc_file: Optional[str]
    selfie_file: Optional[str]
    purpose_of_transactions: Optional[PurposeOfTransactions]
    purpose_of_transactions_explanation: Optional[str]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[BusinessType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]
    external_id: Optional[str]
    tos_id: Optional[str]
    additional_info: Optional[List[AdditionalInfoItem]]


class CreateCustomerResponse(TypedDict):
    id: str
    customer_id: str


class UpdateCustomerInput(TypedDict):
    email: str
    tax_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Country
    postal_code: Optional[str]
    ip_address: Optional[str]
    image_url: Optional[str]
    phone_number: Optional[str]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    proof_of_address_doc_file: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[str]
    id_doc_country: Optional[Country]
    id_doc_type: Optional[IdDocType]
    id_doc_front_file: Optional[str]
    id_doc_back_file: Optional[str]
    legal_name: Optional[str]
    alternate_name: Optional[str]
    formation_date: Optional[str]
    website: Optional[str]
    owners: Optional[List[Dict[str, Any]]]
    incorporation_doc_file: Optional[str]
    proof_of_ownership_doc_file: Optional[str]
    source_of_funds_doc_file: Optional[str]
    selfie_file: Optional[str]
    purpose_of_transactions: Optional[PurposeOfTransactions]
    purpose_of_transactions_explanation: Optional[str]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[BusinessType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]
    external_id: Optional[str]
    tos_id: Optional[str]
    additional_info: Optional[List[AdditionalInfoItem]]


class ListCustomersResponse(TypedDict):
    data: List[Customer]
    pagination: PaginationMetadata


class SuccessResponse(TypedDict):
    success: bool


# --- Async resource ---


class CustomersResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, params: Optional[PaginationParams] = None) -> BlindpayApiResponse[ListCustomersResponse]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return await self._client.get(f"/instances/{self._instance_id}/customers{query_string}")

    async def get(self, customer_id: str) -> BlindpayApiResponse[Customer]:
        return await self._client.get(f"/instances/{self._instance_id}/customers/{customer_id}")

    async def create(self, data: CreateCustomerInput) -> BlindpayApiResponse[CreateCustomerResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/customers", data)

    async def update(self, customer_id: str, data: UpdateCustomerInput) -> BlindpayApiResponse[SuccessResponse]:
        return await self._client.put(f"/instances/{self._instance_id}/customers/{customer_id}", data)

    async def delete(self, customer_id: str) -> BlindpayApiResponse[SuccessResponse]:
        return await self._client.delete(f"/instances/{self._instance_id}/customers/{customer_id}")


# --- Sync resource ---


class CustomersResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, params: Optional[PaginationParams] = None) -> BlindpayApiResponse[ListCustomersResponse]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return self._client.get(f"/instances/{self._instance_id}/customers{query_string}")

    def get(self, customer_id: str) -> BlindpayApiResponse[Customer]:
        return self._client.get(f"/instances/{self._instance_id}/customers/{customer_id}")

    def create(self, data: CreateCustomerInput) -> BlindpayApiResponse[CreateCustomerResponse]:
        return self._client.post(f"/instances/{self._instance_id}/customers", data)

    def update(self, customer_id: str, data: UpdateCustomerInput) -> BlindpayApiResponse[SuccessResponse]:
        return self._client.put(f"/instances/{self._instance_id}/customers/{customer_id}", data)

    def delete(self, customer_id: str) -> BlindpayApiResponse[SuccessResponse]:
        return self._client.delete(f"/instances/{self._instance_id}/customers/{customer_id}")


# --- Factory functions ---


def create_customers_resource(instance_id: str, client: InternalApiClient) -> CustomersResource:
    return CustomersResource(instance_id, client)


def create_customers_resource_sync(instance_id: str, client: InternalApiClientSync) -> CustomersResourceSync:
    return CustomersResourceSync(instance_id, client)
