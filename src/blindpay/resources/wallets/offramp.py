from typing import List

from typing_extensions import Literal, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse

TronNetwork = Literal["tron"]


class OfframpWallet(TypedDict):
    id: str
    external_id: str
    instance_id: str
    receiver_id: str
    bank_account_id: str
    network: TronNetwork
    address: str
    created_at: str
    updated_at: str


ListOfframpWalletsResponse = List[OfframpWallet]
GetOfframpWalletResponse = OfframpWallet


class ListOfframpWalletsInput(TypedDict):
    receiver_id: str
    bank_account_id: str


class CreateOfframpWalletInput(TypedDict):
    receiver_id: str
    bank_account_id: str
    external_id: str
    network: TronNetwork


class CreateOfframpWalletResponse(TypedDict):
    id: str
    external_id: str
    network: TronNetwork
    address: str


class GetOfframpWalletInput(TypedDict):
    receiver_id: str
    bank_account_id: str
    id: str


class OfframpWalletsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, data: ListOfframpWalletsInput) -> BlindpayApiResponse[ListOfframpWalletsResponse]:
        receiver_id = data["receiver_id"]
        bank_account_id = data["bank_account_id"]
        return await self._client.get(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts/{bank_account_id}/offramp-wallets"
        )

    async def create(self, data: CreateOfframpWalletInput) -> BlindpayApiResponse[CreateOfframpWalletResponse]:
        receiver_id = data["receiver_id"]
        bank_account_id = data["bank_account_id"]
        payload = {k: v for k, v in data.items() if k not in ["receiver_id", "bank_account_id"]}
        return await self._client.post(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts/{bank_account_id}/offramp-wallets",
            payload,
        )

    async def get(self, data: GetOfframpWalletInput) -> BlindpayApiResponse[GetOfframpWalletResponse]:
        receiver_id = data["receiver_id"]
        bank_account_id = data["bank_account_id"]
        id = data["id"]
        return await self._client.get(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts/{bank_account_id}/offramp-wallets/{id}"
        )


class OfframpWalletsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, data: ListOfframpWalletsInput) -> BlindpayApiResponse[ListOfframpWalletsResponse]:
        receiver_id = data["receiver_id"]
        bank_account_id = data["bank_account_id"]
        return self._client.get(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts/{bank_account_id}/offramp-wallets"
        )

    def create(self, data: CreateOfframpWalletInput) -> BlindpayApiResponse[CreateOfframpWalletResponse]:
        receiver_id = data["receiver_id"]
        bank_account_id = data["bank_account_id"]
        payload = {k: v for k, v in data.items() if k not in ["receiver_id", "bank_account_id"]}
        return self._client.post(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts/{bank_account_id}/offramp-wallets",
            payload,
        )

    def get(self, data: GetOfframpWalletInput) -> BlindpayApiResponse[GetOfframpWalletResponse]:
        receiver_id = data["receiver_id"]
        bank_account_id = data["bank_account_id"]
        id = data["id"]
        return self._client.get(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/bank-accounts/{bank_account_id}/offramp-wallets/{id}"
        )


def create_offramp_wallets_resource(instance_id: str, client: InternalApiClient) -> OfframpWalletsResource:
    return OfframpWalletsResource(instance_id, client)


def create_offramp_wallets_resource_sync(instance_id: str, client: InternalApiClientSync) -> OfframpWalletsResourceSync:
    return OfframpWalletsResourceSync(instance_id, client)
