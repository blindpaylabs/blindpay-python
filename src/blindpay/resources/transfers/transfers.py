from typing import List, Literal, Optional
from urllib.parse import urlencode

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import (
    BlindpayApiResponse,
    Network,
    PaginationMetadata,
    PaginationParams,
    StablecoinToken,
    TransactionStatus,
)

TransferTrackingStep = Literal["processing", "on_hold", "pending_review", "completed"]


class TrackingBridgeSwap(TypedDict):
    step: TransferTrackingStep
    transaction_hash: Optional[str]
    gas_fee: Optional[str]
    completed_at: Optional[str]
    error_message: Optional[str]


class TrackingPaymaster(TypedDict):
    step: TransferTrackingStep
    transaction_hash: Optional[str]
    gas_fee: Optional[str]
    completed_at: Optional[str]
    error_message: Optional[str]


class TrackingTransactionMonitoring(TypedDict):
    step: TransferTrackingStep
    blockchain_screening: Optional[float]
    risk_score: Optional[float]
    completed_at: Optional[str]


class TrackingTransferComplete(TypedDict):
    step: TransferTrackingStep
    transaction_hash: Optional[str]
    gas_fee: Optional[str]
    completed_at: Optional[str]
    error_message: Optional[str]


class TrackingTransferPartnerFee(TypedDict):
    step: TransferTrackingStep
    transaction_hash: Optional[str]
    gas_fee: Optional[str]
    completed_at: Optional[str]
    error_message: Optional[str]


class Transfer(TypedDict):
    id: str
    status: TransactionStatus
    transfer_quote_id: str
    instance_id: str
    tracking_transaction_monitoring: TrackingTransactionMonitoring
    tracking_paymaster: TrackingPaymaster
    tracking_bridge_swap: TrackingBridgeSwap
    tracking_complete: TrackingTransferComplete
    tracking_partner_fee: TrackingTransferPartnerFee
    created_at: Optional[str]
    updated_at: Optional[str]
    image_url: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    legal_name: Optional[str]
    wallet_id: str
    sender_token: StablecoinToken
    sender_amount: float
    receiver_amount: float
    receiver_network: Network
    receiver_token: StablecoinToken
    receiver_wallet_address: str
    partner_fee_amount: Optional[float]
    external_id: Optional[str]
    receiver_id: str
    address: Optional[str]
    network: Network


class CreateTransferQuoteInput(TypedDict):
    wallet_id: str
    amount_reference: Literal["sender", "receiver"]
    request_amount: int
    sender_token: StablecoinToken
    receiver_wallet_address: str
    receiver_token: StablecoinToken
    receiver_network: Network
    cover_fees: Optional[bool]
    partner_fee_id: Optional[str]


class CreateTransferQuoteResponse(TypedDict):
    id: str
    expires_at: Optional[float]
    commercial_quotation: Optional[float]
    blindpay_quotation: Optional[float]
    receiver_amount: Optional[float]
    sender_amount: Optional[float]
    partner_fee_amount: Optional[float]
    flat_fee: Optional[float]


class CreateTransferInput(TypedDict):
    transfer_quote_id: str


class CreateTransferResponse(TypedDict):
    id: str
    status: TransactionStatus
    tracking_bridge_swap: TrackingBridgeSwap
    tracking_complete: TrackingTransferComplete
    tracking_paymaster: TrackingPaymaster
    tracking_transaction_monitoring: TrackingTransactionMonitoring
    tracking_partner_fee: TrackingTransferPartnerFee


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
