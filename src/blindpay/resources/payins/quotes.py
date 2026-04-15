from typing import List, Optional, Union

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import (
    BlindpayApiResponse,
    Currency,
    CurrencyType,
    PaymentMethod,
    StablecoinToken,
)


class PayerRules(TypedDict, total=False):
    pix_allowed_tax_ids: List[str]


class _CreatePayinQuoteInputRequired(TypedDict):
    currency_type: CurrencyType
    payment_method: PaymentMethod
    request_amount: int
    token: StablecoinToken


class CreatePayinQuoteInput(_CreatePayinQuoteInputRequired, total=False):
    blockchain_wallet_id: Optional[str]
    wallet_id: Optional[str]
    cover_fees: Optional[bool]
    partner_fee_id: Optional[str]
    payer_rules: Optional[PayerRules]
    is_otc: Optional[bool]


class CreatePayinQuoteResponse(TypedDict):
    id: str
    expires_at: Optional[float]
    commercial_quotation: Optional[float]
    blindpay_quotation: Optional[float]
    receiver_amount: Optional[float]
    sender_amount: Optional[float]
    partner_fee_amount: Optional[float]
    flat_fee: Optional[float]
    billing_fee_amount: Optional[float]
    is_otc: Optional[bool]


class GetPayinFxRateInput(TypedDict):
    currency_type: CurrencyType
    from_currency: Union[StablecoinToken, Currency]  # 'from' is a reserved keyword in Python
    to: Union[StablecoinToken, Currency]
    request_amount: int


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
