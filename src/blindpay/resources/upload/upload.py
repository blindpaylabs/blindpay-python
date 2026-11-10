import json
import mimetypes
import os
from typing import IO, Any, Dict, Mapping, Optional, Tuple, Union
from urllib.parse import urlencode

from typing_extensions import Literal, NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync, MultipartFile
from ...types import ApprovalRate, BlindpayApiResponse

UploadBucket = Literal["avatar", "onboarding", "limit_increase", "documents"]

FileContent = Union[bytes, IO[bytes]]
"""The file to upload: raw bytes or a binary file object (e.g. ``open("id.pdf", "rb")``)."""

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
    file: FileContent
    filename: NotRequired[str]
    content_type: NotRequired[str]


class UploadResponse(TypedDict):
    file_url: str


class UploadAnalyzeInput(TypedDict):
    file: FileContent
    type: UploadAnalyzeDocumentType
    metadata: NotRequired[Optional[Union[str, Mapping[str, Any]]]]
    filename: NotRequired[str]
    content_type: NotRequired[str]


class UploadAnalyzeOutput(TypedDict):
    approval_rate: ApprovalRate
    description: str


_MAGIC_BYTES = (
    (b"%PDF", "application/pdf"),
    (b"\x89PNG", "image/png"),
    (b"\xff\xd8\xff", "image/jpeg"),
)


def _file_part(file: FileContent, filename: Optional[str] = None, content_type: Optional[str] = None) -> MultipartFile:
    # The API checks the part's declared MIME type against the bucket's allow-list and the file's magic bytes,
    # so send an accurate one: explicit, else guessed from the filename, else sniffed from the content.
    if filename is None:
        name = getattr(file, "name", None)
        filename = os.path.basename(name) if isinstance(name, str) else "file"
    if content_type is None:
        content_type = mimetypes.guess_type(filename)[0]
    if content_type is None:
        head = _peek(file)
        content_type = next((mime for magic, mime in _MAGIC_BYTES if head.startswith(magic)), None)
    return (filename, file, content_type or "application/octet-stream")


def _peek(file: FileContent) -> bytes:
    if isinstance(file, bytes):
        return file[:8]
    try:
        if file.seekable():
            position = file.tell()
            head = file.read(8)
            file.seek(position)
            return head
    except (AttributeError, OSError, ValueError):
        pass
    return b""


def _upload_request(data: UploadInput) -> Tuple[Dict[str, str], Dict[str, MultipartFile]]:
    files = {"file": _file_part(data["file"], data.get("filename"), data.get("content_type"))}
    return {"bucket": data["bucket"]}, files


def _analyze_request(data: UploadAnalyzeInput) -> Tuple[Dict[str, str], Dict[str, MultipartFile]]:
    form: Dict[str, str] = {"type": data["type"]}
    metadata = data.get("metadata")
    if metadata is not None:
        form["metadata"] = metadata if isinstance(metadata, str) else json.dumps(metadata)
    files = {"file": _file_part(data["file"], data.get("filename"), data.get("content_type"))}
    return form, files


def _instance_query(instance_id: Optional[str]) -> str:
    # API-key calls authenticate against ?instance_id=, so always send the client's own instance.
    return f"?{urlencode({'instance_id': instance_id})}" if instance_id else ""


class UploadResource:
    def __init__(self, client: InternalApiClient, instance_id: Optional[str] = None):
        self._client = client
        self._query = _instance_query(instance_id)

    async def create(self, data: UploadInput) -> BlindpayApiResponse[UploadResponse]:
        form, files = _upload_request(data)
        return await self._client.post_multipart(f"/upload{self._query}", form, files)

    async def analyze(self, data: UploadAnalyzeInput) -> BlindpayApiResponse[UploadAnalyzeOutput]:
        form, files = _analyze_request(data)
        return await self._client.post_multipart(f"/upload/analyze{self._query}", form, files)


class UploadResourceSync:
    def __init__(self, client: InternalApiClientSync, instance_id: Optional[str] = None):
        self._client = client
        self._query = _instance_query(instance_id)

    def create(self, data: UploadInput) -> BlindpayApiResponse[UploadResponse]:
        form, files = _upload_request(data)
        return self._client.post_multipart(f"/upload{self._query}", form, files)

    def analyze(self, data: UploadAnalyzeInput) -> BlindpayApiResponse[UploadAnalyzeOutput]:
        form, files = _analyze_request(data)
        return self._client.post_multipart(f"/upload/analyze{self._query}", form, files)


def create_upload_resource(client: InternalApiClient, instance_id: Optional[str] = None) -> UploadResource:
    return UploadResource(client, instance_id)


def create_upload_resource_sync(client: InternalApiClientSync, instance_id: Optional[str] = None) -> UploadResourceSync:
    return UploadResourceSync(client, instance_id)
