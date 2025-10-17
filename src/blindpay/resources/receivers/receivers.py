from typing import List, Optional, Union

from typing_extensions import Literal, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import (
    BlindpayApiResponse,
    Country,
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


class CreateBusinessWithStandardKYBResponse(TypedDict):
    id: str


ListReceiversResponse = List[Union[IndividualWithStandardKYC, IndividualWithEnhancedKYC, BusinessWithStandardKYB]]

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

    async def list(self) -> BlindpayApiResponse[ListReceiversResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/receivers")

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
        return await self._client.patch(f"/instances/{self._instance_id}/receivers/{receiver_id}", payload)

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

    def list(self) -> BlindpayApiResponse[ListReceiversResponse]:
        return self._client.get(f"/instances/{self._instance_id}/receivers")

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
        return self._client.patch(f"/instances/{self._instance_id}/receivers/{receiver_id}", payload)

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
