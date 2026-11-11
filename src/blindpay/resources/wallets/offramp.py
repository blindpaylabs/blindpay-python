from typing import List, Optional, Union

from typing_extensions import NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, path_param
from ...types import BlindpayApiResponse, Network


class OfframpWallet(TypedDict):
    id: str
    external_id: NotRequired[Optional[str]]
    instance_id: str
    customer_id: str
    bank_account_id: str
    network: Union[Network, str]
    address: str
    created_at: NotRequired[Optional[str]]
    updated_at: NotRequired[Optional[str]]
    partner_fee_id: NotRequired[Optional[str]]


ListOfframpWalletsResponse = List[OfframpWallet]
GetOfframpWalletResponse = OfframpWallet


class ListOfframpWalletsInput(TypedDict):
    customer_id: str
    bank_account_id: str


class CreateOfframpWalletInput(TypedDict):
    customer_id: str
    bank_account_id: str
    external_id: str
    network: Network


class CreateOfframpWalletResponse(TypedDict):
    id: str
    external_id: NotRequired[Optional[str]]
    network: Union[Network, str]
    address: str


class GetOfframpWalletInput(TypedDict):
    customer_id: str
    bank_account_id: str
    id: str


class UpdateOfframpWalletInput(TypedDict):
    customer_id: str
    bank_account_id: str
    id: str
    partner_fee_id: NotRequired[Optional[str]]
    """A partner fee id to apply, or ``None`` to remove the current one. Omit it to leave the fee unchanged."""


class UpdateOfframpWalletResponse(TypedDict):
    success: bool


class OfframpWalletsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, data: ListOfframpWalletsInput) -> BlindpayApiResponse[ListOfframpWalletsResponse]:
        customer_id = data["customer_id"]
        bank_account_id = data["bank_account_id"]
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts/{path_param(bank_account_id)}/offramp-wallets"
        )

    async def create(
        self, data: CreateOfframpWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateOfframpWalletResponse]:
        customer_id = data["customer_id"]
        bank_account_id = data["bank_account_id"]
        payload = {k: v for k, v in data.items() if k not in ["customer_id", "bank_account_id"]}
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts/{path_param(bank_account_id)}/offramp-wallets",
            payload,
            options=options,
        )

    async def get(self, data: GetOfframpWalletInput) -> BlindpayApiResponse[GetOfframpWalletResponse]:
        customer_id = data["customer_id"]
        bank_account_id = data["bank_account_id"]
        id = data["id"]
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts/{path_param(bank_account_id)}/offramp-wallets/{path_param(id)}"
        )

    async def update(
        self, data: UpdateOfframpWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[UpdateOfframpWalletResponse]:
        payload = {k: v for k, v in data.items() if k not in ("customer_id", "bank_account_id", "id")}
        return await self._client.put(
            f"/instances/{self._instance_id}/customers/{path_param(data['customer_id'])}"
            f"/bank-accounts/{path_param(data['bank_account_id'])}/offramp-wallets/{path_param(data['id'])}",
            payload,
            options=options,
        )


class OfframpWalletsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, data: ListOfframpWalletsInput) -> BlindpayApiResponse[ListOfframpWalletsResponse]:
        customer_id = data["customer_id"]
        bank_account_id = data["bank_account_id"]
        return self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts/{path_param(bank_account_id)}/offramp-wallets"
        )

    def create(
        self, data: CreateOfframpWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateOfframpWalletResponse]:
        customer_id = data["customer_id"]
        bank_account_id = data["bank_account_id"]
        payload = {k: v for k, v in data.items() if k not in ["customer_id", "bank_account_id"]}
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts/{path_param(bank_account_id)}/offramp-wallets",
            payload,
            options=options,
        )

    def get(self, data: GetOfframpWalletInput) -> BlindpayApiResponse[GetOfframpWalletResponse]:
        customer_id = data["customer_id"]
        bank_account_id = data["bank_account_id"]
        id = data["id"]
        return self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/bank-accounts/{path_param(bank_account_id)}/offramp-wallets/{path_param(id)}"
        )

    def update(
        self, data: UpdateOfframpWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[UpdateOfframpWalletResponse]:
        payload = {k: v for k, v in data.items() if k not in ("customer_id", "bank_account_id", "id")}
        return self._client.put(
            f"/instances/{self._instance_id}/customers/{path_param(data['customer_id'])}"
            f"/bank-accounts/{path_param(data['bank_account_id'])}/offramp-wallets/{path_param(data['id'])}",
            payload,
            options=options,
        )


def create_offramp_wallets_resource(instance_id: str, client: InternalApiClient) -> OfframpWalletsResource:
    return OfframpWalletsResource(instance_id, client)


def create_offramp_wallets_resource_sync(instance_id: str, client: InternalApiClientSync) -> OfframpWalletsResourceSync:
    return OfframpWalletsResourceSync(instance_id, client)
