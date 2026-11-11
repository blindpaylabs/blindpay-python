from typing import List, Literal, Optional, Union

from typing_extensions import NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, path_param
from ...types import (
    AccountClass,
    BankAccountType,
    BlindpayApiResponse,
    Country,
    Network,
    Rail,
    RecipientRelationship,
    SpeiProtocol,
)

ArgentinaTransfers = Literal["CVU", "CBU", "ALIAS"]
AchCopDocument = Literal["CC", "CE", "NIT", "PASS", "PEP"]
PixType = Literal["pix"]
TransfersBitsoType = Literal["transfers_bitso"]
SpeiBitsoType = Literal["spei_bitso"]
AchCopBitsoType = Literal["ach_cop_bitso"]
AchType = Literal["ach"]
WireType = Literal["wire"]
InternationalSwiftType = Literal["international_swift"]
RtpType = Literal["rtp"]
PixSafeType = Literal["pix_safe"]
TedType = Literal["ted"]


class OfframpWallet(TypedDict):
    address: str
    id: str
    network: Union[Network, str]
    external_id: Optional[str]
    partner_fee_id: NotRequired[Optional[str]]


class BankAccount(TypedDict):
    id: str
    type: Union[Rail, str]
    name: str
    pix_key: Optional[str]
    beneficiary_name: Optional[str]
    routing_number: Optional[str]
    account_number: Optional[str]
    account_type: Optional[Union[BankAccountType, str]]
    account_class: Optional[Union[AccountClass, str]]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Optional[Union[Country, str]]
    postal_code: Optional[str]
    spei_protocol: Optional[str]
    spei_institution_code: Optional[str]
    spei_clabe: Optional[str]
    sepa_beneficiary_bic: Optional[str]
    transfers_type: Optional[Union[ArgentinaTransfers, str]]
    transfers_account: Optional[str]
    ach_cop_beneficiary_first_name: Optional[str]
    ach_cop_beneficiary_last_name: Optional[str]
    ach_cop_document_id: Optional[str]
    ach_cop_document_type: Optional[Union[AchCopDocument, str]]
    ach_cop_email: Optional[str]
    ach_cop_bank_code: Optional[str]
    ach_cop_bank_account: Optional[str]
    swift_code_bic: Optional[str]
    swift_account_holder_name: Optional[str]
    swift_account_number_iban: Optional[str]
    swift_beneficiary_address_line_1: Optional[str]
    swift_beneficiary_address_line_2: Optional[str]
    swift_beneficiary_country: Optional[Union[Country, str]]
    swift_beneficiary_city: Optional[str]
    swift_beneficiary_state_province_region: Optional[str]
    swift_beneficiary_postal_code: Optional[str]
    swift_bank_name: Optional[str]
    swift_bank_address_line_1: Optional[str]
    swift_bank_address_line_2: Optional[str]
    swift_bank_country: Optional[Union[Country, str]]
    swift_bank_city: Optional[str]
    swift_bank_state_province_region: Optional[str]
    swift_bank_postal_code: Optional[str]
    swift_intermediary_bank_swift_code_bic: Optional[str]
    swift_intermediary_bank_account_number_iban: Optional[str]
    swift_intermediary_bank_name: Optional[str]
    swift_intermediary_bank_country: Optional[Union[Country, str]]
    tron_wallet_hash: Optional[str]
    offramp_wallets: Optional[List[OfframpWallet]]
    created_at: Optional[str]
    ted_bank_code: Optional[str]
    ted_branch_code: Optional[str]
    ted_cpf_cnpj: Optional[str]
    faster_payments_beneficiary_country: NotRequired[Optional[Union[Country, str]]]
    faster_payments_account_number: NotRequired[Optional[str]]
    faster_payments_beneficiary_address_line_1: NotRequired[Optional[str]]
    faster_payments_beneficiary_address_line_2: NotRequired[Optional[str]]
    faster_payments_beneficiary_city: NotRequired[Optional[str]]
    faster_payments_beneficiary_legal_name: NotRequired[Optional[str]]
    faster_payments_beneficiary_postal_code: NotRequired[Optional[str]]
    faster_payments_beneficiary_state_province_region: NotRequired[Optional[str]]
    faster_payments_sort_code: NotRequired[Optional[str]]
    plaid_connected_at: NotRequired[Optional[str]]
    swift_intermediary_bank_routing_number: NotRequired[Optional[str]]


ListBankAccountsResponse = List[BankAccount]


# GET .../bank-accounts/{id} returns the same BankAccountOut shape as list().
GetBankAccountResponse = BankAccount


class CreatePixInput(TypedDict):
    customer_id: str
    name: str
    pix_key: Optional[str]


class CreatePixResponse(TypedDict):
    id: str
    type: Union[PixType, str]
    name: str
    pix_key: str
    created_at: str


class CreateArgentinaTransfersInput(TypedDict):
    customer_id: str
    name: str
    beneficiary_name: Optional[str]
    transfers_account: Optional[str]
    transfers_type: Optional[ArgentinaTransfers]


class CreateArgentinaTransfersResponse(TypedDict):
    id: str
    type: Union[TransfersBitsoType, str]
    name: str
    beneficiary_name: str
    transfers_type: Union[ArgentinaTransfers, str]
    transfers_account: str
    created_at: str


class CreateSpeiInput(TypedDict):
    customer_id: str
    beneficiary_name: Optional[str]
    name: str
    spei_clabe: Optional[str]
    spei_institution_code: Optional[str]
    spei_protocol: Optional[SpeiProtocol]


class CreateSpeiResponse(TypedDict):
    id: str
    type: Union[SpeiBitsoType, str]
    name: str
    beneficiary_name: str
    spei_protocol: Union[SpeiProtocol, str]
    spei_institution_code: str
    spei_clabe: str
    created_at: str


class CreateColombiaAchInput(TypedDict):
    customer_id: str
    name: str
    account_type: Optional[BankAccountType]
    ach_cop_beneficiary_first_name: Optional[str]
    ach_cop_beneficiary_last_name: Optional[str]
    ach_cop_document_id: Optional[str]
    ach_cop_document_type: Optional[AchCopDocument]
    ach_cop_email: Optional[str]
    ach_cop_bank_code: Optional[str]
    ach_cop_bank_account: Optional[str]


class CreateColombiaAchResponse(TypedDict):
    id: str
    type: Union[AchCopBitsoType, str]
    name: str
    account_type: Union[BankAccountType, str]
    ach_cop_beneficiary_first_name: str
    ach_cop_beneficiary_last_name: str
    ach_cop_document_id: str
    ach_cop_document_type: Union[AchCopDocument, str]
    ach_cop_email: str
    ach_cop_bank_code: str
    ach_cop_bank_account: str
    created_at: str


class _CreateAchInputRequired(TypedDict):
    customer_id: str


class CreateAchInput(_CreateAchInputRequired, total=False):
    name: str
    account_class: Optional[AccountClass]
    account_number: Optional[str]
    account_type: Optional[BankAccountType]
    beneficiary_name: Optional[str]
    routing_number: Optional[str]
    recipient_relationship: Optional[RecipientRelationship]
    address_line_1: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Optional[Country]
    postal_code: Optional[str]
    address_line_2: Optional[str]
    business_industry: Optional[str]
    phone_number: Optional[str]
    tax_id: Optional[str]
    date_of_birth: Optional[str]


class CreateAchResponse(TypedDict):
    id: str
    type: Union[AchType, str]
    name: str
    beneficiary_name: str
    routing_number: str
    account_number: str
    account_type: Union[BankAccountType, str]
    account_class: Union[AccountClass, str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Optional[Union[Country, str]]
    postal_code: Optional[str]
    ach_cop_beneficiary_first_name: Optional[str]
    ach_cop_beneficiary_last_name: Optional[str]
    ach_cop_document_id: Optional[str]
    ach_cop_document_type: Optional[Union[AchCopDocument, str]]
    ach_cop_email: Optional[str]
    ach_cop_bank_code: Optional[str]
    ach_cop_bank_account: Optional[str]
    created_at: str


class _CreateWireInputRequired(TypedDict):
    customer_id: str


class CreateWireInput(_CreateWireInputRequired, total=False):
    name: str
    account_number: Optional[str]
    account_class: Optional[AccountClass]
    beneficiary_name: Optional[str]
    routing_number: Optional[str]
    recipient_relationship: Optional[RecipientRelationship]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Optional[Country]
    postal_code: Optional[str]
    business_industry: Optional[str]
    phone_number: Optional[str]
    tax_id: Optional[str]
    date_of_birth: Optional[str]


class CreateWireResponse(TypedDict):
    id: str
    type: Union[WireType, str]
    name: str
    beneficiary_name: str
    routing_number: str
    account_number: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Union[Country, str]
    postal_code: str
    created_at: str


class _CreateInternationalSwiftInputRequired(TypedDict):
    customer_id: str


class CreateInternationalSwiftInput(_CreateInternationalSwiftInputRequired, total=False):
    name: str
    account_class: Optional[AccountClass]
    recipient_relationship: Optional[RecipientRelationship]
    swift_account_holder_name: Optional[str]
    swift_account_number_iban: Optional[str]
    swift_bank_address_line_1: Optional[str]
    swift_bank_address_line_2: Optional[str]
    swift_bank_city: Optional[str]
    swift_bank_country: Optional[Country]
    swift_bank_name: Optional[str]
    swift_bank_postal_code: Optional[str]
    swift_bank_state_province_region: Optional[str]
    swift_beneficiary_address_line_1: Optional[str]
    swift_beneficiary_address_line_2: Optional[str]
    swift_beneficiary_city: Optional[str]
    swift_beneficiary_country: Optional[Country]
    swift_beneficiary_postal_code: Optional[str]
    swift_beneficiary_state_province_region: Optional[str]
    swift_code_bic: Optional[str]
    sepa_beneficiary_bic: Optional[str]
    swift_intermediary_bank_account_number_iban: Optional[str]
    swift_intermediary_bank_country: Optional[Country]
    swift_intermediary_bank_name: Optional[str]
    swift_intermediary_bank_swift_code_bic: Optional[str]
    swift_payment_code: Optional[str]
    business_industry: Optional[str]
    phone_number: Optional[str]
    tax_id: Optional[str]
    date_of_birth: Optional[str]
    swift_intermediary_bank_routing_number: Optional[str]


class CreateInternationalSwiftResponse(TypedDict):
    id: str
    type: Union[InternationalSwiftType, str]
    name: str
    beneficiary_name: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Optional[Union[Country, str]]
    postal_code: Optional[str]
    swift_code_bic: str
    swift_account_holder_name: str
    swift_account_number_iban: str
    swift_beneficiary_address_line_1: str
    swift_beneficiary_address_line_2: Optional[str]
    swift_beneficiary_country: Union[Country, str]
    swift_beneficiary_city: str
    swift_beneficiary_state_province_region: str
    swift_beneficiary_postal_code: str
    swift_bank_name: str
    swift_bank_address_line_1: str
    swift_bank_address_line_2: Optional[str]
    swift_bank_country: Union[Country, str]
    swift_bank_city: str
    swift_bank_state_province_region: str
    swift_bank_postal_code: str
    sepa_beneficiary_bic: Optional[str]
    swift_intermediary_bank_swift_code_bic: Optional[str]
    swift_intermediary_bank_account_number_iban: Optional[str]
    swift_intermediary_bank_name: Optional[str]
    swift_intermediary_bank_country: Optional[Union[Country, str]]
    created_at: str


class _CreateRtpInputRequired(TypedDict):
    customer_id: str


class CreateRtpInput(_CreateRtpInputRequired, total=False):
    name: str
    account_class: Optional[AccountClass]
    beneficiary_name: Optional[str]
    routing_number: Optional[str]
    account_number: Optional[str]
    recipient_relationship: Optional[RecipientRelationship]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Optional[Country]
    postal_code: Optional[str]
    business_industry: Optional[str]
    phone_number: Optional[str]
    tax_id: Optional[str]
    date_of_birth: Optional[str]


class CreateRtpResponse(TypedDict):
    id: str
    type: Union[RtpType, str]
    name: str
    beneficiary_name: str
    routing_number: str
    account_number: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Union[Country, str]
    postal_code: str
    created_at: str


class _CreateSepaInputRequired(TypedDict):
    customer_id: str
    name: str
    account_class: Optional[AccountClass]
    sepa_iban: Optional[str]
    sepa_beneficiary_bic: Optional[str]
    sepa_beneficiary_legal_name: Optional[str]
    sepa_beneficiary_address_line_1: Optional[str]
    sepa_beneficiary_city: Optional[str]
    sepa_beneficiary_postal_code: Optional[str]
    sepa_beneficiary_country: Optional[Country]


class CreateSepaInput(_CreateSepaInputRequired, total=False):
    sepa_beneficiary_address_line_2: Optional[str]
    sepa_beneficiary_state_province_region: Optional[str]


class CreateSepaResponse(TypedDict):
    id: str
    type: Union[Literal["sepa"], str]
    name: str
    account_class: Union[AccountClass, str]
    recipient_relationship: Optional[Union[RecipientRelationship, str]]
    sepa_iban: str
    sepa_beneficiary_bic: str
    sepa_beneficiary_legal_name: str
    sepa_beneficiary_address_line_1: str
    sepa_beneficiary_address_line_2: Optional[str]
    sepa_beneficiary_city: str
    sepa_beneficiary_state_province_region: Optional[str]
    sepa_beneficiary_postal_code: str
    sepa_beneficiary_country: Union[Country, str]
    created_at: str


class CreateFasterPaymentsInput(TypedDict):
    """A UK bank account paid over Faster Payments (GBP)."""

    customer_id: str
    name: str
    faster_payments_sort_code: str
    faster_payments_account_number: str
    faster_payments_beneficiary_legal_name: str
    faster_payments_beneficiary_address_line_1: NotRequired[Optional[str]]
    faster_payments_beneficiary_address_line_2: NotRequired[Optional[str]]
    faster_payments_beneficiary_city: NotRequired[Optional[str]]
    faster_payments_beneficiary_state_province_region: NotRequired[Optional[str]]
    faster_payments_beneficiary_postal_code: NotRequired[Optional[str]]
    faster_payments_beneficiary_country: NotRequired[Optional[Country]]
    recipient_relationship: NotRequired[Optional[RecipientRelationship]]


class CreatePixSafeInput(TypedDict):
    customer_id: str
    name: str
    account_number: Optional[str]
    account_type: Optional[BankAccountType]
    pix_safe_bank_code: Optional[str]
    pix_safe_branch_code: Optional[str]
    pix_safe_cpf_cnpj: Optional[str]


class CreatePixSafeResponse(TypedDict):
    id: str
    type: Union[PixSafeType, str]
    name: str
    account_number: str
    account_type: Union[BankAccountType, str]
    pix_safe_bank_code: str
    pix_safe_branch_code: str
    pix_safe_cpf_cnpj: str
    created_at: str


class CreateTedInput(TypedDict):
    customer_id: str
    name: str
    account_number: Optional[str]
    account_type: Optional[BankAccountType]
    ted_bank_code: Optional[str]
    ted_branch_code: Optional[str]
    ted_cpf_cnpj: Optional[str]


class CreateTedResponse(TypedDict):
    id: str
    type: Union[TedType, str]
    name: str
    account_number: str
    account_type: Union[BankAccountType, str]
    ted_bank_code: str
    ted_branch_code: str
    ted_cpf_cnpj: str
    created_at: str


class CreatePlaidLinkInput(TypedDict):
    customer_id: str
    redirect_url: NotRequired[Optional[str]]


class PlaidLink(TypedDict):
    url: str


class BankAccountsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, customer_id: str) -> BlindpayApiResponse[ListBankAccountsResponse]:
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts"
        )

    async def get(self, customer_id: str, id: str) -> BlindpayApiResponse[GetBankAccountResponse]:
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts/{path_param(id)}"
        )

    async def delete(
        self, customer_id: str, id: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        return await self._client.delete(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts/{path_param(id)}",
            options=options,
        )

    async def create_pix(
        self, data: CreatePixInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreatePixResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "pix"
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    async def create_argentina_transfers(
        self, data: CreateArgentinaTransfersInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateArgentinaTransfersResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "transfers_bitso"
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    async def create_spei(
        self, data: CreateSpeiInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateSpeiResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "spei_bitso"
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    async def create_colombia_ach(
        self, data: CreateColombiaAchInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateColombiaAchResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "ach_cop_bitso"
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    async def create_ach(
        self, data: CreateAchInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateAchResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "ach"
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    async def create_wire(
        self, data: CreateWireInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateWireResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "wire"
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    async def create_international_swift(
        self, data: CreateInternationalSwiftInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateInternationalSwiftResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "international_swift"
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    async def create_rtp(
        self, data: CreateRtpInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateRtpResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "rtp"
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    async def create_pix_safe(
        self, data: CreatePixSafeInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreatePixSafeResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "pix_safe"
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    async def create_ted(
        self, data: CreateTedInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateTedResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "ted"
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    async def create_sepa(
        self, data: CreateSepaInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateSepaResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "sepa"
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    async def create_plaid_link(
        self, data: CreatePlaidLinkInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[PlaidLink]:
        """Starts a Plaid Link session for the customer to connect a US bank account; send them to ``url``."""
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts/plaid",
            payload,
            options=options,
        )

    async def create_faster_payments(
        self, data: CreateFasterPaymentsInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[BankAccount]:
        customer_id = data["customer_id"]
        payload = {"type": "faster_payments", **{k: v for k, v in data.items() if k != "customer_id"}}
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )


class BankAccountsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, customer_id: str) -> BlindpayApiResponse[ListBankAccountsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts")

    def get(self, customer_id: str, id: str) -> BlindpayApiResponse[GetBankAccountResponse]:
        return self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts/{path_param(id)}"
        )

    def delete(self, customer_id: str, id: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
        return self._client.delete(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts/{path_param(id)}",
            options=options,
        )

    def create_pix(
        self, data: CreatePixInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreatePixResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "pix"
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    def create_argentina_transfers(
        self, data: CreateArgentinaTransfersInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateArgentinaTransfersResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "transfers_bitso"
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    def create_spei(
        self, data: CreateSpeiInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateSpeiResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "spei_bitso"
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    def create_colombia_ach(
        self, data: CreateColombiaAchInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateColombiaAchResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "ach_cop_bitso"
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    def create_ach(
        self, data: CreateAchInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateAchResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "ach"
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    def create_wire(
        self, data: CreateWireInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateWireResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "wire"
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    def create_international_swift(
        self, data: CreateInternationalSwiftInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateInternationalSwiftResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "international_swift"
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    def create_rtp(
        self, data: CreateRtpInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateRtpResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "rtp"
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    def create_pix_safe(
        self, data: CreatePixSafeInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreatePixSafeResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "pix_safe"
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    def create_ted(
        self, data: CreateTedInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateTedResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "ted"
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    def create_sepa(
        self, data: CreateSepaInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateSepaResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["type"] = "sepa"
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )

    def create_plaid_link(
        self, data: CreatePlaidLinkInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[PlaidLink]:
        """Starts a Plaid Link session for the customer to connect a US bank account; send them to ``url``."""
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts/plaid",
            payload,
            options=options,
        )

    def create_faster_payments(
        self, data: CreateFasterPaymentsInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[BankAccount]:
        customer_id = data["customer_id"]
        payload = {"type": "faster_payments", **{k: v for k, v in data.items() if k != "customer_id"}}
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts",
            payload,
            options=options,
        )


def create_bank_accounts_resource(instance_id: str, client: InternalApiClient) -> BankAccountsResource:
    return BankAccountsResource(instance_id, client)


def create_bank_accounts_resource_sync(instance_id: str, client: InternalApiClientSync) -> BankAccountsResourceSync:
    return BankAccountsResourceSync(instance_id, client)
