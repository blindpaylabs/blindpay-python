from typing import List, Literal, Optional
from urllib.parse import urlencode

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
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
    receiver_id: str
    id: str
    status: TransactionStatus
    sender_wallet_address: str
    signed_transaction: str
    quote_id: str
    instance_id: str
    tracking_transaction: TrackingTransaction
    tracking_payment: TrackingPayment
    tracking_liquidity: TrackingLiquidity
    tracking_complete: TrackingComplete
    tracking_partner_fee: TrackingPartnerFee
    created_at: str
    updated_at: str
    image_url: str
    first_name: str
    last_name: str
    legal_name: str
    network: Network
    token: StablecoinToken
    description: str
    sender_amount: float
    receiver_amount: float
    partner_fee_amount: float
    commercial_quotation: float
    blindpay_quotation: float
    total_fee_amount: float
    receiver_local_amount: float
    currency: Currency  # Excluding "USDT" | "USDB"
    transaction_document_file: str
    transaction_document_type: TransactionDocumentType
    transaction_document_id: str
    name: str
    type: Rail
    pix_key: Optional[str]
    account_number: Optional[str]
    routing_number: Optional[str]
    country: Optional[Country]
    account_class: Optional[AccountClass]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    postal_code: Optional[str]
    account_type: Optional[BankAccountType]
    ach_cop_beneficiary_first_name: Optional[str]
    ach_cop_bank_account: Optional[str]
    ach_cop_bank_code: Optional[str]
    ach_cop_beneficiary_last_name: Optional[str]
    ach_cop_document_id: Optional[str]
    ach_cop_document_type: Optional[str]
    ach_cop_email: Optional[str]
    beneficiary_name: Optional[str]
    spei_clabe: Optional[str]
    spei_protocol: Optional[SpeiProtocol]
    spei_institution_code: Optional[str]
    swift_beneficiary_country: Optional[Country]
    swift_code_bic: Optional[str]
    swift_account_holder_name: Optional[str]
    swift_account_number_iban: Optional[str]
    transfers_account: Optional[str]
    transfers_type: ArgentinaTransfers
    has_virtual_account: bool


class ListPayoutsInput(PaginationParams, total=False):
    receiver_id: str


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


class AuthorizeStellarTokenResponse(TypedDict):
    transaction_hash: str


class CreateStellarPayoutInput(TypedDict):
    quote_id: str
    sender_wallet_address: str
    signed_transaction: Optional[str]


class CreateStellarPayoutResponse(TypedDict):
    id: str
    status: TransactionStatus
    sender_wallet_address: str
    tracking_complete: Optional[TrackingComplete]
    tracking_payment: Optional[TrackingPayment]
    tracking_transaction: Optional[TrackingTransaction]
    tracking_partner_fee: Optional[TrackingPartnerFee]
    tracking_liquidity: Optional[TrackingLiquidity]
    receiver_id: str


class CreateEvmPayoutInput(TypedDict):
    quote_id: str
    sender_wallet_address: str


class CreateEvmPayoutResponse(TypedDict):
    id: str
    status: TransactionStatus
    sender_wallet_address: str
    tracking_complete: Optional[TrackingComplete]
    tracking_payment: Optional[TrackingPayment]
    tracking_transaction: Optional[TrackingTransaction]
    tracking_partner_fee: Optional[TrackingPartnerFee]
    tracking_liquidity: Optional[TrackingLiquidity]
    receiver_id: str


class PayoutsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, params: Optional[ListPayoutsInput] = None) -> BlindpayApiResponse[ListPayoutsResponse]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return await self._client.get(f"/instances/{self._instance_id}/payouts{query_string}")

    async def export(self, params: Optional[ExportPayoutsInput] = None) -> BlindpayApiResponse[ExportPayoutsResponse]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return await self._client.get(f"/instances/{self._instance_id}/export/payouts{query_string}")

    async def get(self, payout_id: str) -> BlindpayApiResponse[Payout]:
        return await self._client.get(f"/instances/{self._instance_id}/payouts/{payout_id}")

    async def get_track(self, payout_id: str) -> BlindpayApiResponse[Payout]:
        return await self._client.get(f"/e/payouts/{payout_id}")

    async def authorize_stellar_token(
        self, data: AuthorizeStellarTokenInput
    ) -> BlindpayApiResponse[AuthorizeStellarTokenResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/payouts/stellar/authorize", data)

    async def create_stellar(self, data: CreateStellarPayoutInput) -> BlindpayApiResponse[CreateStellarPayoutResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/payouts/stellar", data)

    async def create_evm(self, data: CreateEvmPayoutInput) -> BlindpayApiResponse[CreateEvmPayoutResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/payouts/evm", data)


class PayoutsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, params: Optional[ListPayoutsInput] = None) -> BlindpayApiResponse[ListPayoutsResponse]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return self._client.get(f"/instances/{self._instance_id}/payouts{query_string}")

    def export(self, params: Optional[ExportPayoutsInput] = None) -> BlindpayApiResponse[ExportPayoutsResponse]:
        query_string = ""
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = f"?{urlencode(filtered_params)}"
        return self._client.get(f"/instances/{self._instance_id}/export/payouts{query_string}")

    def get(self, payout_id: str) -> BlindpayApiResponse[Payout]:
        return self._client.get(f"/instances/{self._instance_id}/payouts/{payout_id}")

    def get_track(self, payout_id: str) -> BlindpayApiResponse[Payout]:
        return self._client.get(f"/e/payouts/{payout_id}")

    def authorize_stellar_token(
        self, data: AuthorizeStellarTokenInput
    ) -> BlindpayApiResponse[AuthorizeStellarTokenResponse]:
        return self._client.post(f"/instances/{self._instance_id}/payouts/stellar/authorize", data)

    def create_stellar(self, data: CreateStellarPayoutInput) -> BlindpayApiResponse[CreateStellarPayoutResponse]:
        return self._client.post(f"/instances/{self._instance_id}/payouts/stellar", data)

    def create_evm(self, data: CreateEvmPayoutInput) -> BlindpayApiResponse[CreateEvmPayoutResponse]:
        return self._client.post(f"/instances/{self._instance_id}/payouts/evm", data)


def create_payouts_resource(instance_id: str, client: InternalApiClient) -> PayoutsResource:
    return PayoutsResource(instance_id, client)


def create_payouts_resource_sync(instance_id: str, client: InternalApiClientSync) -> PayoutsResourceSync:
    return PayoutsResourceSync(instance_id, client)
