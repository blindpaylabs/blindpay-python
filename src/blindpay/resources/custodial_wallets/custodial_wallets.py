from typing import List, Optional

from typing_extensions import NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions
from ...types import BlindpayApiResponse, Network


class CustodialWallet(TypedDict):
    id: str
    customer_id: str
    instance_id: str
    network: Network
    address: Optional[str]
    created_at: Optional[str]


class CustodialWalletBalanceToken(TypedDict):
    id: str
    address: str
    symbol: str
    amount: float
    earning_amount: float
    total_amount: float


class CustodialWalletBalance(TypedDict):
    # Keyed by uppercase token symbol, as the API returns them. Amounts are whole tokens, not cents.
    USDC: CustodialWalletBalanceToken
    USDT: CustodialWalletBalanceToken
    USDB: CustodialWalletBalanceToken
    EURC: NotRequired[CustodialWalletBalanceToken]
    EURB: NotRequired[CustodialWalletBalanceToken]


class CreateCustodialWalletInput(TypedDict):
    customer_id: str
    network: Network
    name: str
    external_id: NotRequired[Optional[str]]


CreateCustodialWalletResponse = CustodialWallet
ListCustodialWalletsResponse = List[CustodialWallet]


class GetCustodialWalletInput(TypedDict):
    customer_id: str
    id: str


class DeleteCustodialWalletInput(TypedDict):
    customer_id: str
    id: str


class CustodialWalletsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, customer_id: str) -> BlindpayApiResponse[ListCustodialWalletsResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/customers/{customer_id}/wallets")

    async def get(self, data: GetCustodialWalletInput) -> BlindpayApiResponse[CustodialWallet]:
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{data['customer_id']}/wallets/{data['id']}"
        )

    async def create(
        self, data: CreateCustodialWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateCustodialWalletResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{customer_id}/wallets", payload, options=options
        )

    async def get_balance(self, data: GetCustodialWalletInput) -> BlindpayApiResponse[CustodialWalletBalance]:
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{data['customer_id']}/wallets/{data['id']}/balance"
        )

    async def delete(
        self, data: DeleteCustodialWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        return await self._client.delete(
            f"/instances/{self._instance_id}/customers/{data['customer_id']}/wallets/{data['id']}", options=options
        )


class CustodialWalletsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, customer_id: str) -> BlindpayApiResponse[ListCustodialWalletsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/customers/{customer_id}/wallets")

    def get(self, data: GetCustodialWalletInput) -> BlindpayApiResponse[CustodialWallet]:
        return self._client.get(f"/instances/{self._instance_id}/customers/{data['customer_id']}/wallets/{data['id']}")

    def create(
        self, data: CreateCustodialWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateCustodialWalletResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{customer_id}/wallets", payload, options=options
        )

    def get_balance(self, data: GetCustodialWalletInput) -> BlindpayApiResponse[CustodialWalletBalance]:
        return self._client.get(
            f"/instances/{self._instance_id}/customers/{data['customer_id']}/wallets/{data['id']}/balance"
        )

    def delete(
        self, data: DeleteCustodialWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        return self._client.delete(
            f"/instances/{self._instance_id}/customers/{data['customer_id']}/wallets/{data['id']}", options=options
        )


def create_custodial_wallets_resource(instance_id: str, client: InternalApiClient) -> CustodialWalletsResource:
    return CustodialWalletsResource(instance_id, client)


def create_custodial_wallets_resource_sync(
    instance_id: str, client: InternalApiClientSync
) -> CustodialWalletsResourceSync:
    return CustodialWalletsResourceSync(instance_id, client)
