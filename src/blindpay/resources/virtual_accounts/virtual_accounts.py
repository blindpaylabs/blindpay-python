from typing_extensions import Optional, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse, StablecoinToken


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


class CreateVirtualAccountInput(TypedDict):
    receiver_id: str
    blockchain_wallet_id: str
    token: StablecoinToken


CreateVirtualAccountResponse = VirtualAccount
GetVirtualAccountResponse = VirtualAccount


class UpdateVirtualAccountInput(TypedDict):
    receiver_id: str
    blockchain_wallet_id: str
    token: StablecoinToken


class VirtualAccountsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def update(self, data: UpdateVirtualAccountInput) -> BlindpayApiResponse[None]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        return await self._client.put(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts", payload
        )

    async def create(self, data: CreateVirtualAccountInput) -> BlindpayApiResponse[CreateVirtualAccountResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        return await self._client.post(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts", payload
        )

    async def get(self, receiver_id: str) -> BlindpayApiResponse[GetVirtualAccountResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts")


class VirtualAccountsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def update(self, data: UpdateVirtualAccountInput) -> BlindpayApiResponse[None]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        return self._client.put(f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts", payload)

    def create(self, data: CreateVirtualAccountInput) -> BlindpayApiResponse[CreateVirtualAccountResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts", payload)

    def get(self, receiver_id: str) -> BlindpayApiResponse[GetVirtualAccountResponse]:
        return self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/virtual-accounts")


def create_virtual_accounts_resource(instance_id: str, client: InternalApiClient) -> VirtualAccountsResource:
    return VirtualAccountsResource(instance_id, client)


def create_virtual_accounts_resource_sync(
    instance_id: str, client: InternalApiClientSync
) -> VirtualAccountsResourceSync:
    return VirtualAccountsResourceSync(instance_id, client)
