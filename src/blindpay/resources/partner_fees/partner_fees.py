from typing import List, Optional

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse


class PartnerFee(TypedDict):
    id: str
    instance_id: str
    name: str
    payout_percentage_fee: float
    payout_flat_fee: float
    payin_percentage_fee: float
    payin_flat_fee: float
    evm_wallet_address: str
    stellar_wallet_address: str


ListPartnerFeesResponse = List[PartnerFee]


class CreatePartnerFeeInput(TypedDict):
    virtual_account_set: Optional[bool]
    evm_wallet_address: str
    name: str
    payin_flat_fee: float
    payin_percentage_fee: float
    payout_flat_fee: float
    payout_percentage_fee: float
    stellar_wallet_address: Optional[str]


class CreatePartnerFeeResponse(TypedDict):
    id: str
    instance_id: str
    name: str
    payout_percentage_fee: float
    payout_flat_fee: float
    payin_percentage_fee: float
    payin_flat_fee: float
    evm_wallet_address: Optional[str]
    stellar_wallet_address: Optional[str]


class GetPartnerFeeResponse(TypedDict):
    id: str
    instance_id: str
    evm_wallet_address: str
    name: str
    payin_flat_fee: float
    payin_percentage_fee: float
    payout_flat_fee: float
    payout_percentage_fee: float
    stellar_wallet_address: Optional[str]


class PartnerFeesResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self) -> BlindpayApiResponse[ListPartnerFeesResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/partner-fees")

    async def create(self, data: CreatePartnerFeeInput) -> BlindpayApiResponse[CreatePartnerFeeResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/partner-fees", data)

    async def get(self, id: str) -> BlindpayApiResponse[GetPartnerFeeResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/partner-fees/{id}")

    async def delete(self, id: str) -> BlindpayApiResponse[None]:
        return await self._client.delete(f"/instances/{self._instance_id}/partner-fees/{id}")


class PartnerFeesResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self) -> BlindpayApiResponse[ListPartnerFeesResponse]:
        return self._client.get(f"/instances/{self._instance_id}/partner-fees")

    def create(self, data: CreatePartnerFeeInput) -> BlindpayApiResponse[CreatePartnerFeeResponse]:
        return self._client.post(f"/instances/{self._instance_id}/partner-fees", data)

    def get(self, id: str) -> BlindpayApiResponse[GetPartnerFeeResponse]:
        return self._client.get(f"/instances/{self._instance_id}/partner-fees/{id}")

    def delete(self, id: str) -> BlindpayApiResponse[None]:
        return self._client.delete(f"/instances/{self._instance_id}/partner-fees/{id}")


def create_partner_fees_resource(instance_id: str, client: InternalApiClient) -> PartnerFeesResource:
    return PartnerFeesResource(instance_id, client)


def create_partner_fees_resource_sync(instance_id: str, client: InternalApiClientSync) -> PartnerFeesResourceSync:
    return PartnerFeesResourceSync(instance_id, client)
