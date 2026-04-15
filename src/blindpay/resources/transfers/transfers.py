from typing import List, Optional
from urllib.parse import urlencode

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import (
    BlindpayApiResponse,
    Currency,
    PaginationMetadata,
    PaginationParams,
    TransactionStatus,
)


class TrackingStep(TypedDict):
    status: str
    date: Optional[str]


class Transfer(TypedDict):
    id: str
    instance_id: str
    status: TransactionStatus
    quote_id: str
    source_wallet_id: str
    destination_wallet_id: str
    amount: float
    currency: Currency
    tracking_transaction: TrackingStep
    tracking_transaction_monitoring: TrackingStep
    tracking_complete: TrackingStep
    created_at: str
    updated_at: str


class CreateTransferQuoteInput(TypedDict):
    source_wallet_id: str
    destination_wallet_id: str
    amount: float


class CreateTransferQuoteResponse(TypedDict):
    id: str
    amount: float
    currency: Currency
    fee_amount: float
    source_wallet_id: str
    destination_wallet_id: str


class CreateTransferInput(TypedDict):
    quote_id: str


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
