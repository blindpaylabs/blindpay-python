from typing import Dict, Optional

from typing_extensions import NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions
from ...types import BlindpayApiResponse


class FeeOptions(TypedDict):
    payin_flat: float
    payin_percentage: float
    payout_flat: float
    payout_percentage: float


class YieldFee(TypedDict):
    """The yield split, in basis points (100 = 1%)."""

    blindpay_share_bps: int
    partner_share_bps: int
    partner_wallets: NotRequired[Dict[str, str]]


# "yield" is a Python keyword, so the wire key lives in a functional TypedDict base.
_FeesYield = TypedDict("_FeesYield", {"yield": NotRequired[Optional[YieldFee]]})


class FeesResponse(_FeesYield):
    ach: Optional[FeeOptions]
    domestic_wire: Optional[FeeOptions]
    pix: Optional[FeeOptions]
    solana: Optional[FeeOptions]
    ted: NotRequired[Optional[FeeOptions]]
    faster_payments: NotRequired[FeeOptions]
    ach_colombia: NotRequired[Optional[FeeOptions]]
    arbitrum: NotRequired[Optional[FeeOptions]]
    base: NotRequired[Optional[FeeOptions]]
    ethereum: NotRequired[Optional[FeeOptions]]
    international_swift: NotRequired[Optional[FeeOptions]]
    pix_safe: NotRequired[Optional[FeeOptions]]
    polygon: NotRequired[Optional[FeeOptions]]
    rtp: NotRequired[Optional[FeeOptions]]
    sepa: NotRequired[Optional[FeeOptions]]
    spei: NotRequired[Optional[FeeOptions]]
    stellar: NotRequired[Optional[FeeOptions]]
    transfers_3: NotRequired[Optional[FeeOptions]]
    tron: NotRequired[Optional[FeeOptions]]
    created_at: NotRequired[Optional[str]]
    id: NotRequired[str]
    instance_id: NotRequired[str]
    updated_at: NotRequired[Optional[str]]


class FeesResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def get(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[FeesResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/billing/fees", options=options)


class FeesResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def get(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[FeesResponse]:
        return self._client.get(f"/instances/{self._instance_id}/billing/fees", options=options)


def create_fees_resource(instance_id: str, client: InternalApiClient) -> FeesResource:
    return FeesResource(instance_id, client)


def create_fees_resource_sync(instance_id: str, client: InternalApiClientSync) -> FeesResourceSync:
    return FeesResourceSync(instance_id, client)
