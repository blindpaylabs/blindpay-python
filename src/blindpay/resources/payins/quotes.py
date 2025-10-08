from typing import List, Literal, Optional

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import (
    BlindpayApiResponse,
    Currency,
    CurrencyType,
    StablecoinToken,
)

PaymentMethod = Literal["ach", "wire", "pix", "spei"]


class PayerRules(TypedDict, total=False):
    pix_allowed_tax_ids: List[str]


class CreatePayinQuoteInput(TypedDict):
    blockchain_wallet_id: str
    currency_type: CurrencyType
    payment_method: PaymentMethod
    request_amount: float
    token: StablecoinToken
    cover_fees: bool
    partner_fee_id: Optional[str]
    payer_rules: PayerRules


class CreatePayinQuoteResponse(TypedDict):
    id: str
    expires_at: int
    commercial_quotation: float
    blindpay_quotation: float
    receiver_amount: float
    sender_amount: float
    partner_fee_amount: Optional[float]
    flat_fee: Optional[float]


class GetPayinFxRateInput(TypedDict):
    currency_type: CurrencyType
    from_currency: Currency  # 'from' is a reserved keyword in Python
    to: Currency
    request_amount: float


class GetPayinFxRateResponse(TypedDict):
    commercial_quotation: float
    blindpay_quotation: float
    result_amount: float
    instance_flat_fee: float
    instance_percentage_fee: float


class PayinQuotesResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def create(self, data: CreatePayinQuoteInput) -> BlindpayApiResponse[CreatePayinQuoteResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/payin-quotes", data)

    async def get_fx_rate(self, data: GetPayinFxRateInput) -> BlindpayApiResponse[GetPayinFxRateResponse]:
        # Convert 'from_currency' back to 'from' for API
        payload = {
            "currency_type": data["currency_type"],
            "from": data["from_currency"],
            "to": data["to"],
            "request_amount": data["request_amount"],
        }
        return await self._client.post(f"/instances/{self._instance_id}/payin-quotes/fx", payload)


class PayinQuotesResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def create(self, data: CreatePayinQuoteInput) -> BlindpayApiResponse[CreatePayinQuoteResponse]:
        return self._client.post(f"/instances/{self._instance_id}/payin-quotes", data)

    def get_fx_rate(self, data: GetPayinFxRateInput) -> BlindpayApiResponse[GetPayinFxRateResponse]:
        # Convert 'from_currency' back to 'from' for API
        payload = {
            "currency_type": data["currency_type"],
            "from": data["from_currency"],
            "to": data["to"],
            "request_amount": data["request_amount"],
        }
        return self._client.post(f"/instances/{self._instance_id}/payin-quotes/fx", payload)


def create_payin_quotes_resource(instance_id: str, client: InternalApiClient) -> PayinQuotesResource:
    return PayinQuotesResource(instance_id, client)


def create_payin_quotes_resource_sync(instance_id: str, client: InternalApiClientSync) -> PayinQuotesResourceSync:
    return PayinQuotesResourceSync(instance_id, client)
