from typing import List, Optional, TypedDict
from urllib.parse import urlencode

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import (
    BlindpayApiResponse,
    Network,
    PaginationMetadata,
    PaginationParams,
    StablecoinToken,
    TrackingComplete,
    TrackingPartnerFee,
    TrackingPayment,
    TrackingTransaction,
    TransactionStatus,
)


class AchDetails(TypedDict):
    routing_number: str
    account_number: str


class WireDetails(TypedDict):
    routing_number: str
    account_number: str


class RtpDetails(TypedDict):
    routing_number: str
    account_number: str


class BeneficiaryDetails(TypedDict):
    name: str
    address_line_1: str
    address_line_2: Optional[str]


class ReceivingBankDetails(TypedDict):
    name: str
    address_line_1: str
    address_line_2: Optional[str]


class BankDetails(TypedDict):
    routing_number: str
    account_number: str
    account_type: str
    swift_bic_code: str
    ach: AchDetails
    wire: WireDetails
    rtp: RtpDetails
    beneficiary: BeneficiaryDetails
    receiving_bank: ReceivingBankDetails


class Payin(TypedDict):
    receiver_id: str
    id: str
    pix_code: Optional[str]
    memo_code: Optional[str]
    clabe: Optional[str]
    status: TransactionStatus
    payin_quote_id: str
    instance_id: str
    tracking_transaction: Optional[TrackingTransaction]
    tracking_payment: Optional[TrackingPayment]
    tracking_complete: Optional[TrackingComplete]
    tracking_partner_fee: Optional[TrackingPartnerFee]
    created_at: str
    updated_at: str
    image_url: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    legal_name: Optional[str]
    type: str
    payment_method: str
    sender_amount: float
    receiver_amount: float
    token: StablecoinToken
    partner_fee_amount: float
    total_fee_amount: float
    commercial_quotation: float
    blindpay_quotation: float
    currency: str
    billing_fee: float
    name: str
    address: str
    network: Network
    blindpay_bank_details: BankDetails


class ListPayinsInput(PaginationParams):
    status: Optional[TransactionStatus]
    receiver_id: Optional[str]


class ListPayinsResponse(TypedDict):
    data: List[Payin]
    pagination: PaginationMetadata


class CreatePayinInput(TypedDict):
    quote_id: str
    sender_address: str
    receiver_address: str
    amount: float
    token: StablecoinToken
    network: Network
    description: Optional[str]


class GetPayinTrackingTransaction(TypedDict):
    step: str
    status: str
    external_id: str
    completed_at: str
    sender_name: str
    sender_tax_id: str
    sender_bank_code: str
    sender_account_number: str
    trace_number: str
    transaction_reference: str
    description: str


class GetPayinTrackResponse(TypedDict):
    receiver_id: str
    id: str
    pix_code: str
    memo_code: str
    clabe: str
    status: str
    payin_quote_id: str
    instance_id: str
    tracking_transaction: TrackingTransaction
    tracking_payment: TrackingPayment
    tracking_complete: TrackingComplete
    tracking_partner_fee: TrackingPartnerFee
    created_at: str
    updated_at: str
    image_url: str
    first_name: str
    last_name: str
    legal_name: str
    type: str
    payment_method: str
    sender_amount: float
    receiver_amount: float
    token: StablecoinToken
    partner_fee_amount: float
    total_fee_amount: float
    commercial_quotation: float
    blindpay_quotation: float
    currency: str
    billing_fee: float
    name: str
    address: str
    network: Network
    blindpay_bank_details: BankDetails


class ExportPayinsInput(TypedDict):
    limit: Optional[str]
    offset: Optional[str]
    status: TransactionStatus


ExportPayinsResponse = List[Payin]


class CreateEvmPayinResponse(TypedDict):
    id: str
    status: TransactionStatus
    pix_code: Optional[str]
    memo_code: Optional[str]
    clabe: Optional[str]
    tracking_complete: Optional[TrackingComplete]
    tracking_payment: Optional[TrackingPayment]
    tracking_transaction: Optional[TrackingTransaction]
    tracking_partner_fee: Optional[TrackingPartnerFee]
    blindpay_bank_details: BankDetails
    receiver_id: str
    receiver_amount: float


class PayinsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, params: Optional[ListPayinsInput] = None) -> BlindpayApiResponse[ListPayinsResponse]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return await self._client.get(f"/instances/{self._instance_id}/payins{query_string}")

    async def get(self, payin_id: str) -> BlindpayApiResponse[Payin]:
        return await self._client.get(f"/instances/{self._instance_id}/payins/{payin_id}")

    async def export(self, params: ExportPayinsInput) -> BlindpayApiResponse[ExportPayinsResponse]:
        filtered_params = {k: v for k, v in params.items() if v is not None}
        query_string = f"?{urlencode(filtered_params)}" if filtered_params else ""
        return await self._client.get(f"/instances/{self._instance_id}/export/payins{query_string}")

    async def create_evm(self, payin_quote_id: str) -> BlindpayApiResponse[CreateEvmPayinResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/payins/evm", {"payin_quote_id": payin_quote_id})


class PayinsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, params: Optional[ListPayinsInput] = None) -> BlindpayApiResponse[ListPayinsResponse]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return self._client.get(f"/instances/{self._instance_id}/payins{query_string}")

    def get(self, payin_id: str) -> BlindpayApiResponse[Payin]:
        return self._client.get(f"/instances/{self._instance_id}/payins/{payin_id}")

    def get_track(self, payin_id: str) -> BlindpayApiResponse[GetPayinTrackResponse]:
        return self._client.get(f"/e/payins/{payin_id}")

    def export(self, params: ExportPayinsInput) -> BlindpayApiResponse[ExportPayinsResponse]:
        filtered_params = {k: v for k, v in params.items() if v is not None}
        query_string = f"?{urlencode(filtered_params)}" if filtered_params else ""
        return self._client.get(f"/instances/{self._instance_id}/export/payins{query_string}")

    def create_evm(self, payin_quote_id: str) -> BlindpayApiResponse[CreateEvmPayinResponse]:
        return self._client.post(f"/instances/{self._instance_id}/payins/evm", {"payin_quote_id": payin_quote_id})


def create_payins_resource(instance_id: str, client: InternalApiClient) -> PayinsResource:
    return PayinsResource(instance_id, client)


def create_payins_resource_sync(instance_id: str, client: InternalApiClientSync) -> PayinsResourceSync:
    return PayinsResourceSync(instance_id, client)
