from typing import List, Optional, Union

from typing_extensions import Literal, NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, path_param
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


class VirtualAccountBeneficiary(TypedDict):
    name: str


class VirtualAccountBreBKey(TypedDict):
    key: str


class VirtualAccountCo(TypedDict):
    """Colombian (Bre-B) receiving details."""

    bre_b: VirtualAccountBreBKey
    beneficiary: NotRequired[Optional[VirtualAccountBeneficiary]]


class VirtualAccountSpei(TypedDict):
    clabe: str


class VirtualAccountMx(TypedDict):
    """Mexican (SPEI) receiving details."""

    spei: VirtualAccountSpei
    beneficiary: NotRequired[Optional[VirtualAccountBeneficiary]]


class CreateVirtualAccountBreB(TypedDict):
    gender: Literal["male", "female"]


class VirtualAccount(TypedDict):
    id: str
    us: USBankDetails
    token: Union[StablecoinToken, str]
    blockchain_wallet_id: Optional[str]
    banking_partner: Optional[Union[BankingPartner, str]]
    kyc_status: Optional[str]
    blockchain_wallet: Optional[str]
    co: NotRequired[Optional[VirtualAccountCo]]
    mx: NotRequired[Optional[VirtualAccountMx]]
    partner_fee_id: NotRequired[Optional[str]]


class _CreateVirtualAccountInputRequired(TypedDict):
    customer_id: str


class CreateVirtualAccountInput(_CreateVirtualAccountInputRequired, total=False):
    blockchain_wallet_id: str
    token: StablecoinToken
    banking_partner: BankingPartner
    sole_proprietor_doc_type: Optional[str]
    sole_proprietor_doc_file: Optional[str]
    bre_b: Optional[CreateVirtualAccountBreB]
    partner_fee_id: Optional[str]


CreateVirtualAccountResponse = VirtualAccount
GetVirtualAccountResponse = VirtualAccount


class UpdateVirtualAccountInput(TypedDict):
    blockchain_wallet_id: str
    token: StablecoinToken
    partner_fee_id: NotRequired[Optional[str]]


class ListVirtualAccountsResponse(TypedDict):
    data: List[VirtualAccount]


class VirtualAccountsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, customer_id: str) -> BlindpayApiResponse[ListVirtualAccountsResponse]:
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/virtual-accounts"
        )

    async def update(
        self,
        customer_id: str,
        virtual_account_id: str,
        data: UpdateVirtualAccountInput,
        options: Optional[RequestOptions] = None,
    ) -> BlindpayApiResponse[None]:
        return await self._client.put(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/virtual-accounts/{path_param(virtual_account_id)}",
            data,
            options=options,
        )

    async def create(
        self, data: CreateVirtualAccountInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateVirtualAccountResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/virtual-accounts",
            payload,
            options=options,
        )

    async def get(self, customer_id: str, virtual_account_id: str) -> BlindpayApiResponse[GetVirtualAccountResponse]:
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/virtual-accounts/{path_param(virtual_account_id)}"
        )


class VirtualAccountsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, customer_id: str) -> BlindpayApiResponse[ListVirtualAccountsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/virtual-accounts")

    def update(
        self,
        customer_id: str,
        virtual_account_id: str,
        data: UpdateVirtualAccountInput,
        options: Optional[RequestOptions] = None,
    ) -> BlindpayApiResponse[None]:
        return self._client.put(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/virtual-accounts/{path_param(virtual_account_id)}",
            data,
            options=options,
        )

    def create(
        self, data: CreateVirtualAccountInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateVirtualAccountResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/virtual-accounts",
            payload,
            options=options,
        )

    def get(self, customer_id: str, virtual_account_id: str) -> BlindpayApiResponse[GetVirtualAccountResponse]:
        return self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/virtual-accounts/{path_param(virtual_account_id)}"
        )


def create_virtual_accounts_resource(instance_id: str, client: InternalApiClient) -> VirtualAccountsResource:
    return VirtualAccountsResource(instance_id, client)


def create_virtual_accounts_resource_sync(
    instance_id: str, client: InternalApiClientSync
) -> VirtualAccountsResourceSync:
    return VirtualAccountsResourceSync(instance_id, client)
