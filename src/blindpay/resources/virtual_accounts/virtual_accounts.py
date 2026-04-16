from typing import List, Optional

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BankingPartner, BlindpayApiResponse, StablecoinToken


class BankAccountInfo(TypedDict):
    routing_number: str
    account_number: str


class BeneficiaryInfo(TypedDict):
    name: str
    address_line_1: str
    address_line_2: Optional[str]


class ReceivingBankInfo(TypedDict):
    name: str
    address_line_1: str
    address_line_2: Optional[str]


class USBankDetails(TypedDict):
    ach: BankAccountInfo
    wire: BankAccountInfo
    rtp: BankAccountInfo
    swift_bic_code: str
    account_type: str
    beneficiary: BeneficiaryInfo
    receiving_bank: ReceivingBankInfo


class VirtualAccount(TypedDict):
    id: str
    us: USBankDetails
    token: StablecoinToken
    blockchain_wallet_id: str
    banking_partner: Optional[BankingPartner]
    kyc_status: Optional[str]
    blockchain_wallet: Optional[str]


class CreateVirtualAccountInput(TypedDict, total=False):
    receiver_id: str
    blockchain_wallet_id: str
    token: StablecoinToken
    banking_partner: BankingPartner
    sole_proprietor_doc_type: str
    sole_proprietor_doc_file: str


CreateVirtualAccountResponse = VirtualAccount
GetVirtualAccountResponse = VirtualAccount


class UpdateVirtualAccountInput(TypedDict):
    receiver_id: str
    virtual_account_id: str
    blockchain_wallet_id: str
    token: StablecoinToken


class ListVirtualAccountsResponse(TypedDict):
    data: List[VirtualAccount]


class VirtualAccountsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, receiver_id: str) -> BlindpayApiResponse[ListVirtualAccountsResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts")

    async def update(self, data: UpdateVirtualAccountInput) -> BlindpayApiResponse[None]:
        receiver_id = data["receiver_id"]
        virtual_account_id = data["virtual_account_id"]
        payload = {k: v for k, v in data.items() if k not in ["receiver_id", "virtual_account_id"]}
        return await self._client.put(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts/{virtual_account_id}", payload
        )

    async def create(self, data: CreateVirtualAccountInput) -> BlindpayApiResponse[CreateVirtualAccountResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        return await self._client.post(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts", payload
        )

    async def get(self, receiver_id: str, virtual_account_id: str) -> BlindpayApiResponse[GetVirtualAccountResponse]:
        return await self._client.get(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts/{virtual_account_id}"
        )


class VirtualAccountsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, receiver_id: str) -> BlindpayApiResponse[ListVirtualAccountsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts")

    def update(self, data: UpdateVirtualAccountInput) -> BlindpayApiResponse[None]:
        receiver_id = data["receiver_id"]
        virtual_account_id = data["virtual_account_id"]
        payload = {k: v for k, v in data.items() if k not in ["receiver_id", "virtual_account_id"]}
        return self._client.put(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts/{virtual_account_id}", payload
        )

    def create(self, data: CreateVirtualAccountInput) -> BlindpayApiResponse[CreateVirtualAccountResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts", payload)

    def get(self, receiver_id: str, virtual_account_id: str) -> BlindpayApiResponse[GetVirtualAccountResponse]:
        return self._client.get(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts/{virtual_account_id}"
        )


def create_virtual_accounts_resource(instance_id: str, client: InternalApiClient) -> VirtualAccountsResource:
    return VirtualAccountsResource(instance_id, client)


def create_virtual_accounts_resource_sync(
    instance_id: str, client: InternalApiClientSync
) -> VirtualAccountsResourceSync:
    return VirtualAccountsResourceSync(instance_id, client)
