from typing import List, Optional, Union
from urllib.parse import urlencode

from typing_extensions import Literal, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import (
    BlindpayApiResponse,
    Country,
    PaginationMetadata,
    PaginationParams,
)

IndividualType = Literal["individual"]
BusinessType = Literal["business"]
StandardKycType = Literal["standard"]
EnhancedKycType = Literal["enhanced"]
KycType = Literal["light", "standard", "enhanced"]

ProofOfAddressDocType = Literal[
    "UTILITY_BILL", "BANK_STATEMENT", "RENTAL_AGREEMENT", "TAX_DOCUMENT", "GOVERNMENT_CORRESPONDENCE"
]

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

SourceOfFundsDocType = Literal[
    "business_income",
    "gambling_proceeds",
    "gifts",
    "government_benefits",
    "inheritance",
    "investment_loans",
    "pension_retirement",
    "salary",
    "sale_of_assets_real_estate",
    "savings",
    "esops",
    "investment_proceeds",
    "someone_else_funds",
]

SoleProprietorDocType = Literal["bank_statement", "master_service_agreement", "salary_slip"]

IdentificationDocument = Literal["PASSPORT", "ID_CARD", "DRIVERS"]

OwnerRole = Literal["beneficial_controlling", "beneficial_owner", "controlling_person"]

LimitIncreaseRequestStatus = Literal["in_review", "approved", "rejected"]

LimitIncreaseRequestSupportingDocumentType = Literal[
    "individual_bank_statement",
    "individual_tax_return",
    "individual_proof_of_income",
    "business_bank_statement",
    "business_financial_statements",
    "business_tax_return",
]

ReceiverStatus = Literal["verifying", "approved", "rejected", "deprecated", "pending_review"]

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

ReceiverBusinessType = Literal["corporation", "llc", "partnership", "sole_proprietorship", "trust", "non_profit"]

BusinessIndustry = Literal[
    "111998",
    "112120",
    "113310",
    "115114",
    "541211",
    "541810",
    "541430",
    "541715",
    "541930",
    "561422",
    "561311",
    "561612",
    "561740",
    "561730",
    "236115",
    "236220",
    "237310",
    "238210",
    "811111",
    "812111",
    "812112",
    "532111",
    "624410",
    "541922",
    "811210",
    "812199",
    "611110",
    "611310",
    "611410",
    "611710",
    "211120",
    "212114",
    "221310",
    "562111",
    "562920",
    "213112",
    "522110",
    "522210",
    "522320",
    "523150",
    "523940",
    "523999",
    "524113",
    "813110",
    "813211",
    "813219",
    "551112",
    "721110",
    "722511",
    "722513",
    "561510",
    "713110",
    "713210",
    "712110",
    "711110",
    "711211",
    "621111",
    "621210",
    "622110",
    "623110",
    "621511",
    "623220",
    "541940",
    "621399",
    "621910",
    "541110",
    "311421",
    "337121",
    "322220",
    "339920",
    "334210",
    "339930",
    "312130",
    "334111",
    "334118",
    "325412",
    "339112",
    "336110",
    "336390",
    "315990",
    "313110",
    "339910",
    "516120",
    "513130",
    "512250",
    "519130",
    "711410",
    "711510",
    "531110",
    "531120",
    "531130",
    "531190",
    "531210",
    "531311",
    "531312",
    "531320",
    "531390",
    "454110",
    "445110",
    "455110",
    "457110",
    "449210",
    "444110",
    "459210",
    "459120",
    "445320",
    "458110",
    "458210",
    "458310",
    "455219",
    "424210",
    "456110",
    "541511",
    "541512",
    "541519",
    "518210",
    "511210",
    "517111",
    "517112",
    "517410",
    "481111",
    "483111",
    "485210",
    "488510",
    "484121",
    "493110",
    "423430",
    "423690",
    "423110",
    "423830",
    "423840",
    "423510",
    "424690",
    "424990",
    "424410",
    "424480",
    "423940",
    "541611",
    "541618",
    "541330",
    "541990",
    "541214",
    "561499",
    "dapp",
    "exchange",
    "gambling",
    "gaming",
    "infra",
    "marketplace",
    "neo_bank",
    "other",
    "saas",
    "social",
    "wallet",
]

EstimatedAnnualRevenue = Literal[
    "0_99999",
    "100000_999999",
    "1000000_9999999",
    "10000000_49999999",
    "50000000_249999999",
    "2500000000_plus",
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

TaxType = Literal["SSN", "ITIN"]

AmlStatus = Literal["clear", "hit", "error"]


class FraudWarning(TypedDict):
    id: Optional[str]
    name: Optional[str]
    operation: Optional[str]
    score: Optional[float]


class AmlHits(TypedDict):
    has_sanction_match: bool
    has_pep_match: bool
    has_watchlist_match: bool
    has_crimelist_match: bool
    has_adversemedia_match: bool


class KycWarning(TypedDict):
    code: Optional[str]
    message: Optional[str]
    resolution_status: Optional[str]
    warning_id: Optional[str]


class TransactionLimit(TypedDict):
    per_transaction: float
    daily: float
    monthly: float


class Owner(TypedDict):
    id: str
    instance_id: str
    receiver_id: str
    role: OwnerRole
    first_name: str
    last_name: str
    date_of_birth: str
    tax_id: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Country
    postal_code: str
    id_doc_country: Country
    id_doc_type: IdentificationDocument
    id_doc_front_file: str
    id_doc_back_file: Optional[str]
    proof_of_address_doc_type: ProofOfAddressDocType
    proof_of_address_doc_file: str
    ownership_percentage: Optional[int]
    title: Optional[str]
    tax_type: Optional[TaxType]


class IndividualWithStandardKYC(TypedDict):
    id: str
    type: IndividualType
    kyc_type: StandardKycType
    kyc_status: str
    kyc_warnings: Optional[List[KycWarning]]
    email: str
    tax_id: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Country
    postal_code: str
    ip_address: Optional[str]
    image_url: Optional[str]
    phone_number: str
    proof_of_address_doc_type: ProofOfAddressDocType
    proof_of_address_doc_file: str
    first_name: str
    last_name: str
    date_of_birth: str
    id_doc_country: Country
    id_doc_type: IdentificationDocument
    id_doc_front_file: str
    id_doc_back_file: str
    aiprise_validation_key: str
    instance_id: str
    tos_id: Optional[str]
    created_at: str
    updated_at: str
    limit: TransactionLimit
    fraud_warnings: Optional[List[FraudWarning]]
    selfie_file: Optional[str]
    is_fbo: Optional[bool]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[ReceiverBusinessType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]
    external_id: Optional[str]
    aml_status: Optional[AmlStatus]
    aml_hits: Optional[AmlHits]
    is_tos_accepted: Optional[bool]


class IndividualWithEnhancedKYC(TypedDict):
    id: str
    type: IndividualType
    kyc_type: EnhancedKycType
    kyc_status: str
    kyc_warnings: Optional[List[KycWarning]]
    email: str
    tax_id: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Country
    postal_code: str
    ip_address: Optional[str]
    image_url: Optional[str]
    phone_number: Optional[str]
    proof_of_address_doc_type: ProofOfAddressDocType
    proof_of_address_doc_file: str
    first_name: str
    last_name: str
    date_of_birth: str
    id_doc_country: Country
    id_doc_type: IdentificationDocument
    id_doc_front_file: str
    id_doc_back_file: Optional[str]
    aiprise_validation_key: str
    instance_id: str
    source_of_funds_doc_type: str
    source_of_funds_doc_file: str
    individual_holding_doc_front_file: str
    purpose_of_transactions: PurposeOfTransactions
    purpose_of_transactions_explanation: Optional[str]
    tos_id: Optional[str]
    created_at: str
    updated_at: str
    limit: TransactionLimit
    fraud_warnings: Optional[List[FraudWarning]]
    selfie_file: Optional[str]
    is_fbo: Optional[bool]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[ReceiverBusinessType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]
    external_id: Optional[str]
    aml_status: Optional[AmlStatus]
    aml_hits: Optional[AmlHits]
    is_tos_accepted: Optional[bool]


class BusinessWithStandardKYB(TypedDict):
    id: str
    type: BusinessType
    kyc_type: StandardKycType
    kyc_status: str
    kyc_warnings: Optional[List[KycWarning]]
    email: str
    tax_id: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Country
    postal_code: str
    ip_address: Optional[str]
    image_url: Optional[str]
    phone_number: Optional[str]
    proof_of_address_doc_type: ProofOfAddressDocType
    proof_of_address_doc_file: str
    legal_name: str
    alternate_name: Optional[str]
    formation_date: str
    website: Optional[str]
    owners: List[Owner]
    incorporation_doc_file: str
    proof_of_ownership_doc_file: str
    external_id: Optional[str]
    instance_id: str
    tos_id: Optional[str]
    aiprise_validation_key: str
    created_at: str
    updated_at: str
    limit: TransactionLimit
    fraud_warnings: Optional[List[FraudWarning]]
    selfie_file: Optional[str]
    is_fbo: Optional[bool]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[ReceiverBusinessType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]
    aml_status: Optional[AmlStatus]
    aml_hits: Optional[AmlHits]
    is_tos_accepted: Optional[bool]


class CreateIndividualWithStandardKYCInput(TypedDict):
    external_id: Optional[str]
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    country: Country
    date_of_birth: str
    email: str
    first_name: str
    phone_number: Optional[str]
    id_doc_country: Country
    id_doc_front_file: str
    id_doc_type: IdentificationDocument
    id_doc_back_file: Optional[str]
    last_name: str
    postal_code: str
    proof_of_address_doc_file: str
    proof_of_address_doc_type: ProofOfAddressDocType
    state_province_region: str
    tax_id: str
    tos_id: str
    ip_address: Optional[str]
    image_url: Optional[str]
    selfie_file: Optional[str]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    occupation: Optional[str]


class CreateIndividualWithStandardKYCResponse(TypedDict):
    id: str


class CreateIndividualWithEnhancedKYCInput(TypedDict):
    external_id: Optional[str]
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    country: Country
    date_of_birth: str
    email: str
    first_name: str
    id_doc_country: Country
    id_doc_front_file: str
    id_doc_type: IdentificationDocument
    id_doc_back_file: Optional[str]
    individual_holding_doc_front_file: str
    last_name: str
    postal_code: str
    phone_number: Optional[str]
    proof_of_address_doc_file: str
    proof_of_address_doc_type: ProofOfAddressDocType
    purpose_of_transactions: PurposeOfTransactions
    source_of_funds_doc_file: str
    source_of_funds_doc_type: SourceOfFundsDocType
    purpose_of_transactions_explanation: Optional[str]
    state_province_region: str
    tax_id: str
    tos_id: str
    ip_address: Optional[str]
    image_url: Optional[str]
    selfie_file: Optional[str]
    is_fbo: Optional[bool]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    occupation: Optional[str]


class CreateIndividualWithEnhancedKYCResponse(TypedDict):
    id: str


class CreateBusinessWithStandardKYBInput(TypedDict):
    external_id: Optional[str]
    address_line_1: str
    address_line_2: Optional[str]
    alternate_name: str
    city: str
    country: Country
    email: str
    formation_date: str
    incorporation_doc_file: str
    legal_name: str
    owners: List[Owner]
    postal_code: str
    proof_of_address_doc_file: str
    proof_of_address_doc_type: ProofOfAddressDocType
    proof_of_ownership_doc_file: str
    state_province_region: str
    tax_id: str
    tos_id: str
    website: Optional[str]
    ip_address: Optional[str]
    image_url: Optional[str]
    phone_number: Optional[str]
    selfie_file: Optional[str]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[ReceiverBusinessType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]


class CreateBusinessWithStandardKYBResponse(TypedDict):
    id: str


ListReceiversResponse = List[Union[IndividualWithStandardKYC, IndividualWithEnhancedKYC, BusinessWithStandardKYB]]


class ListReceiversPaginatedResponse(TypedDict):
    data: List[Union[IndividualWithStandardKYC, IndividualWithEnhancedKYC, BusinessWithStandardKYB]]
    pagination: PaginationMetadata


class ListReceiversInput(PaginationParams, total=False):
    full_name: str
    receiver_name: str
    status: ReceiverStatus
    receiver_id: str
    bank_account_id: str
    country: str


GetReceiverResponse = Union[IndividualWithStandardKYC, IndividualWithEnhancedKYC, BusinessWithStandardKYB]


class OwnerUpdate(TypedDict):
    id: str
    first_name: str
    last_name: str
    role: OwnerRole
    date_of_birth: str
    tax_id: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Country
    postal_code: str
    id_doc_country: Country
    id_doc_type: IdentificationDocument
    id_doc_front_file: str
    id_doc_back_file: Optional[str]
    ownership_percentage: Optional[int]
    title: Optional[str]
    tax_type: Optional[TaxType]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    proof_of_address_doc_file: Optional[str]


class UpdateReceiverInput(TypedDict):
    receiver_id: str
    email: Optional[str]
    tax_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Optional[Country]
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
    id_doc_type: Optional[IdentificationDocument]
    id_doc_front_file: Optional[str]
    id_doc_back_file: Optional[str]
    legal_name: Optional[str]
    alternate_name: Optional[str]
    formation_date: Optional[str]
    website: Optional[str]
    owners: Optional[List[OwnerUpdate]]
    incorporation_doc_file: Optional[str]
    proof_of_ownership_doc_file: Optional[str]
    source_of_funds_doc_type: Optional[SourceOfFundsDocType]
    source_of_funds_doc_file: Optional[str]
    individual_holding_doc_front_file: Optional[str]
    purpose_of_transactions: Optional[PurposeOfTransactions]
    purpose_of_transactions_explanation: Optional[str]
    external_id: Optional[str]
    tos_id: Optional[str]
    selfie_file: Optional[str]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[ReceiverBusinessType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]


class PayinLimit(TypedDict):
    daily: float
    monthly: float


class PayoutLimit(TypedDict):
    daily: float
    monthly: float


class Limits(TypedDict):
    payin: PayinLimit
    payout: PayoutLimit


class GetReceiverLimitsResponse(TypedDict):
    limits: Limits


class LimitIncreaseRequest(TypedDict):
    id: str
    receiver_id: str
    status: LimitIncreaseRequestStatus
    daily: float
    monthly: float
    per_transaction: float
    supporting_document_file: str
    supporting_document_type: LimitIncreaseRequestSupportingDocumentType
    created_at: str
    updated_at: str


GetLimitIncreaseRequestsResponse = List[LimitIncreaseRequest]


class RequestLimitIncreaseInput(TypedDict):
    receiver_id: str
    daily: float
    monthly: float
    per_transaction: float
    supporting_document_file: str
    supporting_document_type: LimitIncreaseRequestSupportingDocumentType


class RequestLimitIncreaseResponse(TypedDict):
    id: str


class ReceiversResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(
        self, params: Optional[ListReceiversInput] = None
    ) -> BlindpayApiResponse[Union[ListReceiversResponse, ListReceiversPaginatedResponse]]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return await self._client.get(f"/instances/{self._instance_id}/receivers{query_string}")

    async def create_individual_with_standard_kyc(
        self, data: CreateIndividualWithStandardKYCInput
    ) -> BlindpayApiResponse[CreateIndividualWithStandardKYCResponse]:
        payload = {"kyc_type": "standard", "type": "individual", **data}
        return await self._client.post(f"/instances/{self._instance_id}/receivers", payload)

    async def create_individual_with_enhanced_kyc(
        self, data: CreateIndividualWithEnhancedKYCInput
    ) -> BlindpayApiResponse[CreateIndividualWithEnhancedKYCResponse]:
        payload = {"kyc_type": "enhanced", "type": "individual", **data}
        return await self._client.post(f"/instances/{self._instance_id}/receivers", payload)

    async def create_business_with_standard_kyb(
        self, data: CreateBusinessWithStandardKYBInput
    ) -> BlindpayApiResponse[CreateBusinessWithStandardKYBResponse]:
        payload = {"kyc_type": "standard", "type": "business", **data}
        return await self._client.post(f"/instances/{self._instance_id}/receivers", payload)

    async def get(self, receiver_id: str) -> BlindpayApiResponse[GetReceiverResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}")

    async def update(self, data: UpdateReceiverInput) -> BlindpayApiResponse[None]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        return await self._client.put(f"/instances/{self._instance_id}/receivers/{receiver_id}", payload)

    async def delete(self, receiver_id: str) -> BlindpayApiResponse[None]:
        return await self._client.delete(f"/instances/{self._instance_id}/receivers/{receiver_id}")

    async def get_limits(self, receiver_id: str) -> BlindpayApiResponse[GetReceiverLimitsResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/limits/receivers/{receiver_id}")

    async def get_limit_increase_requests(
        self, receiver_id: str
    ) -> BlindpayApiResponse[GetLimitIncreaseRequestsResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/limit-increase")

    async def request_limit_increase(
        self, data: RequestLimitIncreaseInput
    ) -> BlindpayApiResponse[RequestLimitIncreaseResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        return await self._client.post(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/limit-increase", payload
        )


class ReceiversResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(
        self, params: Optional[ListReceiversInput] = None
    ) -> BlindpayApiResponse[Union[ListReceiversResponse, ListReceiversPaginatedResponse]]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return self._client.get(f"/instances/{self._instance_id}/receivers{query_string}")

    def create_individual_with_standard_kyc(
        self, data: CreateIndividualWithStandardKYCInput
    ) -> BlindpayApiResponse[CreateIndividualWithStandardKYCResponse]:
        payload = {"kyc_type": "standard", "type": "individual", **data}
        return self._client.post(f"/instances/{self._instance_id}/receivers", payload)

    def create_individual_with_enhanced_kyc(
        self, data: CreateIndividualWithEnhancedKYCInput
    ) -> BlindpayApiResponse[CreateIndividualWithEnhancedKYCResponse]:
        payload = {"kyc_type": "enhanced", "type": "individual", **data}
        return self._client.post(f"/instances/{self._instance_id}/receivers", payload)

    def create_business_with_standard_kyb(
        self, data: CreateBusinessWithStandardKYBInput
    ) -> BlindpayApiResponse[CreateBusinessWithStandardKYBResponse]:
        payload = {"kyc_type": "standard", "type": "business", **data}
        return self._client.post(f"/instances/{self._instance_id}/receivers", payload)

    def get(self, receiver_id: str) -> BlindpayApiResponse[GetReceiverResponse]:
        return self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}")

    def update(self, data: UpdateReceiverInput) -> BlindpayApiResponse[None]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        return self._client.put(f"/instances/{self._instance_id}/receivers/{receiver_id}", payload)

    def delete(self, receiver_id: str) -> BlindpayApiResponse[None]:
        return self._client.delete(f"/instances/{self._instance_id}/receivers/{receiver_id}")

    def get_limits(self, receiver_id: str) -> BlindpayApiResponse[GetReceiverLimitsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/limits/receivers/{receiver_id}")

    def get_limit_increase_requests(self, receiver_id: str) -> BlindpayApiResponse[GetLimitIncreaseRequestsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/limit-increase")

    def request_limit_increase(
        self, data: RequestLimitIncreaseInput
    ) -> BlindpayApiResponse[RequestLimitIncreaseResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/limit-increase", payload)


def create_receivers_resource(instance_id: str, client: InternalApiClient) -> ReceiversResource:
    return ReceiversResource(instance_id, client)


def create_receivers_resource_sync(instance_id: str, client: InternalApiClientSync) -> ReceiversResourceSync:
    return ReceiversResourceSync(instance_id, client)
