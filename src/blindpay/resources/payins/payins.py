from typing import AsyncIterator, Iterator, List, NotRequired, Optional, TypedDict, Union

from typing_extensions import deprecated

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, build_query, path_param
from ..._internal.pagination import async_auto_paging_iter, auto_paging_iter
from ...types import (
    BlindpayApiResponse,
    Country,
    ManualExecutionStatus,
    Network,
    PaginationMetadata,
    PaginationParams,
    PaymentMethod,
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
    name: NotRequired[str]
    address_line_1: NotRequired[str]
    address_line_2: NotRequired[Optional[str]]


class ReceivingBankDetails(TypedDict):
    name: NotRequired[str]
    address_line_1: NotRequired[str]
    address_line_2: NotRequired[Optional[str]]


class BankDetails(TypedDict):
    routing_number: NotRequired[str]
    account_number: NotRequired[str]
    account_type: NotRequired[str]
    swift_bic_code: NotRequired[Optional[str]]
    ach: NotRequired[Optional[AchDetails]]
    wire: NotRequired[Optional[WireDetails]]
    rtp: NotRequired[Optional[RtpDetails]]
    beneficiary: BeneficiaryDetails
    receiving_bank: ReceivingBankDetails


class Payin(TypedDict):
    customer_id: str
    id: str
    pix_code: NotRequired[Optional[str]]
    memo_code: NotRequired[Optional[str]]
    clabe: NotRequired[Optional[str]]
    status: Union[TransactionStatus, str]
    manual_execution_status: NotRequired[Optional[Union[ManualExecutionStatus, str]]]
    payin_quote_id: str
    instance_id: str
    tracking_transaction: Optional[TrackingTransaction]
    tracking_payment: Optional[TrackingPayment]
    tracking_complete: Optional[TrackingComplete]
    tracking_partner_fee: NotRequired[Optional[TrackingPartnerFee]]
    created_at: NotRequired[Optional[str]]
    updated_at: NotRequired[Optional[str]]
    image_url: NotRequired[Optional[str]]
    first_name: NotRequired[Optional[str]]
    last_name: NotRequired[Optional[str]]
    legal_name: NotRequired[Optional[str]]
    type: str
    payment_method: str
    sender_amount: Optional[float]
    receiver_amount: Optional[float]
    token: Union[StablecoinToken, str]
    partner_fee_amount: NotRequired[Optional[float]]
    total_fee_amount: NotRequired[Optional[float]]
    commercial_quotation: Optional[float]
    blindpay_quotation: Optional[float]
    currency: str
    billing_fee: NotRequired[float]
    name: str
    address: NotRequired[Optional[str]]
    network: Union[Network, str]
    blindpay_bank_details: NotRequired[Optional[BankDetails]]
    is_otc: NotRequired[Optional[bool]]
    billing_fee_amount: NotRequired[Optional[float]]
    pse_document_type: NotRequired[Optional[str]]
    pse_full_name: NotRequired[Optional[str]]
    pse_payment_link: NotRequired[Optional[str]]
    pse_tax_id: NotRequired[Optional[str]]
    partner_fee_id: NotRequired[Optional[str]]


class ListPayinsInput(PaginationParams, total=False):
    status: Optional[TransactionStatus]
    customer_id: Optional[str]
    customer_name: str
    bank_account_id: str
    country: Country
    payment_method: PaymentMethod
    network: Network
    token: StablecoinToken


class ListPayinsResponse(TypedDict):
    data: List[Payin]
    pagination: PaginationMetadata


class CreatePayinInput(TypedDict):
    quote_id: NotRequired[str]
    sender_address: NotRequired[str]
    receiver_address: NotRequired[str]
    amount: NotRequired[float]
    token: NotRequired[StablecoinToken]
    network: NotRequired[Network]
    description: NotRequired[Optional[str]]
    payin_quote_id: str


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
    customer_id: str
    id: str
    pix_code: NotRequired[Optional[str]]
    memo_code: NotRequired[Optional[str]]
    clabe: NotRequired[Optional[str]]
    status: str
    manual_execution_status: NotRequired[Optional[Union[ManualExecutionStatus, str]]]
    payin_quote_id: str
    instance_id: str
    tracking_transaction: TrackingTransaction
    tracking_payment: TrackingPayment
    tracking_complete: TrackingComplete
    tracking_partner_fee: NotRequired[TrackingPartnerFee]
    created_at: NotRequired[Optional[str]]
    updated_at: NotRequired[Optional[str]]
    image_url: NotRequired[Optional[str]]
    first_name: NotRequired[Optional[str]]
    last_name: NotRequired[Optional[str]]
    legal_name: NotRequired[Optional[str]]
    type: str
    payment_method: str
    sender_amount: Optional[float]
    receiver_amount: Optional[float]
    token: Union[StablecoinToken, str]
    partner_fee_amount: NotRequired[Optional[float]]
    total_fee_amount: NotRequired[Optional[float]]
    commercial_quotation: Optional[float]
    blindpay_quotation: Optional[float]
    currency: str
    billing_fee: NotRequired[float]
    name: str
    address: NotRequired[Optional[str]]
    network: Union[Network, str]
    blindpay_bank_details: NotRequired[Optional[BankDetails]]
    partner_fee_id: NotRequired[Optional[str]]
    billing_fee_amount: NotRequired[Optional[float]]


class ExportPayinsInput(TypedDict, total=False):
    limit: Optional[str]
    offset: Optional[str]
    status: TransactionStatus


ExportPayinsResponse = List[Payin]


class CreateEvmPayinResponse(TypedDict):
    id: str
    status: Union[TransactionStatus, str]
    pix_code: NotRequired[Optional[str]]
    memo_code: NotRequired[Optional[str]]
    clabe: NotRequired[Optional[str]]
    tracking_complete: Optional[TrackingComplete]
    tracking_payment: Optional[TrackingPayment]
    tracking_transaction: Optional[TrackingTransaction]
    tracking_partner_fee: NotRequired[Optional[TrackingPartnerFee]]
    blindpay_bank_details: BankDetails
    customer_id: NotRequired[Optional[str]]
    receiver_amount: NotRequired[Optional[float]]
    billing_fee_amount: NotRequired[Optional[float]]


_EXPORT_DEPRECATION = (
    "payins.export() calls GET /instances/{instance_id}/export/payins, a route the API does not have, so it "
    "always fails. It will be removed in the next major version."
)


class PayinsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(
        self, params: Optional[ListPayinsInput] = None
    ) -> BlindpayApiResponse[Union[ListPayinsResponse, List[Payin]]]:
        query_string = build_query(params)
        return await self._client.get(f"/instances/{self._instance_id}/payins{query_string}")

    def list_auto_paging(self, params: Optional[ListPayinsInput] = None) -> AsyncIterator[Payin]:
        return async_auto_paging_iter(self.list, params)

    async def get(self, payin_id: str) -> BlindpayApiResponse[Payin]:
        return await self._client.get(f"/instances/{self._instance_id}/payins/{path_param(payin_id)}")

    @deprecated(_EXPORT_DEPRECATION)
    async def export(self, params: ExportPayinsInput) -> BlindpayApiResponse[ExportPayinsResponse]:
        query_string = build_query(params)
        return await self._client.get(f"/instances/{self._instance_id}/export/payins{query_string}")

    async def get_track(
        self, payin_id: str, checkout_token: Optional[str] = None
    ) -> BlindpayApiResponse[GetPayinTrackResponse]:
        """Public tracking endpoint for BlindPay's web and iOS apps; server-side calls get 401 in production.
        Use ``payins.get(payin_id)`` instead. ``checkout_token`` authorises a card-payin checkout page."""
        query_string = build_query({"checkout_token": checkout_token})
        return await self._client.get(f"/e/payins/{path_param(payin_id)}{query_string}")

    async def create_evm(
        self, payin_quote_id: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateEvmPayinResponse]:
        return await self._client.post(
            f"/instances/{self._instance_id}/payins/evm", {"payin_quote_id": payin_quote_id}, options=options
        )


class PayinsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(
        self, params: Optional[ListPayinsInput] = None
    ) -> BlindpayApiResponse[Union[ListPayinsResponse, List[Payin]]]:
        query_string = build_query(params)
        return self._client.get(f"/instances/{self._instance_id}/payins{query_string}")

    def list_auto_paging(self, params: Optional[ListPayinsInput] = None) -> Iterator[Payin]:
        return auto_paging_iter(self.list, params)

    def get(self, payin_id: str) -> BlindpayApiResponse[Payin]:
        return self._client.get(f"/instances/{self._instance_id}/payins/{path_param(payin_id)}")

    def get_track(
        self, payin_id: str, checkout_token: Optional[str] = None
    ) -> BlindpayApiResponse[GetPayinTrackResponse]:
        """Public tracking endpoint for BlindPay's web and iOS apps; server-side calls get 401 in production.
        Use ``payins.get(payin_id)`` instead. ``checkout_token`` authorises a card-payin checkout page."""
        query_string = build_query({"checkout_token": checkout_token})
        return self._client.get(f"/e/payins/{path_param(payin_id)}{query_string}")

    @deprecated(_EXPORT_DEPRECATION)
    def export(self, params: ExportPayinsInput) -> BlindpayApiResponse[ExportPayinsResponse]:
        query_string = build_query(params)
        return self._client.get(f"/instances/{self._instance_id}/export/payins{query_string}")

    def create_evm(
        self, payin_quote_id: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateEvmPayinResponse]:
        return self._client.post(
            f"/instances/{self._instance_id}/payins/evm", {"payin_quote_id": payin_quote_id}, options=options
        )


def create_payins_resource(instance_id: str, client: InternalApiClient) -> PayinsResource:
    return PayinsResource(instance_id, client)


def create_payins_resource_sync(instance_id: str, client: InternalApiClientSync) -> PayinsResourceSync:
    return PayinsResourceSync(instance_id, client)
