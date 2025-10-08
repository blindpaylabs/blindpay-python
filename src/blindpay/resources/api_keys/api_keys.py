from typing import List, Optional

from typing_extensions import Literal, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse

Permission = Literal["full_access"]


class ApiKey(TypedDict):
    id: str
    name: str
    permission: Permission
    token: str
    ip_whitelist: Optional[List[str]]
    unkey_id: str
    last_used_at: Optional[str]
    instance_id: str
    created_at: str
    updated_at: str


ListApiKeysResponse = List[ApiKey]


class CreateApiKeyInput(TypedDict):
    name: str
    permission: Literal["full_access"]
    ip_whitelist: Optional[List[str]]


class CreateApiKeyResponse(TypedDict):
    id: str
    token: str


GetApiKeyResponse = ApiKey


class ApiKeysResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self) -> BlindpayApiResponse[ListApiKeysResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/api-keys")

    async def create(self, data: CreateApiKeyInput) -> BlindpayApiResponse[CreateApiKeyResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/api-keys", data)

    async def get(self, id: str) -> BlindpayApiResponse[GetApiKeyResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/api-keys/{id}")

    async def delete(self, id: str) -> BlindpayApiResponse[None]:
        return await self._client.delete(f"/instances/{self._instance_id}/api-keys/{id}")


class ApiKeysResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self) -> BlindpayApiResponse[ListApiKeysResponse]:
        return self._client.get(f"/instances/{self._instance_id}/api-keys")

    def create(self, data: CreateApiKeyInput) -> BlindpayApiResponse[CreateApiKeyResponse]:
        return self._client.post(f"/instances/{self._instance_id}/api-keys", data)

    def get(self, id: str) -> BlindpayApiResponse[GetApiKeyResponse]:
        return self._client.get(f"/instances/{self._instance_id}/api-keys/{id}")

    def delete(self, id: str) -> BlindpayApiResponse[None]:
        return self._client.delete(f"/instances/{self._instance_id}/api-keys/{id}")


def create_api_keys_resource(instance_id: str, client: InternalApiClient) -> ApiKeysResource:
    return ApiKeysResource(instance_id, client)


def create_api_keys_resource_sync(instance_id: str, client: InternalApiClientSync) -> ApiKeysResourceSync:
    return ApiKeysResourceSync(instance_id, client)
