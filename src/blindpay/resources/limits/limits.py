from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse


class PayinLimit(TypedDict):
    daily: float
    monthly: float


class PayoutLimit(TypedDict):
    daily: float
    monthly: float


class CustomerLimits(TypedDict):
    payin: PayinLimit
    payout: PayoutLimit


class GetCustomerLimitsResponse(TypedDict):
    limits: CustomerLimits


# --- Async resource ---


class LimitsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def get_customer_limits(self, customer_id: str) -> BlindpayApiResponse[GetCustomerLimitsResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/limits/customers/{customer_id}")


# --- Sync resource ---


class LimitsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def get_customer_limits(self, customer_id: str) -> BlindpayApiResponse[GetCustomerLimitsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/limits/customers/{customer_id}")


# --- Factory functions ---


def create_limits_resource(instance_id: str, client: InternalApiClient) -> LimitsResource:
    return LimitsResource(instance_id, client)


def create_limits_resource_sync(instance_id: str, client: InternalApiClientSync) -> LimitsResourceSync:
    return LimitsResourceSync(instance_id, client)
