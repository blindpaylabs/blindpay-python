from typing import Dict, List, Literal, Optional

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse

SandboxStatus = Literal["active", "inactive"]


class SandboxItem(TypedDict):
    id: str
    name: str
    status: SandboxStatus
    metadata: Optional[Dict[str, str]]
    created_at: Optional[str]
    updated_at: Optional[str]


class CreateSandboxInput(TypedDict, total=False):
    name: str
    metadata: Dict[str, str]


class CreateSandboxResponse(TypedDict):
    id: str
    name: str
    status: SandboxStatus
    metadata: Optional[Dict[str, str]]


class ListSandboxResponse(TypedDict):
    data: List[SandboxItem]


class _UpdateSandboxInputRequired(TypedDict):
    sandbox_id: str


class UpdateSandboxInput(_UpdateSandboxInputRequired, total=False):
    name: str
    metadata: Dict[str, str]


# --- Async resource ---


class SandboxResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self) -> BlindpayApiResponse[List[SandboxItem]]:
        return await self._client.get(f"/instances/{self._instance_id}/sandbox")

    async def get(self, sandbox_id: str) -> BlindpayApiResponse[SandboxItem]:
        return await self._client.get(f"/instances/{self._instance_id}/sandbox/{sandbox_id}")

    async def create(self, data: CreateSandboxInput) -> BlindpayApiResponse[CreateSandboxResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/sandbox", data)

    async def update(self, data: UpdateSandboxInput) -> BlindpayApiResponse[SandboxItem]:
        sandbox_id = data["sandbox_id"]
        payload = {k: v for k, v in data.items() if k != "sandbox_id"}
        return await self._client.patch(f"/instances/{self._instance_id}/sandbox/{sandbox_id}", payload)

    async def delete(self, sandbox_id: str) -> BlindpayApiResponse[None]:
        return await self._client.delete(f"/instances/{self._instance_id}/sandbox/{sandbox_id}")


# --- Sync resource ---


class SandboxResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self) -> BlindpayApiResponse[List[SandboxItem]]:
        return self._client.get(f"/instances/{self._instance_id}/sandbox")

    def get(self, sandbox_id: str) -> BlindpayApiResponse[SandboxItem]:
        return self._client.get(f"/instances/{self._instance_id}/sandbox/{sandbox_id}")

    def create(self, data: CreateSandboxInput) -> BlindpayApiResponse[CreateSandboxResponse]:
        return self._client.post(f"/instances/{self._instance_id}/sandbox", data)

    def update(self, data: UpdateSandboxInput) -> BlindpayApiResponse[SandboxItem]:
        sandbox_id = data["sandbox_id"]
        payload = {k: v for k, v in data.items() if k != "sandbox_id"}
        return self._client.patch(f"/instances/{self._instance_id}/sandbox/{sandbox_id}", payload)

    def delete(self, sandbox_id: str) -> BlindpayApiResponse[None]:
        return self._client.delete(f"/instances/{self._instance_id}/sandbox/{sandbox_id}")


# --- Factory functions ---


def create_sandbox_resource(instance_id: str, client: InternalApiClient) -> SandboxResource:
    return SandboxResource(instance_id, client)


def create_sandbox_resource_sync(instance_id: str, client: InternalApiClientSync) -> SandboxResourceSync:
    return SandboxResourceSync(instance_id, client)
