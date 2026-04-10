from typing import Optional

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse


class FeeOptions(TypedDict):
    payin_flat: float
    payin_percentage: float
    payout_flat: float
    payout_percentage: float


class FeesResponse(TypedDict):
    ach: Optional[FeeOptions]
    domestic_wire: Optional[FeeOptions]
    pix: Optional[FeeOptions]
    solana: Optional[FeeOptions]


class FeesResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def get(self) -> BlindpayApiResponse[FeesResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/billing/fees")


class FeesResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def get(self) -> BlindpayApiResponse[FeesResponse]:
        return self._client.get(f"/instances/{self._instance_id}/billing/fees")


def create_fees_resource(instance_id: str, client: InternalApiClient) -> FeesResource:
    return FeesResource(instance_id, client)


def create_fees_resource_sync(instance_id: str, client: InternalApiClientSync) -> FeesResourceSync:
    return FeesResourceSync(instance_id, client)
