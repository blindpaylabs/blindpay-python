from typing import AsyncIterator, Iterator, List, Optional, Union

from typing_extensions import Literal, NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, build_query, path_param
from ..._internal.pagination import async_auto_paging_iter, auto_paging_iter
from ...types import BlindpayApiResponse, Network, PaginationMetadata

YieldStatus = Literal["disabled", "enabled", "disabling"]


class CustodialWallet(TypedDict):
    id: str
    customer_id: NotRequired[str]
    instance_id: NotRequired[str]
    network: Union[Network, str]
    address: NotRequired[Optional[str]]
    created_at: NotRequired[Optional[str]]
    yield_status: NotRequired[Optional[Union[YieldStatus, str]]]


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


WalletDepositStatus = Literal["processing", "completed", "on_hold", "refunded"]
WalletDepositToken = Literal["USDC", "USDT", "USDB", "EURC", "EURB"]


class WalletDeposit(TypedDict):
    """A deposit into a managed wallet. ``amount`` is integer cents; ``token_amount`` the exact token amount."""

    id: str
    wallet_id: str
    network: Union[Network, str]
    token: Union[WalletDepositToken, str]
    amount: int
    token_amount: Optional[str]
    status: Union[WalletDepositStatus, str]
    transaction_hash: str
    sender_address: Optional[str]
    created_at: str


class ListWalletDepositsResponse(TypedDict):
    data: List[WalletDeposit]
    pagination: PaginationMetadata


class GetWalletDepositsInput(TypedDict):
    """``limit`` is one of 5, 10, 50, 100, 200 (default 10); the API always returns the envelope."""

    customer_id: str
    id: str
    limit: NotRequired[Union[Literal["5", "10", "50", "100", "200"], int]]
    starting_after: NotRequired[str]
    ending_before: NotRequired[str]
    token: NotRequired[WalletDepositToken]
    status: NotRequired[WalletDepositStatus]


class CustodialWalletsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, customer_id: str) -> BlindpayApiResponse[ListCustodialWalletsResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/wallets")

    async def get(self, data: GetCustodialWalletInput) -> BlindpayApiResponse[CustodialWallet]:
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(data['customer_id'])}/wallets/{path_param(data['id'])}"
        )

    async def create(
        self, data: CreateCustodialWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateCustodialWalletResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/wallets", payload, options=options
        )

    async def get_balance(self, data: GetCustodialWalletInput) -> BlindpayApiResponse[CustodialWalletBalance]:
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(data['customer_id'])}/wallets/{path_param(data['id'])}/balance"
        )

    async def delete(
        self, data: DeleteCustodialWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        return await self._client.delete(
            f"/instances/{self._instance_id}/customers/{path_param(data['customer_id'])}/wallets/{path_param(data['id'])}",
            options=options,
        )

    async def get_deposits(self, data: GetWalletDepositsInput) -> BlindpayApiResponse[ListWalletDepositsResponse]:
        query_string = build_query({k: v for k, v in data.items() if k not in ("customer_id", "id")})
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(data['customer_id'])}"
            f"/wallets/{path_param(data['id'])}/deposits{query_string}"
        )

    def get_deposits_auto_paging(self, data: GetWalletDepositsInput) -> AsyncIterator[WalletDeposit]:
        return async_auto_paging_iter(self.get_deposits, data)


class CustodialWalletsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, customer_id: str) -> BlindpayApiResponse[ListCustodialWalletsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/wallets")

    def get(self, data: GetCustodialWalletInput) -> BlindpayApiResponse[CustodialWallet]:
        return self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(data['customer_id'])}/wallets/{path_param(data['id'])}"
        )

    def create(
        self, data: CreateCustodialWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateCustodialWalletResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/wallets", payload, options=options
        )

    def get_balance(self, data: GetCustodialWalletInput) -> BlindpayApiResponse[CustodialWalletBalance]:
        return self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(data['customer_id'])}/wallets/{path_param(data['id'])}/balance"
        )

    def delete(
        self, data: DeleteCustodialWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        return self._client.delete(
            f"/instances/{self._instance_id}/customers/{path_param(data['customer_id'])}/wallets/{path_param(data['id'])}",
            options=options,
        )

    def get_deposits(self, data: GetWalletDepositsInput) -> BlindpayApiResponse[ListWalletDepositsResponse]:
        query_string = build_query({k: v for k, v in data.items() if k not in ("customer_id", "id")})
        return self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(data['customer_id'])}"
            f"/wallets/{path_param(data['id'])}/deposits{query_string}"
        )

    def get_deposits_auto_paging(self, data: GetWalletDepositsInput) -> Iterator[WalletDeposit]:
        return auto_paging_iter(self.get_deposits, data)


def create_custodial_wallets_resource(instance_id: str, client: InternalApiClient) -> CustodialWalletsResource:
    return CustodialWalletsResource(instance_id, client)


def create_custodial_wallets_resource_sync(
    instance_id: str, client: InternalApiClientSync
) -> CustodialWalletsResourceSync:
    return CustodialWalletsResourceSync(instance_id, client)
