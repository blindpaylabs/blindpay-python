from typing import List, Optional
from urllib.parse import urlencode

from typing_extensions import Literal, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import (
    BlindpayApiResponse,
    Country,
    PaginationMetadata,
    PaginationParams,
)

ReceiverType = Literal["individual", "business"]
KycType = Literal["light", "standard", "enhanced"]
KycStatus = Literal["verifying", "approved", "rejected", "deprecated", "pending_review"]
AmlStatus = Literal["clear", "hit", "error"]
IdentificationDocument = Literal["PASSPORT", "ID_CARD", "DRIVERS"]
OwnerRole = Literal["beneficial_controlling", "beneficial_owner", "controlling_person"]

ProofOfAddressDocType = Literal[
    "UTILITY_BILL", "BANK_STATEMENT", "RENTAL_AGREEMENT", "TAX_DOCUMENT", "GOVERNMENT_CORRESPONDENCE"
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

BusinessEntityType = Literal["corporation", "llc", "partnership", "sole_proprietorship", "trust", "non_profit"]

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
]

EstimatedAnnualRevenue = Literal[
    "0_99999", "100000_999999", "1000000_9999999", "10000000_49999999", "50000000_249999999", "2500000000_plus"
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

LimitIncreaseRequestStatus = Literal["in_review", "approved", "rejected"]

LimitIncreaseRequestSupportingDocumentType = Literal[
    "individual_bank_statement",
    "individual_tax_return",
    "individual_proof_of_income",
    "business_bank_statement",
    "business_financial_statements",
    "business_tax_return",
]


class KycWarning(TypedDict):
    code: Optional[str]
    message: Optional[str]
    resolution_status: Optional[str]
    warning_id: Optional[str]


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


class TransactionLimit(TypedDict):
    per_transaction: Optional[float]
    daily: Optional[float]
    monthly: Optional[float]


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
    id_doc_front_file: Optional[str]
    id_doc_back_file: Optional[str]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    proof_of_address_doc_file: Optional[str]
    ownership_percentage: Optional[int]
    title: Optional[str]
    tax_type: Optional[TaxType]


class OwnerInput(TypedDict):
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
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    proof_of_address_doc_file: Optional[str]
    ownership_percentage: Optional[int]
    title: Optional[str]
    tax_type: Optional[TaxType]


class OwnerUpdateInput(TypedDict):
    id: str
    role: Optional[OwnerRole]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[str]
    tax_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Optional[Country]
    postal_code: Optional[str]
    id_doc_country: Optional[Country]
    id_doc_type: Optional[IdentificationDocument]
    id_doc_front_file: Optional[str]
    id_doc_back_file: Optional[str]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    proof_of_address_doc_file: Optional[str]
    ownership_percentage: Optional[int]
    title: Optional[str]
    tax_type: Optional[TaxType]


class Receiver(TypedDict):
    id: str
    type: ReceiverType
    kyc_type: KycType
    kyc_status: KycStatus
    kyc_warnings: Optional[List[KycWarning]]
    fraud_warnings: Optional[List[FraudWarning]]
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
    id_doc_type: Optional[IdentificationDocument]
    id_doc_front_file: Optional[str]
    id_doc_back_file: Optional[str]
    legal_name: Optional[str]
    alternate_name: Optional[str]
    formation_date: Optional[str]
    website: Optional[str]
    owners: Optional[List[Owner]]
    incorporation_doc_file: Optional[str]
    proof_of_ownership_doc_file: Optional[str]
    source_of_funds_doc_type: Optional[SourceOfFundsDocType]
    source_of_funds_doc_file: Optional[str]
    selfie_file: Optional[str]
    purpose_of_transactions: Optional[PurposeOfTransactions]
    purpose_of_transactions_explanation: Optional[str]
    is_fbo: Optional[bool]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[BusinessEntityType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]
    external_id: Optional[str]
    instance_id: str
    tos_id: Optional[str]
    aml_status: Optional[AmlStatus]
    aml_hits: Optional[AmlHits]
    created_at: Optional[str]
    updated_at: Optional[str]
    limit: TransactionLimit
    is_tos_accepted: Optional[bool]


class CreateReceiverInput(TypedDict):
    type: ReceiverType
    kyc_type: KycType
    email: str
    country: Country
    tax_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
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
    owners: Optional[List[OwnerInput]]
    incorporation_doc_file: Optional[str]
    proof_of_ownership_doc_file: Optional[str]
    source_of_funds_doc_type: Optional[SourceOfFundsDocType]
    source_of_funds_doc_file: Optional[str]
    selfie_file: Optional[str]
    purpose_of_transactions: Optional[PurposeOfTransactions]
    purpose_of_transactions_explanation: Optional[str]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[BusinessEntityType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]
    external_id: Optional[str]
    tos_id: Optional[str]


class CreateReceiverResponse(TypedDict):
    id: str


class ListReceiversInput(PaginationParams, total=False):
    full_name: str
    receiver_name: str
    status: KycStatus
    receiver_id: str
    bank_account_id: str
    country: Country


class ListReceiversResponse(TypedDict):
    data: List[Receiver]
    pagination: PaginationMetadata


class UpdateReceiverInput(TypedDict):
    receiver_id: str
    email: str
    country: Country
    tax_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
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
    owners: Optional[List[OwnerUpdateInput]]
    incorporation_doc_file: Optional[str]
    proof_of_ownership_doc_file: Optional[str]
    source_of_funds_doc_type: Optional[SourceOfFundsDocType]
    source_of_funds_doc_file: Optional[str]
    selfie_file: Optional[str]
    purpose_of_transactions: Optional[PurposeOfTransactions]
    purpose_of_transactions_explanation: Optional[str]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[BusinessEntityType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]
    external_id: Optional[str]
    tos_id: Optional[str]


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


# --- Async resource ---


class ReceiversResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, params: Optional[ListReceiversInput] = None) -> BlindpayApiResponse[ListReceiversResponse]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return await self._client.get(f"/instances/{self._instance_id}/receivers{query_string}")

    async def create(self, data: CreateReceiverInput) -> BlindpayApiResponse[CreateReceiverResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/receivers", data)

    async def get(self, receiver_id: str) -> BlindpayApiResponse[Receiver]:
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


# --- Sync resource ---


class ReceiversResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, params: Optional[ListReceiversInput] = None) -> BlindpayApiResponse[ListReceiversResponse]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return self._client.get(f"/instances/{self._instance_id}/receivers{query_string}")

    def create(self, data: CreateReceiverInput) -> BlindpayApiResponse[CreateReceiverResponse]:
        return self._client.post(f"/instances/{self._instance_id}/receivers", data)

    def get(self, receiver_id: str) -> BlindpayApiResponse[Receiver]:
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


# --- Factory functions ---


def create_receivers_resource(instance_id: str, client: InternalApiClient) -> ReceiversResource:
    return ReceiversResource(instance_id, client)


def create_receivers_resource_sync(instance_id: str, client: InternalApiClientSync) -> ReceiversResourceSync:
    return ReceiversResourceSync(instance_id, client)
