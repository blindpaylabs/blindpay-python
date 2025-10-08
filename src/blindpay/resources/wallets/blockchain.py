from typing import List, Optional

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse, Network


class GetBlockchainWalletMessageResponse(TypedDict):
    message: str


class BlockchainWallet(TypedDict):
    id: str
    name: str
    network: Network
    address: Optional[str]
    signature_tx_hash: Optional[str]
    is_account_abstraction: bool
    receiver_id: str


ListBlockchainWalletsResponse = List[BlockchainWallet]
GetBlockchainWalletResponse = BlockchainWallet
CreateBlockchainWalletResponse = BlockchainWallet


class CreateBlockchainWalletWithAddressInput(TypedDict):
    receiver_id: str
    name: str
    network: Network
    address: str


class CreateBlockchainWalletWithHashInput(TypedDict):
    receiver_id: str
    name: str
    network: Network
    signature_tx_hash: str


class GetBlockchainWalletInput(TypedDict):
    receiver_id: str
    id: str


class DeleteBlockchainWalletInput(TypedDict):
    receiver_id: str
    id: str


class CreateAssetTrustlineResponse(TypedDict):
    xdr: str


class MintUsdbStellarInput(TypedDict):
    address: str
    amount: str
    signedXdr: str


class BlockchainWalletsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, receiver_id: str) -> BlindpayApiResponse[ListBlockchainWalletsResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/blockchain-wallets")

    async def create_with_address(
        self, data: CreateBlockchainWalletWithAddressInput
    ) -> BlindpayApiResponse[CreateBlockchainWalletResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["is_account_abstraction"] = True
        return await self._client.post(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/blockchain-wallets", payload
        )

    async def create_with_hash(
        self, data: CreateBlockchainWalletWithHashInput
    ) -> BlindpayApiResponse[CreateBlockchainWalletResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["is_account_abstraction"] = False
        return await self._client.post(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/blockchain-wallets", payload
        )

    async def get_wallet_message(self, receiver_id: str) -> BlindpayApiResponse[GetBlockchainWalletMessageResponse]:
        return await self._client.get(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/blockchain-wallets/sign-message"
        )

    async def get(self, data: GetBlockchainWalletInput) -> BlindpayApiResponse[GetBlockchainWalletResponse]:
        receiver_id = data["receiver_id"]
        id = data["id"]
        return await self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/blockchain-wallets/{id}")

    async def delete(self, data: DeleteBlockchainWalletInput) -> BlindpayApiResponse[None]:
        receiver_id = data["receiver_id"]
        id = data["id"]
        return await self._client.delete(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/blockchain-wallets/{id}"
        )

    async def create_asset_trustline(self, address: str) -> BlindpayApiResponse[CreateAssetTrustlineResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/create-asset-trustline", {"address": address})

    async def mint_usdb_stellar(self, data: MintUsdbStellarInput) -> BlindpayApiResponse[None]:
        return await self._client.post(f"/instances/{self._instance_id}/mint-usdb-stellar", data)


class BlockchainWalletsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, receiver_id: str) -> BlindpayApiResponse[ListBlockchainWalletsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/blockchain-wallets")

    def create_with_address(
        self, data: CreateBlockchainWalletWithAddressInput
    ) -> BlindpayApiResponse[CreateBlockchainWalletResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["is_account_abstraction"] = True
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/blockchain-wallets", payload)

    def create_with_hash(
        self, data: CreateBlockchainWalletWithHashInput
    ) -> BlindpayApiResponse[CreateBlockchainWalletResponse]:
        receiver_id = data["receiver_id"]
        payload = {k: v for k, v in data.items() if k != "receiver_id"}
        payload["is_account_abstraction"] = False
        return self._client.post(f"/instances/{self._instance_id}/receivers/{receiver_id}/blockchain-wallets", payload)

    def get_wallet_message(self, receiver_id: str) -> BlindpayApiResponse[GetBlockchainWalletMessageResponse]:
        return self._client.get(
            f"/instances/{self._instance_id}/receivers/{receiver_id}/blockchain-wallets/sign-message"
        )

    def get(self, data: GetBlockchainWalletInput) -> BlindpayApiResponse[GetBlockchainWalletResponse]:
        receiver_id = data["receiver_id"]
        id = data["id"]
        return self._client.get(f"/instances/{self._instance_id}/receivers/{receiver_id}/blockchain-wallets/{id}")

    def delete(self, data: DeleteBlockchainWalletInput) -> BlindpayApiResponse[None]:
        receiver_id = data["receiver_id"]
        id = data["id"]
        return self._client.delete(f"/instances/{self._instance_id}/receivers/{receiver_id}/blockchain-wallets/{id}")

    def create_asset_trustline(self, address: str) -> BlindpayApiResponse[CreateAssetTrustlineResponse]:
        return self._client.post(f"/instances/{self._instance_id}/create-asset-trustline", {"address": address})

    def mint_usdb_stellar(self, data: MintUsdbStellarInput) -> BlindpayApiResponse[None]:
        return self._client.post(f"/instances/{self._instance_id}/mint-usdb-stellar", data)


def create_blockchain_wallets_resource(instance_id: str, client: InternalApiClient) -> BlockchainWalletsResource:
    return BlockchainWalletsResource(instance_id, client)


def create_blockchain_wallets_resource_sync(
    instance_id: str, client: InternalApiClientSync
) -> BlockchainWalletsResourceSync:
    return BlockchainWalletsResourceSync(instance_id, client)
