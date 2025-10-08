from typing import Any, Dict, List, Optional

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
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
    bank_account_id: str
    currency_type: CurrencyType
    network: Optional[Network]
    request_amount: float
    token: Optional[StablecoinToken]
    cover_fees: Optional[bool]
    description: Optional[str]
    partner_fee_id: Optional[str]
    transaction_document_file: Optional[str]
    transaction_document_id: Optional[str]
    transaction_document_type: TransactionDocumentType


class CreateQuoteResponse(TypedDict):
    id: str
    expires_at: int
    commercial_quotation: float
    blindpay_quotation: float
    receiver_amount: float
    sender_amount: float
    partner_fee_amount: float
    flat_fee: float
    contract: Contract
    receiver_local_amount: float
    description: str


class GetFxRateInput(TypedDict):
    currency_type: CurrencyType
    from_currency: Currency  # 'from' is reserved in Python
    to: Currency
    request_amount: float


class GetFxRateResponse(TypedDict):
    commercial_quotation: float
    blindpay_quotation: float
    result_amount: float
    instance_flat_fee: float
    instance_percentage_fee: float


class QuotesResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def create(self, data: CreateQuoteInput) -> BlindpayApiResponse[CreateQuoteResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/quotes", data)

    async def get_fx_rate(self, data: GetFxRateInput) -> BlindpayApiResponse[GetFxRateResponse]:
        payload = {
            "currency_type": data["currency_type"],
            "from": data["from_currency"],
            "to": data["to"],
            "request_amount": data["request_amount"],
        }
        return await self._client.post(f"/instances/{self._instance_id}/quotes/fx", payload)


class QuotesResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def create(self, data: CreateQuoteInput) -> BlindpayApiResponse[CreateQuoteResponse]:
        return self._client.post(f"/instances/{self._instance_id}/quotes", data)

    def get_fx_rate(self, data: GetFxRateInput) -> BlindpayApiResponse[GetFxRateResponse]:
        payload = {
            "currency_type": data["currency_type"],
            "from": data["from_currency"],
            "to": data["to"],
            "request_amount": data["request_amount"],
        }
        return self._client.post(f"/instances/{self._instance_id}/quotes/fx", payload)


def create_quotes_resource(instance_id: str, client: InternalApiClient) -> QuotesResource:
    return QuotesResource(instance_id, client)


def create_quotes_resource_sync(instance_id: str, client: InternalApiClientSync) -> QuotesResourceSync:
    return QuotesResourceSync(instance_id, client)
