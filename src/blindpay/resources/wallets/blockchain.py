from typing import List, Optional

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, path_param
from ...types import BlindpayApiResponse, Network


class GetBlockchainWalletMessageResponse(TypedDict):
    message: str


class BlockchainWallet(TypedDict):
    id: str
    name: Optional[str]
    network: Optional[Network]
    address: Optional[str]
    signature_tx_hash: Optional[str]
    is_account_abstraction: Optional[bool]
    customer_id: str


ListBlockchainWalletsResponse = List[BlockchainWallet]
GetBlockchainWalletResponse = BlockchainWallet
CreateBlockchainWalletResponse = BlockchainWallet


class CreateBlockchainWalletWithAddressInput(TypedDict):
    customer_id: str
    name: str
    network: Network
    address: Optional[str]


class CreateBlockchainWalletWithHashInput(TypedDict):
    customer_id: str
    name: str
    network: Network
    signature_tx_hash: Optional[str]


class GetBlockchainWalletInput(TypedDict):
    customer_id: str
    id: str


class DeleteBlockchainWalletInput(TypedDict):
    customer_id: str
    id: str


class CreateAssetTrustlineResponse(TypedDict):
    xdr: str


class MintUsdbStellarInput(TypedDict):
    address: str
    amount: str
    signedXdr: str


class MintUsdbSolanaInput(TypedDict):
    address: str
    amount: str


class MintUsdbSolanaResponse(TypedDict):
    success: bool
    signature: str


class PrepareSolanaDelegationTransactionInput(TypedDict):
    amount: str
    owner_address: str
    token_address: str


class PrepareSolanaDelegationTransactionResponse(TypedDict):
    success: bool
    transaction: str


class BlockchainWalletsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, customer_id: str) -> BlindpayApiResponse[ListBlockchainWalletsResponse]:
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/blockchain-wallets"
        )

    async def create_with_address(
        self, data: CreateBlockchainWalletWithAddressInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateBlockchainWalletResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["is_account_abstraction"] = True
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/blockchain-wallets",
            payload,
            options=options,
        )

    async def create_with_hash(
        self, data: CreateBlockchainWalletWithHashInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateBlockchainWalletResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["is_account_abstraction"] = False
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/blockchain-wallets",
            payload,
            options=options,
        )

    async def get_wallet_message(self, customer_id: str) -> BlindpayApiResponse[GetBlockchainWalletMessageResponse]:
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/blockchain-wallets/sign-message"
        )

    async def get(self, data: GetBlockchainWalletInput) -> BlindpayApiResponse[GetBlockchainWalletResponse]:
        customer_id = data["customer_id"]
        id = data["id"]
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/blockchain-wallets/{path_param(id)}"
        )

    async def delete(
        self, data: DeleteBlockchainWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        customer_id = data["customer_id"]
        id = data["id"]
        return await self._client.delete(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/blockchain-wallets/{path_param(id)}",
            options=options,
        )

    async def create_asset_trustline(
        self, address: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateAssetTrustlineResponse]:
        return await self._client.post(
            f"/instances/{self._instance_id}/create-asset-trustline", {"address": address}, options=options
        )

    async def mint_usdb_stellar(
        self, data: MintUsdbStellarInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        return await self._client.post(f"/instances/{self._instance_id}/mint-usdb-stellar", data, options=options)

    async def mint_usdb_solana(
        self, data: MintUsdbSolanaInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[MintUsdbSolanaResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/mint-usdb-solana", data, options=options)

    async def prepare_solana_delegation_transaction(
        self, data: PrepareSolanaDelegationTransactionInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[PrepareSolanaDelegationTransactionResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/prepare-delegate-solana", data, options=options)


class BlockchainWalletsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, customer_id: str) -> BlindpayApiResponse[ListBlockchainWalletsResponse]:
        return self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/blockchain-wallets"
        )

    def create_with_address(
        self, data: CreateBlockchainWalletWithAddressInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateBlockchainWalletResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["is_account_abstraction"] = True
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/blockchain-wallets",
            payload,
            options=options,
        )

    def create_with_hash(
        self, data: CreateBlockchainWalletWithHashInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateBlockchainWalletResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        payload["is_account_abstraction"] = False
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/blockchain-wallets",
            payload,
            options=options,
        )

    def get_wallet_message(self, customer_id: str) -> BlindpayApiResponse[GetBlockchainWalletMessageResponse]:
        return self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/blockchain-wallets/sign-message"
        )

    def get(self, data: GetBlockchainWalletInput) -> BlindpayApiResponse[GetBlockchainWalletResponse]:
        customer_id = data["customer_id"]
        id = data["id"]
        return self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/blockchain-wallets/{path_param(id)}"
        )

    def delete(
        self, data: DeleteBlockchainWalletInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        customer_id = data["customer_id"]
        id = data["id"]
        return self._client.delete(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/blockchain-wallets/{path_param(id)}",
            options=options,
        )

    def create_asset_trustline(
        self, address: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateAssetTrustlineResponse]:
        return self._client.post(
            f"/instances/{self._instance_id}/create-asset-trustline", {"address": address}, options=options
        )

    def mint_usdb_stellar(
        self, data: MintUsdbStellarInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        return self._client.post(f"/instances/{self._instance_id}/mint-usdb-stellar", data, options=options)

    def mint_usdb_solana(
        self, data: MintUsdbSolanaInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[MintUsdbSolanaResponse]:
        return self._client.post(f"/instances/{self._instance_id}/mint-usdb-solana", data, options=options)

    def prepare_solana_delegation_transaction(
        self, data: PrepareSolanaDelegationTransactionInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[PrepareSolanaDelegationTransactionResponse]:
        return self._client.post(f"/instances/{self._instance_id}/prepare-delegate-solana", data, options=options)


def create_blockchain_wallets_resource(instance_id: str, client: InternalApiClient) -> BlockchainWalletsResource:
    return BlockchainWalletsResource(instance_id, client)


def create_blockchain_wallets_resource_sync(
    instance_id: str, client: InternalApiClientSync
) -> BlockchainWalletsResourceSync:
    return BlockchainWalletsResourceSync(instance_id, client)
