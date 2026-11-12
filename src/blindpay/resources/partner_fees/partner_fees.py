from typing import List, Optional, Union

from typing_extensions import NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, path_param
from ...types import BlindpayApiResponse


class PartnerFee(TypedDict):
    id: str
    instance_id: str
    name: str
    payout_percentage_fee: float
    payout_flat_fee: float
    payin_percentage_fee: float
    payin_flat_fee: float
    evm_wallet_address: NotRequired[str]
    stellar_wallet_address: NotRequired[str]


ListPartnerFeesResponse = List[PartnerFee]


class CreatePartnerFeeInput(TypedDict):
    virtual_account_set: NotRequired[Optional[bool]]
    evm_wallet_address: NotRequired[Optional[str]]
    """Not in the public spec; optional, and kept only so existing calls still type-check."""
    name: str
    payin_flat_fee: Union[int, float]
    """Integer cents (1000 = 10.00)."""
    payin_percentage_fee: Union[int, float]
    """Integer basis points (100 = 1%)."""
    payout_flat_fee: Union[int, float]
    """Integer cents (1000 = 10.00)."""
    payout_percentage_fee: Union[int, float]
    """Integer basis points (100 = 1%)."""
    stellar_wallet_address: NotRequired[Optional[str]]
    """Not in the public spec; optional, and kept only so existing calls still type-check."""


class CreatePartnerFeeResponse(TypedDict):
    id: str
    instance_id: str
    name: str
    payout_percentage_fee: float
    payout_flat_fee: float
    payin_percentage_fee: float
    payin_flat_fee: float
    evm_wallet_address: NotRequired[Optional[str]]
    stellar_wallet_address: NotRequired[Optional[str]]


class GetPartnerFeeResponse(TypedDict):
    id: str
    instance_id: str
    evm_wallet_address: NotRequired[str]
    name: str
    payin_flat_fee: float
    payin_percentage_fee: float
    payout_flat_fee: float
    payout_percentage_fee: float
    stellar_wallet_address: NotRequired[Optional[str]]


class PartnerFeesResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[ListPartnerFeesResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/partner-fees", options=options)

    async def create(
        self, data: CreatePartnerFeeInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreatePartnerFeeResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/partner-fees", data, options=options)

    async def get(
        self, id: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[GetPartnerFeeResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/partner-fees/{path_param(id)}", options=options)

    async def delete(self, id: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
        return await self._client.delete(
            f"/instances/{self._instance_id}/partner-fees/{path_param(id)}", options=options
        )


class PartnerFeesResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[ListPartnerFeesResponse]:
        return self._client.get(f"/instances/{self._instance_id}/partner-fees", options=options)

    def create(
        self, data: CreatePartnerFeeInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreatePartnerFeeResponse]:
        return self._client.post(f"/instances/{self._instance_id}/partner-fees", data, options=options)

    def get(self, id: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[GetPartnerFeeResponse]:
        return self._client.get(f"/instances/{self._instance_id}/partner-fees/{path_param(id)}", options=options)

    def delete(self, id: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
        return self._client.delete(f"/instances/{self._instance_id}/partner-fees/{path_param(id)}", options=options)


def create_partner_fees_resource(instance_id: str, client: InternalApiClient) -> PartnerFeesResource:
    return PartnerFeesResource(instance_id, client)


def create_partner_fees_resource_sync(instance_id: str, client: InternalApiClientSync) -> PartnerFeesResourceSync:
    return PartnerFeesResourceSync(instance_id, client)
