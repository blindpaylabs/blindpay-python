from typing import Any, Dict, List, Optional

from typing_extensions import NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions
from ...types import (
    BlindpayApiResponse,
    Currency,
    CurrencyType,
    Network,
    StablecoinToken,
    TransactionDocumentType,
)


class ContractNetwork(TypedDict):
    name: str
    chainId: int


class Contract(TypedDict):
    abi: List[Dict[str, Any]]
    address: str
    functionName: str
    blindpayContractAddress: str
    amount: str
    network: ContractNetwork


class CreateQuoteInput(TypedDict):
    bank_account_id: NotRequired[str]
    currency_type: NotRequired[CurrencyType]
    network: Optional[Network]
    request_amount: NotRequired[float]
    token: Optional[StablecoinToken]
    cover_fees: NotRequired[Optional[bool]]
    description: NotRequired[Optional[str]]
    partner_fee_id: NotRequired[Optional[str]]
    transaction_document_file: Optional[str]
    transaction_document_id: Optional[str]
    transaction_document_type: TransactionDocumentType
    refund_wallet_address: NotRequired[Optional[str]]
    payable_id: NotRequired[Optional[str]]


class CreateQuoteResponse(TypedDict):
    id: str
    expires_at: Optional[int]
    commercial_quotation: Optional[float]
    blindpay_quotation: Optional[float]
    receiver_amount: Optional[float]
    sender_amount: Optional[float]
    partner_fee_amount: NotRequired[Optional[float]]
    flat_fee: NotRequired[Optional[float]]
    contract: NotRequired[Optional[Contract]]
    customer_local_amount: NotRequired[Optional[float]]
    description: NotRequired[Optional[str]]


class GetFxRateInput(TypedDict):
    currency_type: CurrencyType
    from_currency: Currency  # 'from' is reserved in Python
    to: Currency
    request_amount: float


class GetFxRateResponse(TypedDict):
    commercial_quotation: Optional[float]
    blindpay_quotation: Optional[float]
    result_amount: float
    instance_flat_fee: NotRequired[Optional[float]]
    instance_percentage_fee: float


class QuotesResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def create(
        self, data: CreateQuoteInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateQuoteResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/quotes", data, options=options)

    async def get_fx_rate(
        self, data: GetFxRateInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[GetFxRateResponse]:
        payload = {
            "currency_type": data["currency_type"],
            "from": data["from_currency"],
            "to": data["to"],
            "request_amount": data["request_amount"],
        }
        return await self._client.post(f"/instances/{self._instance_id}/quotes/fx", payload, options=options)


class QuotesResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def create(
        self, data: CreateQuoteInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateQuoteResponse]:
        return self._client.post(f"/instances/{self._instance_id}/quotes", data, options=options)

    def get_fx_rate(
        self, data: GetFxRateInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[GetFxRateResponse]:
        payload = {
            "currency_type": data["currency_type"],
            "from": data["from_currency"],
            "to": data["to"],
            "request_amount": data["request_amount"],
        }
        return self._client.post(f"/instances/{self._instance_id}/quotes/fx", payload, options=options)


def create_quotes_resource(instance_id: str, client: InternalApiClient) -> QuotesResource:
    return QuotesResource(instance_id, client)


def create_quotes_resource_sync(instance_id: str, client: InternalApiClientSync) -> QuotesResourceSync:
    return QuotesResourceSync(instance_id, client)
