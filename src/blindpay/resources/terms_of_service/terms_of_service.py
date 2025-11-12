from typing_extensions import Optional, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse


class InitiateInput(TypedDict):
    idempotency_key: str
    receiver_id: Optional[str]
    redirect_url: Optional[str]


class InitiateResponse(TypedDict):
    url: str


class TermsOfServiceResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def initiate(self, data: InitiateInput) -> BlindpayApiResponse[InitiateResponse]:
        return await self._client.post(f"/e/instances/{self._instance_id}/tos", data)


class TermsOfServiceResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def initiate(self, data: InitiateInput) -> BlindpayApiResponse[InitiateResponse]:
        return self._client.post(f"/e/instances/{self._instance_id}/tos", data)


def create_terms_of_service_resource(instance_id: str, client: InternalApiClient) -> TermsOfServiceResource:
    return TermsOfServiceResource(instance_id, client)


def create_terms_of_service_resource_sync(
    instance_id: str, client: InternalApiClientSync
) -> TermsOfServiceResourceSync:
    return TermsOfServiceResourceSync(instance_id, client)
