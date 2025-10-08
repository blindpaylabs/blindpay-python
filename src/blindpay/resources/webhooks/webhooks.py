from typing import List

from typing_extensions import Literal, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse

WebhookEvents = Literal[
    "receiver.new",
    "receiver.update",
    "bankAccount.new",
    "payout.new",
    "payout.update",
    "payout.complete",
    "payout.partnerFee",
    "blockchainWallet.new",
    "payin.new",
    "payin.update",
    "payin.complete",
    "payin.partnerFee",
]


class CreateWebhookEndpointInput(TypedDict):
    url: str
    events: List[WebhookEvents]


class CreateWebhookEndpointResponse(TypedDict):
    id: str


class WebhookEndpoint(TypedDict):
    id: str
    url: str
    events: List[WebhookEvents]
    last_event_at: str
    instance_id: str
    created_at: str
    updated_at: str


ListWebhookEndpointsResponse = List[WebhookEndpoint]


class GetWebhookEndpointSecretResponse(TypedDict):
    key: str


class GetPortalAccessUrlResponse(TypedDict):
    url: str


class WebhookEndpointsResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self) -> BlindpayApiResponse[ListWebhookEndpointsResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/webhook-endpoints")

    async def create(self, data: CreateWebhookEndpointInput) -> BlindpayApiResponse[CreateWebhookEndpointResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/webhook-endpoints", data)

    async def delete(self, id: str) -> BlindpayApiResponse[None]:
        return await self._client.delete(f"/instances/{self._instance_id}/webhook-endpoints/{id}")

    async def get_secret(self, id: str) -> BlindpayApiResponse[GetWebhookEndpointSecretResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/webhook-endpoints/{id}/secret")

    async def get_portal_access_url(self) -> BlindpayApiResponse[GetPortalAccessUrlResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/webhook-endpoints/portal-access")


class WebhookEndpointsResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self) -> BlindpayApiResponse[ListWebhookEndpointsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/webhook-endpoints")

    def create(self, data: CreateWebhookEndpointInput) -> BlindpayApiResponse[CreateWebhookEndpointResponse]:
        return self._client.post(f"/instances/{self._instance_id}/webhook-endpoints", data)

    def delete(self, id: str) -> BlindpayApiResponse[None]:
        return self._client.delete(f"/instances/{self._instance_id}/webhook-endpoints/{id}")

    def get_secret(self, id: str) -> BlindpayApiResponse[GetWebhookEndpointSecretResponse]:
        return self._client.get(f"/instances/{self._instance_id}/webhook-endpoints/{id}/secret")

    def get_portal_access_url(self) -> BlindpayApiResponse[GetPortalAccessUrlResponse]:
        return self._client.get(f"/instances/{self._instance_id}/webhook-endpoints/portal-access")


def create_webhook_endpoints_resource(instance_id: str, client: InternalApiClient) -> WebhookEndpointsResource:
    return WebhookEndpointsResource(instance_id, client)


def create_webhook_endpoints_resource_sync(
    instance_id: str, client: InternalApiClientSync
) -> WebhookEndpointsResourceSync:
    return WebhookEndpointsResourceSync(instance_id, client)
