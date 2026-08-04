from typing import Optional

from typing_extensions import Literal, NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import ApprovalRate, BlindpayApiResponse

UploadBucket = Literal["avatar", "onboarding", "limit_increase"]

UploadAnalyzeDocumentType = Literal[
    "proof_of_address",
    "identity_document",
    "incorporation_document",
    "proof_of_ownership",
    "source_of_funds",
    "selfie",
    "bank_statement",
    "tax_return",
    "proof_of_income",
    "financial_statement",
    "invoice",
    "transaction_document",
    "passport",
    "pay_stub",
    "employment_letter",
    "investment",
    "crypto_exchange",
    "blockchain_wallet",
    "contract",
    "accounts_receivable",
    "merchant_processor",
    "shareholder_loan",
]


class UploadInput(TypedDict):
    bucket: UploadBucket
    file: str


class UploadResponse(TypedDict):
    url: str


class UploadAnalyzeInput(TypedDict):
    file: str
    type: UploadAnalyzeDocumentType
    metadata: NotRequired[Optional[str]]


class UploadAnalyzeOutput(TypedDict):
    approval_rate: ApprovalRate
    description: str


class UploadResource:
    def __init__(self, client: InternalApiClient):
        self._client = client

    async def create(self, data: UploadInput) -> BlindpayApiResponse[UploadResponse]:
        return await self._client.post("/upload", data)

    async def analyze(self, data: UploadAnalyzeInput) -> BlindpayApiResponse[UploadAnalyzeOutput]:
        return await self._client.post("/upload/analyze", data)


class UploadResourceSync:
    def __init__(self, client: InternalApiClientSync):
        self._client = client

    def create(self, data: UploadInput) -> BlindpayApiResponse[UploadResponse]:
        return self._client.post("/upload", data)

    def analyze(self, data: UploadAnalyzeInput) -> BlindpayApiResponse[UploadAnalyzeOutput]:
        return self._client.post("/upload/analyze", data)


def create_upload_resource(client: InternalApiClient) -> UploadResource:
    return UploadResource(client)


def create_upload_resource_sync(client: InternalApiClientSync) -> UploadResourceSync:
    return UploadResourceSync(client)
