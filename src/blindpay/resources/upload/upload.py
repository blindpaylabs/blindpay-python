from typing_extensions import Literal, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse

UploadBucket = Literal["avatar", "onboarding", "limit_increase"]


class UploadInput(TypedDict):
    bucket: UploadBucket
    file: str


class UploadResponse(TypedDict):
    url: str


class UploadResource:
    def __init__(self, client: InternalApiClient):
        self._client = client

    async def create(self, data: UploadInput) -> BlindpayApiResponse[UploadResponse]:
        return await self._client.post("/upload", data)


class UploadResourceSync:
    def __init__(self, client: InternalApiClientSync):
        self._client = client

    def create(self, data: UploadInput) -> BlindpayApiResponse[UploadResponse]:
        return self._client.post("/upload", data)


def create_upload_resource(client: InternalApiClient) -> UploadResource:
    return UploadResource(client)


def create_upload_resource_sync(client: InternalApiClientSync) -> UploadResourceSync:
    return UploadResourceSync(client)
