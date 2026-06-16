from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse


class MigrateInstanceOwnershipInput(TypedDict):
    user_id: str


class MigrateInstanceOwnershipResponse(TypedDict):
    success: bool


# --- Async resource ---


class OwnershipResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def migrate(
        self, data: MigrateInstanceOwnershipInput
    ) -> BlindpayApiResponse[MigrateInstanceOwnershipResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/ownership", data)


# --- Sync resource ---


class OwnershipResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def migrate(self, data: MigrateInstanceOwnershipInput) -> BlindpayApiResponse[MigrateInstanceOwnershipResponse]:
        return self._client.post(f"/instances/{self._instance_id}/ownership", data)


# --- Factory functions ---


def create_ownership_resource(instance_id: str, client: InternalApiClient) -> OwnershipResource:
    return OwnershipResource(instance_id, client)


def create_ownership_resource_sync(instance_id: str, client: InternalApiClientSync) -> OwnershipResourceSync:
    return OwnershipResourceSync(instance_id, client)
