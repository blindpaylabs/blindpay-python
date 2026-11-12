from typing import AsyncIterator, Iterator, List, Optional, Union

from typing_extensions import Literal, NotRequired, Required, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, build_query, path_param
from ..._internal.pagination import async_auto_paging_iter, auto_paging_iter
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
    estimated_time_of_arrival: NotRequired[Optional[str]]


class CreateTransferQuoteInput(TypedDict, total=False):
    wallet_id: Required[str]
    sender_token: Required[StablecoinToken]
    customer_wallet_address: Required[str]
    customer_token: Required[StablecoinToken]
    customer_network: Required[Network]
    request_amount: Required[int]
    """Integer cents (1000 = 10.00). A swap between different tokens needs at least 100 USDC, measured on the USDC
    side; below that the API returns 400 ``TRANSFERS_SWAP_AMOUNT_BELOW_MINIMUM``."""
    amount_reference: Required[AmountReference]
    cover_fees: Optional[bool]
    partner_fee_id: Optional[str]
    partner_flat_fee: int
    partner_percentage_fee: int


class CreateTransferQuoteResponse(TypedDict):
    id: str
    expires_at: Optional[float]
    commercial_quotation: Optional[float]
    blindpay_quotation: Optional[float]
    receiver_amount: float
    sender_amount: float
    flat_fee: float
    partner_fee_amount: NotRequired[Optional[float]]
    partner_flat_fee: NotRequired[int]
    partner_percentage_fee: NotRequired[int]


class CreateTransferInput(TypedDict):
    transfer_quote_id: str


class Transfer(TypedDict):
    id: str
    instance_id: str
    status: Union[TransactionStatus, str]
    transfer_quote_id: str
    wallet_id: str
    sender_token: Union[StablecoinToken, str]
    sender_amount: float
    receiver_amount: float
    customer_token: Union[StablecoinToken, str]
    customer_network: Union[Network, str]
    customer_wallet_address: str
    customer_id: str
    address: NotRequired[Optional[str]]
    network: str
    tracking_transaction_monitoring: TransferTrackingStep
    tracking_paymaster: TransferTrackingStep
    tracking_bridge_swap: TransferTrackingStep
    tracking_complete: TransferTrackingStep
    tracking_partner_fee: NotRequired[Optional[TransferTrackingStep]]
    created_at: NotRequired[Optional[str]]
    updated_at: NotRequired[Optional[str]]
    image_url: NotRequired[Optional[str]]
    first_name: NotRequired[Optional[str]]
    last_name: NotRequired[Optional[str]]
    legal_name: NotRequired[Optional[str]]
    partner_fee_amount: NotRequired[Optional[float]]
    external_id: NotRequired[Optional[str]]
    partner_flat_fee: NotRequired[int]
    partner_percentage_fee: NotRequired[int]


class CreateTransferTrackingStep(TypedDict):
    step: str
    transaction_hash: NotRequired[Optional[str]]
    gas_fee: NotRequired[Optional[str]]
    completed_at: NotRequired[Optional[str]]
    error_message: NotRequired[Optional[str]]


class CreateTransferTrackingMonitoring(TypedDict):
    step: str
    blockchain_screening: NotRequired[Optional[float]]
    risk_score: NotRequired[Optional[float]]
    completed_at: NotRequired[Optional[str]]


class CreateTransferResponse(TypedDict):
    id: str
    status: Union[TransactionStatus, str]
    tracking_bridge_swap: CreateTransferTrackingStep
    tracking_complete: CreateTransferTrackingStep
    tracking_paymaster: CreateTransferTrackingStep
    tracking_transaction_monitoring: CreateTransferTrackingMonitoring
    tracking_partner_fee: NotRequired[Optional[CreateTransferTrackingStep]]


GetTransferResponse = Transfer


class ListTransfersResponse(TypedDict):
    data: List[Transfer]
    pagination: PaginationMetadata


class ListTransfersInput(PaginationParams, total=False):
    customer_id: str
    wallet_id: str
    status: TransactionStatus
    network: Network
    token: StablecoinToken


class TransfersResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def create_quote(
        self, data: CreateTransferQuoteInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateTransferQuoteResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/transfer-quotes", data, options=options)

    async def create(
        self, data: CreateTransferInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateTransferResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/transfers", data, options=options)

    async def list(
        self, params: Optional[ListTransfersInput] = None, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[ListTransfersResponse]:
        query_string = build_query(params)
        return await self._client.get(f"/instances/{self._instance_id}/transfers{query_string}", options=options)

    def list_auto_paging(self, params: Optional[ListTransfersInput] = None) -> AsyncIterator[Transfer]:
        return async_auto_paging_iter(self.list, params)

    async def get(
        self, transfer_id: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[GetTransferResponse]:
        return await self._client.get(
            f"/instances/{self._instance_id}/transfers/{path_param(transfer_id)}", options=options
        )

    async def get_track(
        self, transfer_id: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[GetTransferResponse]:
        """Public tracking endpoint for BlindPay's web and iOS apps; server-side calls get 401 in production.
        Use ``transfers.get(transfer_id)`` instead."""
        return await self._client.get(f"/e/transfers/{path_param(transfer_id)}", options=options)


class TransfersResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def create_quote(
        self, data: CreateTransferQuoteInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateTransferQuoteResponse]:
        return self._client.post(f"/instances/{self._instance_id}/transfer-quotes", data, options=options)

    def create(
        self, data: CreateTransferInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateTransferResponse]:
        return self._client.post(f"/instances/{self._instance_id}/transfers", data, options=options)

    def list(
        self, params: Optional[ListTransfersInput] = None, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[ListTransfersResponse]:
        query_string = build_query(params)
        return self._client.get(f"/instances/{self._instance_id}/transfers{query_string}", options=options)

    def list_auto_paging(self, params: Optional[ListTransfersInput] = None) -> Iterator[Transfer]:
        return auto_paging_iter(self.list, params)

    def get(
        self, transfer_id: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[GetTransferResponse]:
        return self._client.get(f"/instances/{self._instance_id}/transfers/{path_param(transfer_id)}", options=options)

    def get_track(
        self, transfer_id: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[GetTransferResponse]:
        """Public tracking endpoint for BlindPay's web and iOS apps; server-side calls get 401 in production.
        Use ``transfers.get(transfer_id)`` instead."""
        return self._client.get(f"/e/transfers/{path_param(transfer_id)}", options=options)


def create_transfers_resource(instance_id: str, client: InternalApiClient) -> TransfersResource:
    return TransfersResource(instance_id, client)


def create_transfers_resource_sync(instance_id: str, client: InternalApiClientSync) -> TransfersResourceSync:
    return TransfersResourceSync(instance_id, client)
