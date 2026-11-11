from typing import AsyncIterator, Iterator, List, Literal, Optional, Union

from typing_extensions import NotRequired, TypedDict, deprecated

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, build_query, path_param
from ..._internal.pagination import async_auto_paging_iter, auto_paging_iter
from ...types import (
    AccountClass,
    BankAccountType,
    BlindpayApiResponse,
    Country,
    Currency,
    Network,
    PaginationMetadata,
    PaginationParams,
    Rail,
    SpeiProtocol,
    StablecoinToken,
    TrackingComplete,
    TrackingLiquidity,
    TrackingPartnerFee,
    TrackingPayment,
    TrackingTransaction,
    TransactionDocumentType,
    TransactionStatus,
)

ArgentinaTransfers = Literal["CVU", "CBU", "ALIAS"]


class Payout(TypedDict):
    customer_id: str
    id: str
    status: Union[TransactionStatus, str]
    sender_wallet_address: str
    signed_transaction: Optional[str]
    quote_id: str
    instance_id: str
    tracking_transaction: TrackingTransaction
    tracking_payment: TrackingPayment
    tracking_liquidity: Optional[TrackingLiquidity]
    tracking_complete: TrackingComplete
    tracking_partner_fee: TrackingPartnerFee
    created_at: Optional[str]
    updated_at: Optional[str]
    image_url: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    legal_name: Optional[str]
    network: Union[Network, str]
    token: Union[StablecoinToken, str]
    description: Optional[str]
    sender_amount: Optional[float]
    receiver_amount: Optional[float]
    partner_fee_amount: Optional[float]
    commercial_quotation: Optional[float]
    blindpay_quotation: Optional[float]
    total_fee_amount: Optional[float]
    customer_local_amount: Optional[float]
    currency: Union[Currency, str]  # Excluding "USDT" | "USDB"
    transaction_document_file: Optional[str]
    transaction_document_type: Optional[Union[TransactionDocumentType, str]]
    transaction_document_id: Optional[str]
    name: str
    type: Union[Rail, str]
    pix_key: Optional[str]
    account_number: Optional[str]
    routing_number: Optional[str]
    country: Optional[Union[Country, str]]
    account_class: Optional[Union[AccountClass, str]]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    postal_code: Optional[str]
    account_type: Optional[Union[BankAccountType, str]]
    ach_cop_beneficiary_first_name: Optional[str]
    ach_cop_bank_account: Optional[str]
    ach_cop_bank_code: Optional[str]
    ach_cop_beneficiary_last_name: Optional[str]
    ach_cop_document_id: Optional[str]
    ach_cop_document_type: Optional[str]
    ach_cop_email: Optional[str]
    beneficiary_name: Optional[str]
    spei_clabe: Optional[str]
    spei_protocol: Optional[Union[SpeiProtocol, str]]
    spei_institution_code: Optional[str]
    swift_beneficiary_country: Optional[Union[Country, str]]
    swift_code_bic: Optional[str]
    swift_account_holder_name: Optional[str]
    swift_account_number_iban: Optional[str]
    transfers_account: Optional[str]
    transfers_type: Optional[Union[ArgentinaTransfers, str]]
    has_virtual_account: Optional[bool]
    partner_fee_id: Optional[str]
    ted_bank_code: Optional[str]
    ted_branch_code: Optional[str]
    ted_cpf_cnpj: Optional[str]
    billing_fee_amount: Optional[float]
    cpn_payment_id: Optional[str]
    sender_legal_name: Optional[str]
    faster_payments_beneficiary_country: NotRequired[Optional[Union[Country, str]]]
    sepa_beneficiary_country: NotRequired[Optional[Union[Country, str]]]
    bank_account_id: NotRequired[Optional[str]]
    faster_payments_account_number: NotRequired[Optional[str]]
    faster_payments_beneficiary_address_line_1: NotRequired[Optional[str]]
    faster_payments_beneficiary_city: NotRequired[Optional[str]]
    faster_payments_beneficiary_legal_name: NotRequired[Optional[str]]
    faster_payments_beneficiary_postal_code: NotRequired[Optional[str]]
    faster_payments_sort_code: NotRequired[Optional[str]]
    payable_id: NotRequired[Optional[str]]
    sepa_beneficiary_address_line_1: NotRequired[Optional[str]]
    sepa_beneficiary_city: NotRequired[Optional[str]]
    sepa_beneficiary_legal_name: NotRequired[Optional[str]]
    sepa_beneficiary_postal_code: NotRequired[Optional[str]]
    sepa_iban: NotRequired[Optional[str]]


class ListPayoutsInput(PaginationParams, total=False):
    customer_id: str


class ListPayoutsResponse(TypedDict):
    data: List[Payout]
    pagination: PaginationMetadata


class ExportPayoutsInput(TypedDict, total=False):
    limit: str
    offset: str


ExportPayoutsResponse = List[Payout]


class AuthorizeStellarTokenInput(TypedDict):
    quote_id: str
    sender_wallet_address: str
    wallet_id: NotRequired[str]


class AuthorizeStellarTokenResponse(TypedDict):
    transaction_hash: str


class CreateStellarPayoutInput(TypedDict):
    quote_id: str
    sender_wallet_address: str
    signed_transaction: Optional[str]
    wallet_id: NotRequired[str]


class CreateStellarPayoutResponse(TypedDict):
    id: str
    status: Union[TransactionStatus, str]
    sender_wallet_address: str
    tracking_complete: Optional[TrackingComplete]
    tracking_payment: Optional[TrackingPayment]
    tracking_transaction: Optional[TrackingTransaction]
    tracking_partner_fee: Optional[TrackingPartnerFee]
    tracking_liquidity: Optional[TrackingLiquidity]
    customer_id: Optional[str]
    payable_id: NotRequired[Optional[str]]


class CreateEvmPayoutInput(TypedDict):
    quote_id: str
    sender_wallet_address: str
    wallet_id: NotRequired[str]


class CreateEvmPayoutResponse(TypedDict):
    id: str
    status: Union[TransactionStatus, str]
    sender_wallet_address: str
    tracking_complete: Optional[TrackingComplete]
    tracking_payment: Optional[TrackingPayment]
    tracking_transaction: Optional[TrackingTransaction]
    tracking_partner_fee: Optional[TrackingPartnerFee]
    tracking_liquidity: Optional[TrackingLiquidity]
    customer_id: Optional[str]
    payable_id: NotRequired[Optional[str]]


class CreateSolanaPayoutInput(TypedDict):
    quote_id: str
    sender_wallet_address: str
    wallet_id: NotRequired[str]


class CreateSolanaPayoutResponse(TypedDict):
    id: str
    status: Union[TransactionStatus, str]
    sender_wallet_address: str
    tracking_complete: Optional[TrackingComplete]
    tracking_payment: Optional[TrackingPayment]
    tracking_transaction: Optional[TrackingTransaction]
    tracking_partner_fee: Optional[TrackingPartnerFee]
    tracking_liquidity: Optional[TrackingLiquidity]
    customer_id: Optional[str]
    payable_id: NotRequired[Optional[str]]


class SubmitPayoutDocumentsInput(TypedDict):
    payout_id: str
    transaction_document_type: TransactionDocumentType
    transaction_document_id: str
    transaction_document_file: str
    description: Optional[str]


class SubmitPayoutDocumentsResponse(TypedDict):
    id: str


_EXPORT_DEPRECATION = (
    "payouts.export() calls GET /instances/{instance_id}/export/payouts, a route the API does not have, so it "
    "always fails. It will be removed in the next major version."
)


class PayoutsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(
        self, params: Optional[ListPayoutsInput] = None
    ) -> BlindpayApiResponse[Union[ListPayoutsResponse, List[Payout]]]:
        query_string = build_query(params)
        return await self._client.get(f"/instances/{self._instance_id}/payouts{query_string}")

    def list_auto_paging(self, params: Optional[ListPayoutsInput] = None) -> AsyncIterator[Payout]:
        return async_auto_paging_iter(self.list, params)

    @deprecated(_EXPORT_DEPRECATION)
    async def export(self, params: Optional[ExportPayoutsInput] = None) -> BlindpayApiResponse[ExportPayoutsResponse]:
        query_string = build_query(params)
        return await self._client.get(f"/instances/{self._instance_id}/export/payouts{query_string}")

    async def get(self, payout_id: str) -> BlindpayApiResponse[Payout]:
        return await self._client.get(f"/instances/{self._instance_id}/payouts/{path_param(payout_id)}")

    async def get_track(self, payout_id: str) -> BlindpayApiResponse[Payout]:
        return await self._client.get(f"/e/payouts/{path_param(payout_id)}")

    async def authorize_stellar_token(
        self, data: AuthorizeStellarTokenInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[AuthorizeStellarTokenResponse]:
        return await self._client.post(
            f"/instances/{self._instance_id}/payouts/stellar/authorize", data, options=options
        )

    async def create_stellar(
        self, data: CreateStellarPayoutInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateStellarPayoutResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/payouts/stellar", data, options=options)

    async def create_evm(
        self, data: CreateEvmPayoutInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateEvmPayoutResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/payouts/evm", data, options=options)

    async def create_solana(
        self, data: CreateSolanaPayoutInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateSolanaPayoutResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/payouts/solana", data, options=options)

    async def submit_documents(
        self, data: SubmitPayoutDocumentsInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[SubmitPayoutDocumentsResponse]:
        payout_id = data["payout_id"]
        payload = {k: v for k, v in data.items() if k != "payout_id"}
        return await self._client.post(
            f"/instances/{self._instance_id}/payouts/{path_param(payout_id)}/documents", payload, options=options
        )


class PayoutsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(
        self, params: Optional[ListPayoutsInput] = None
    ) -> BlindpayApiResponse[Union[ListPayoutsResponse, List[Payout]]]:
        query_string = build_query(params)
        return self._client.get(f"/instances/{self._instance_id}/payouts{query_string}")

    def list_auto_paging(self, params: Optional[ListPayoutsInput] = None) -> Iterator[Payout]:
        return auto_paging_iter(self.list, params)

    @deprecated(_EXPORT_DEPRECATION)
    def export(self, params: Optional[ExportPayoutsInput] = None) -> BlindpayApiResponse[ExportPayoutsResponse]:
        query_string = build_query(params)
        return self._client.get(f"/instances/{self._instance_id}/export/payouts{query_string}")

    def get(self, payout_id: str) -> BlindpayApiResponse[Payout]:
        return self._client.get(f"/instances/{self._instance_id}/payouts/{path_param(payout_id)}")

    def get_track(self, payout_id: str) -> BlindpayApiResponse[Payout]:
        return self._client.get(f"/e/payouts/{path_param(payout_id)}")

    def authorize_stellar_token(
        self, data: AuthorizeStellarTokenInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[AuthorizeStellarTokenResponse]:
        return self._client.post(f"/instances/{self._instance_id}/payouts/stellar/authorize", data, options=options)

    def create_stellar(
        self, data: CreateStellarPayoutInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateStellarPayoutResponse]:
        return self._client.post(f"/instances/{self._instance_id}/payouts/stellar", data, options=options)

    def create_evm(
        self, data: CreateEvmPayoutInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateEvmPayoutResponse]:
        return self._client.post(f"/instances/{self._instance_id}/payouts/evm", data, options=options)

    def create_solana(
        self, data: CreateSolanaPayoutInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateSolanaPayoutResponse]:
        return self._client.post(f"/instances/{self._instance_id}/payouts/solana", data, options=options)

    def submit_documents(
        self, data: SubmitPayoutDocumentsInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[SubmitPayoutDocumentsResponse]:
        payout_id = data["payout_id"]
        payload = {k: v for k, v in data.items() if k != "payout_id"}
        return self._client.post(
            f"/instances/{self._instance_id}/payouts/{path_param(payout_id)}/documents", payload, options=options
        )


def create_payouts_resource(instance_id: str, client: InternalApiClient) -> PayoutsResource:
    return PayoutsResource(instance_id, client)


def create_payouts_resource_sync(instance_id: str, client: InternalApiClientSync) -> PayoutsResourceSync:
    return PayoutsResourceSync(instance_id, client)
