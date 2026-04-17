from typing import List, Optional
from urllib.parse import urlencode

from typing_extensions import Literal, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import (
    BlindpayApiResponse,
    Network,
    PaginationMetadata,
    PaginationParams,
    StablecoinToken,
    TransactionStatus,
)

AmountReference = Literal["sender", "receiver"]


class TransferTrackingStep(TypedDict):
    step: str
    estimated_time_of_arrival: Optional[str]


class CreateTransferQuoteInput(TypedDict, total=False):
    wallet_id: str
    sender_token: StablecoinToken
    receiver_wallet_address: str
    receiver_token: StablecoinToken
    receiver_network: Network
    request_amount: int
    amount_reference: AmountReference
    cover_fees: Optional[bool]
    partner_fee_id: Optional[str]


class CreateTransferQuoteResponse(TypedDict):
    id: str
    expires_at: Optional[float]
    commercial_quotation: Optional[float]
    blindpay_quotation: Optional[float]
    receiver_amount: float
    sender_amount: float
    flat_fee: float
    partner_fee_amount: Optional[float]


class CreateTransferInput(TypedDict):
    transfer_quote_id: str


class Transfer(TypedDict):
    id: str
    instance_id: str
    status: TransactionStatus
    transfer_quote_id: str
    wallet_id: str
    sender_token: StablecoinToken
    sender_amount: float
    receiver_amount: float
    receiver_token: StablecoinToken
    receiver_network: Network
    receiver_wallet_address: str
    receiver_id: str
    address: str
    network: str
    tracking_transaction_monitoring: TransferTrackingStep
    tracking_paymaster: TransferTrackingStep
    tracking_bridge_swap: TransferTrackingStep
    tracking_complete: TransferTrackingStep
    tracking_partner_fee: TransferTrackingStep
    created_at: str
    updated_at: str
    image_url: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    legal_name: Optional[str]
    partner_fee_amount: Optional[float]
    external_id: Optional[str]


CreateTransferResponse = Transfer
GetTransferResponse = Transfer


class ListTransfersResponse(TypedDict):
    data: List[Transfer]
    pagination: PaginationMetadata


class TransfersResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def create_quote(self, data: CreateTransferQuoteInput) -> BlindpayApiResponse[CreateTransferQuoteResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/transfer-quotes", data)

    async def create(self, data: CreateTransferInput) -> BlindpayApiResponse[CreateTransferResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/transfers", data)

    async def list(self, params: Optional[PaginationParams] = None) -> BlindpayApiResponse[ListTransfersResponse]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return await self._client.get(f"/instances/{self._instance_id}/transfers{query_string}")

    async def get(self, transfer_id: str) -> BlindpayApiResponse[GetTransferResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/transfers/{transfer_id}")

    async def get_track(self, transfer_id: str) -> BlindpayApiResponse[GetTransferResponse]:
        return await self._client.get(f"/e/transfers/{transfer_id}")


class TransfersResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def create_quote(self, data: CreateTransferQuoteInput) -> BlindpayApiResponse[CreateTransferQuoteResponse]:
        return self._client.post(f"/instances/{self._instance_id}/transfer-quotes", data)

    def create(self, data: CreateTransferInput) -> BlindpayApiResponse[CreateTransferResponse]:
        return self._client.post(f"/instances/{self._instance_id}/transfers", data)

    def list(self, params: Optional[PaginationParams] = None) -> BlindpayApiResponse[ListTransfersResponse]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return self._client.get(f"/instances/{self._instance_id}/transfers{query_string}")

    def get(self, transfer_id: str) -> BlindpayApiResponse[GetTransferResponse]:
        return self._client.get(f"/instances/{self._instance_id}/transfers/{transfer_id}")

    def get_track(self, transfer_id: str) -> BlindpayApiResponse[GetTransferResponse]:
        return self._client.get(f"/e/transfers/{transfer_id}")


def create_transfers_resource(instance_id: str, client: InternalApiClient) -> TransfersResource:
    return TransfersResource(instance_id, client)


def create_transfers_resource_sync(instance_id: str, client: InternalApiClientSync) -> TransfersResourceSync:
    return TransfersResourceSync(instance_id, client)
