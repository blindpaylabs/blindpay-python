from typing import List, Literal, Optional

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import AccountClass, BankAccountType, BlindpayApiResponse, Country, Rail, SpeiProtocol

ArgentinaTransfers = Literal["CVU", "CBU", "ALIAS"]
AchCopDocument = Literal["CC", "CE", "NIT", "PASS", "PEP"]
OfframpNetwork = Literal["tron"]
PixType = Literal["pix"]
TransfersBitsoType = Literal["transfers_bitso"]
SpeiBitsoType = Literal["spei_bitso"]
AchCopBitsoType = Literal["ach_cop_bitso"]
AchType = Literal["ach"]
WireType = Literal["wire"]
InternationalSwiftType = Literal["international_swift"]
RtpType = Literal["rtp"]


class OfframpWallet(TypedDict):
    address: str
    id: str
    network: OfframpNetwork
    external_id: str


class BankAccount(TypedDict):
    id: str
    type: Rail
    name: str
    pix_key: Optional[str]
    beneficiary_name: Optional[str]
    routing_number: Optional[str]
    account_number: Optional[str]
    account_type: Optional[BankAccountType]
    account_class: Optional[AccountClass]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Optional[Country]
    postal_code: Optional[str]
    spei_protocol: Optional[str]
    spei_institution_code: Optional[str]
    spei_clabe: Optional[str]
    transfers_type: Optional[ArgentinaTransfers]
    transfers_account: Optional[str]
    ach_cop_beneficiary_first_name: Optional[str]
    ach_cop_beneficiary_last_name: Optional[str]
    ach_cop_document_id: Optional[str]
    ach_cop_document_type: Optional[AchCopDocument]
    ach_cop_email: Optional[str]
    ach_cop_bank_code: Optional[str]
    ach_cop_bank_account: Optional[str]
    swift_code_bic: Optional[str]
    swift_account_holder_name: Optional[str]
    swift_account_number_iban: Optional[str]
    swift_beneficiary_address_line_1: Optional[str]
    swift_beneficiary_address_line_2: Optional[str]
    swift_beneficiary_country: Optional[Country]
    swift_beneficiary_city: Optional[str]
    swift_beneficiary_state_province_region: Optional[str]
    swift_beneficiary_postal_code: Optional[str]
    swift_bank_name: Optional[str]
    swift_bank_address_line_1: Optional[str]
    swift_bank_address_line_2: Optional[str]
    swift_bank_country: Optional[Country]
    swift_bank_city: Optional[str]
    swift_bank_state_province_region: Optional[str]
    swift_bank_postal_code: Optional[str]
    swift_intermediary_bank_swift_code_bic: Optional[str]
    swift_intermediary_bank_account_number_iban: Optional[str]
    swift_intermediary_bank_name: Optional[str]
    swift_intermediary_bank_country: Optional[Country]
    tron_wallet_hash: Optional[str]
    offramp_wallets: Optional[List[OfframpWallet]]
    created_at: str


class ListBankAccountsResponse(TypedDict):
    data: List[BankAccount]


class GetBankAccountResponse(TypedDict):
    id: str
    receiver_id: str
    account_holder_name: str
    account_number: str
    routing_number: str
    account_type: BankAccountType
    bank_name: str
    swift_code: Optional[str]
    iban: Optional[str]
    is_primary: bool
    created_at: str
    updated_at: str


class CreatePixInput(TypedDict):
    receiver_id: str
    name: str
    pix_key: str


class CreatePixResponse(TypedDict):
    id: str
    type: PixType
    name: str
    pix_key: str
    created_at: str


class CreateArgentinaTransfersInput(TypedDict):
    receiver_id: str
    name: str
    beneficiary_name: str
    transfers_account: str
    transfers_type: ArgentinaTransfers


class CreateArgentinaTransfersResponse(TypedDict):
    id: str
    type: TransfersBitsoType
    name: str
    beneficiary_name: str
    transfers_type: ArgentinaTransfers
    transfers_account: str
    created_at: str


class CreateSpeiInput(TypedDict):
    receiver_id: str
    beneficiary_name: str
    name: str
    spei_clabe: str
    spei_institution_code: str
    spei_protocol: SpeiProtocol


class CreateSpeiResponse(TypedDict):
    id: str
    type: SpeiBitsoType
    name: str
    beneficiary_name: str
    spei_protocol: SpeiProtocol
    spei_institution_code: str
    spei_clabe: str
    created_at: str


class CreateColombiaAchInput(TypedDict):
    receiver_id: str
    name: str
    account_type: BankAccountType
    ach_cop_beneficiary_first_name: str
    ach_cop_beneficiary_last_name: str
    ach_cop_document_id: str
    ach_cop_document_type: AchCopDocument
    ach_cop_email: str
    ach_cop_bank_code: str
    ach_cop_bank_account: str


class CreateColombiaAchResponse(TypedDict):
    id: str
    type: AchCopBitsoType
    name: str
    account_type: BankAccountType
    ach_cop_beneficiary_first_name: str
    ach_cop_beneficiary_last_name: str
    ach_cop_document_id: str
    ach_cop_document_type: AchCopDocument
    ach_cop_email: str
    ach_cop_bank_code: str
    ach_cop_bank_account: str
    created_at: str


class CreateAchInput(TypedDict):
    receiver_id: str
    name: str
    account_class: AccountClass
    account_number: str
    account_type: BankAccountType
    beneficiary_name: str
    routing_number: str


class CreateAchResponse(TypedDict):
    id: str
    type: AchType
    name: str
    beneficiary_name: str
    routing_number: str
    account_number: str
    account_type: BankAccountType
    account_class: AccountClass
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Optional[Country]
    postal_code: Optional[str]
    ach_cop_beneficiary_first_name: Optional[str]
    ach_cop_beneficiary_last_name: Optional[str]
    ach_cop_document_id: Optional[str]
    ach_cop_document_type: Optional[AchCopDocument]
    ach_cop_email: Optional[str]
    ach_cop_bank_code: Optional[str]
    ach_cop_bank_account: Optional[str]
    created_at: str


class CreateWireInput(TypedDict):
    receiver_id: str
    name: str
    account_number: str
    beneficiary_name: str
    routing_number: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Country
    postal_code: str


class CreateWireResponse(TypedDict):
    id: str
    type: WireType
    name: str
    beneficiary_name: str
    routing_number: str
    account_number: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Country
    postal_code: str
    created_at: str


class CreateInternationalSwiftInput(TypedDict):
    receiver_id: str
    name: str
    swift_account_holder_name: str
    swift_account_number_iban: str
    swift_bank_address_line_1: str
    swift_bank_address_line_2: Optional[str]
    swift_bank_city: str
    swift_bank_country: Country
    swift_bank_name: str
    swift_bank_postal_code: str
    swift_bank_state_province_region: str
    swift_beneficiary_address_line_1: str
    swift_beneficiary_address_line_2: Optional[str]
    swift_beneficiary_city: str
    swift_beneficiary_country: Country
    swift_beneficiary_postal_code: str
    swift_beneficiary_state_province_region: str
    swift_code_bic: str
    swift_intermediary_bank_account_number_iban: Optional[str]
    swift_intermediary_bank_country: Optional[Country]
    swift_intermediary_bank_name: Optional[str]
    swift_intermediary_bank_swift_code_bic: Optional[str]


class CreateInternationalSwiftResponse(TypedDict):
    id: str
    type: InternationalSwiftType
    name: str
    beneficiary_name: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Optional[Country]
    postal_code: Optional[str]
    swift_code_bic: str
    swift_account_holder_name: str
    swift_account_number_iban: str
    swift_beneficiary_address_line_1: str
    swift_beneficiary_address_line_2: Optional[str]
    swift_beneficiary_country: Country
    swift_beneficiary_city: str
    swift_beneficiary_state_province_region: str
    swift_beneficiary_postal_code: str
    swift_bank_name: str
    swift_bank_address_line_1: str
    swift_bank_address_line_2: Optional[str]
    swift_bank_country: Country
    swift_bank_city: str
    swift_bank_state_province_region: str
    swift_bank_postal_code: str
    swift_intermediary_bank_swift_code_bic: Optional[str]
    swift_intermediary_bank_account_number_iban: Optional[str]
    swift_intermediary_bank_name: Optional[str]
    swift_intermediary_bank_country: Optional[Country]
    created_at: str


class CreateRtpInput(TypedDict):
    receiver_id: str
    name: str
    beneficiary_name: str
    routing_number: str
    account_number: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Country
    postal_code: str


class CreateRtpResponse(TypedDict):
    id: str
    type: RtpType
    name: str
    beneficiary_name: str
    routing_number: str
    account_number: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Country
    postal_code: str
    created_at: str


class BankAccountsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, receiver_id: str) -> BlindpayApiResponse[ListBankAccountsResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts")

    async def get(self, receiver_id: str, id: str) -> BlindpayApiResponse[GetBankAccountResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts/{id}")

    async def delete(self, receiver_id: str, id: str) -> BlindpayApiResponse[None]:
        return await self._client.delete(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts/{id}")

    async def create_pix(self, data: CreatePixInput) -> BlindpayApiResponse[CreatePixResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "pix"
        return await self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    async def create_argentina_transfers(
        self, data: CreateArgentinaTransfersInput
    ) -> BlindpayApiResponse[CreateArgentinaTransfersResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "transfers_bitso"
        return await self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    async def create_spei(self, data: CreateSpeiInput) -> BlindpayApiResponse[CreateSpeiResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "spei_bitso"
        return await self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    async def create_colombia_ach(self, data: CreateColombiaAchInput) -> BlindpayApiResponse[CreateColombiaAchResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "ach_cop_bitso"
        return await self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    async def create_ach(self, data: CreateAchInput) -> BlindpayApiResponse[CreateAchResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "ach"
        return await self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    async def create_wire(self, data: CreateWireInput) -> BlindpayApiResponse[CreateWireResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "wire"
        return await self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    async def create_international_swift(
        self, data: CreateInternationalSwiftInput
    ) -> BlindpayApiResponse[CreateInternationalSwiftResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "international_swift"
        return await self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    async def create_rtp(self, data: CreateRtpInput) -> BlindpayApiResponse[CreateRtpResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "rtp"
        return await self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)


class BankAccountsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, receiver_id: str) -> BlindpayApiResponse[ListBankAccountsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts")

    def get(self, receiver_id: str, id: str) -> BlindpayApiResponse[GetBankAccountResponse]:
        return self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts/{id}")

    def delete(self, receiver_id: str, id: str) -> BlindpayApiResponse[None]:
        return self._client.delete(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts/{id}")

    def create_pix(self, data: CreatePixInput) -> BlindpayApiResponse[CreatePixResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "pix"
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    def create_argentina_transfers(
        self, data: CreateArgentinaTransfersInput
    ) -> BlindpayApiResponse[CreateArgentinaTransfersResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "transfers_bitso"
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    def create_spei(self, data: CreateSpeiInput) -> BlindpayApiResponse[CreateSpeiResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "spei_bitso"
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    def create_colombia_ach(self, data: CreateColombiaAchInput) -> BlindpayApiResponse[CreateColombiaAchResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "ach_cop_bitso"
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    def create_ach(self, data: CreateAchInput) -> BlindpayApiResponse[CreateAchResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "ach"
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    def create_wire(self, data: CreateWireInput) -> BlindpayApiResponse[CreateWireResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "wire"
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    def create_international_swift(
        self, data: CreateInternationalSwiftInput
    ) -> BlindpayApiResponse[CreateInternationalSwiftResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "international_swift"
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)

    def create_rtp(self, data: CreateRtpInput) -> BlindpayApiResponse[CreateRtpResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["type"] = "rtp"
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts", payload)


def create_bank_accounts_resource(instance_id: str, client: InternalApiClient) -> BankAccountsResource:
    return BankAccountsResource(instance_id, client)


def create_bank_accounts_resource_sync(instance_id: str, client: InternalApiClientSync) -> BankAccountsResourceSync:
    return BankAccountsResourceSync(instance_id, client)
