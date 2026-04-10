from typing import List, Optional

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse, Network


class CustodialWallet(TypedDict):
    id: str
    receiver_id: str
    instance_id: str
    network: Network
    address: str
    created_at: str


class CustodialWalletBalanceToken(TypedDict):
    amount: float
    token: str
    address: str


class CustodialWalletBalance(TypedDict):
    usdc: Optional[CustodialWalletBalanceToken]
    usdt: Optional[CustodialWalletBalanceToken]
    usdb: Optional[CustodialWalletBalanceToken]


class CreateCustodialWalletInput(TypedDict):
    receiver_id: str
    network: Network


CreateCustodialWalletResponse = CustodialWallet
ListCustodialWalletsResponse = List[CustodialWallet]


class GetCustodialWalletInput(TypedDict):
    receiver_id: str
    id: str


class DeleteCustodialWalletInput(TypedDict):
    receiver_id: str
    id: str


class CustodialWalletsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, receiver_id: str) -> BlindpayApiResponse[ListCustodialWalletsResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/wallets")

    async def get(self, data: GetCustodialWalletInput) -> BlindpayApiResponse[CustodialWallet]:
        return await self._client.get(
            f"/instances/{self._instance_id}/receivers/{data['receiver_id']}/wallets/{data['id']}"
        )

    async def create(self, data: CreateCustodialWalletInput) -> BlindpayApiResponse[CreateCustodialWalletResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        return await self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/wallets", payload)

    async def get_balance(self, data: GetCustodialWalletInput) -> BlindpayApiResponse[CustodialWalletBalance]:
        return await self._client.get(
            f"/instances/{self._instance_id}/receivers/{data['receiver_id']}/wallets/{data['id']}/balance"
        )

    async def delete(self, data: DeleteCustodialWalletInput) -> BlindpayApiResponse[None]:
        return await self._client.delete(
            f"/instances/{self._instance_id}/receivers/{data['receiver_id']}/wallets/{data['id']}"
        )


class CustodialWalletsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, receiver_id: str) -> BlindpayApiResponse[ListCustodialWalletsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/wallets")

    def get(self, data: GetCustodialWalletInput) -> BlindpayApiResponse[CustodialWallet]:
        return self._client.get(f"/instances/{self._instance_id}/receivers/{data['receiver_id']}/wallets/{data['id']}")

    def create(self, data: CreateCustodialWalletInput) -> BlindpayApiResponse[CreateCustodialWalletResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/wallets", payload)

    def get_balance(self, data: GetCustodialWalletInput) -> BlindpayApiResponse[CustodialWalletBalance]:
        return self._client.get(
            f"/instances/{self._instance_id}/receivers/{data['receiver_id']}/wallets/{data['id']}/balance"
        )

    def delete(self, data: DeleteCustodialWalletInput) -> BlindpayApiResponse[None]:
        return self._client.delete(
            f"/instances/{self._instance_id}/receivers/{data['receiver_id']}/wallets/{data['id']}"
        )


def create_custodial_wallets_resource(instance_id: str, client: InternalApiClient) -> CustodialWalletsResource:
    return CustodialWalletsResource(instance_id, client)


def create_custodial_wallets_resource_sync(
    instance_id: str, client: InternalApiClientSync
) -> CustodialWalletsResourceSync:
    return CustodialWalletsResourceSync(instance_id, client)
