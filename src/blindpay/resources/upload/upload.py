import json
import mimetypes
import os
import warnings
from typing import IO, Any, Dict, Mapping, Optional, Tuple, TypeVar, Union, cast, overload

from typing_extensions import Literal, NotRequired, TypedDict, deprecated

from ..._internal.api_client import InternalApiClient, InternalApiClientSync, MultipartFile
from ..._internal.http import RequestOptions, build_query
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


class UploadFile(TypedDict):
    file: FileContent
    filename: NotRequired[str]
    content_type: NotRequired[str]


class UploadInput(UploadFile):
    bucket: UploadBucket


class UploadResponse(TypedDict):
    file_url: str


class UploadAnalyzeInput(UploadFile):
    type: UploadAnalyzeDocumentType
    metadata: NotRequired[Optional[Union[str, Mapping[str, Any]]]]


class UploadAnalyzeOutput(TypedDict):
    approval_rate: ApprovalRate
    description: str


_MAGIC_BYTES = (
    (b"%PDF", "application/pdf"),
    (b"\x89PNG", "image/png"),
    (b"\xff\xd8\xff", "image/jpeg"),
)


def _file_part(data: UploadFile) -> MultipartFile:
    file = data["file"]
    filename = data.get("filename")
    content_type = data.get("content_type")
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
    files = {"file": _file_part(data)}
    return {"bucket": data["bucket"]}, files


def _analyze_request(data: UploadAnalyzeInput) -> Tuple[Dict[str, str], Dict[str, MultipartFile]]:
    form: Dict[str, str] = {"type": data["type"]}
    metadata = data.get("metadata")
    if metadata is not None:
        form["metadata"] = metadata if isinstance(metadata, str) else json.dumps(metadata)
    files = {"file": _file_part(data)}
    return form, files


def _build_instance_query(instance_id: Optional[str]) -> str:
    # API-key calls authenticate against ?instance_id=, so always send the client's own instance.
    return build_query({"instance_id": instance_id})


_ClientT = TypeVar("_ClientT")


def _legacy_order(
    instance_id: Union[str, None, _ClientT], client: Optional[_ClientT]
) -> Tuple[Optional[str], _ClientT]:
    # Before instance_id was required here, the factories and classes took (client) alone. Keep those calls
    # working (they get no ?instance_id=, as before) and warn, since the API rejects uploads without it.
    if client is None:
        warnings.warn(
            "Pass the instance id first: create_upload_resource(instance_id, client).", DeprecationWarning, stacklevel=3
        )
        return None, cast(_ClientT, instance_id)
    return cast(Optional[str], instance_id), client


class UploadResource:
    def __init__(self, instance_id: Optional[str], client: Optional[InternalApiClient] = None):
        resolved_instance_id, resolved_client = _legacy_order(instance_id, client)
        self._client: InternalApiClient = resolved_client
        self._instance_query = _build_instance_query(resolved_instance_id)

    async def create(
        self, data: UploadInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[UploadResponse]:
        form, files = _upload_request(data)
        return await self._client.post_multipart(f"/upload{self._instance_query}", form, files, options=options)

    async def analyze(
        self, data: UploadAnalyzeInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[UploadAnalyzeOutput]:
        form, files = _analyze_request(data)
        return await self._client.post_multipart(f"/upload/analyze{self._instance_query}", form, files, options=options)


class UploadResourceSync:
    def __init__(self, instance_id: Optional[str], client: Optional[InternalApiClientSync] = None):
        resolved_instance_id, resolved_client = _legacy_order(instance_id, client)
        self._client: InternalApiClientSync = resolved_client
        self._instance_query = _build_instance_query(resolved_instance_id)

    def create(
        self, data: UploadInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[UploadResponse]:
        form, files = _upload_request(data)
        return self._client.post_multipart(f"/upload{self._instance_query}", form, files, options=options)

    def analyze(
        self, data: UploadAnalyzeInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[UploadAnalyzeOutput]:
        form, files = _analyze_request(data)
        return self._client.post_multipart(f"/upload/analyze{self._instance_query}", form, files, options=options)


@overload
def create_upload_resource(instance_id: str, client: InternalApiClient) -> UploadResource: ...
@overload
@deprecated("Pass the instance id first: create_upload_resource(instance_id, client).")
def create_upload_resource(instance_id: InternalApiClient) -> UploadResource: ...
def create_upload_resource(
    instance_id: Union[str, InternalApiClient], client: Optional[InternalApiClient] = None
) -> UploadResource:
    resolved_instance_id, resolved_client = _legacy_order(instance_id, client)
    return UploadResource(resolved_instance_id, resolved_client)


@overload
def create_upload_resource_sync(instance_id: str, client: InternalApiClientSync) -> UploadResourceSync: ...
@overload
@deprecated("Pass the instance id first: create_upload_resource_sync(instance_id, client).")
def create_upload_resource_sync(instance_id: InternalApiClientSync) -> UploadResourceSync: ...
def create_upload_resource_sync(
    instance_id: Union[str, InternalApiClientSync], client: Optional[InternalApiClientSync] = None
) -> UploadResourceSync:
    resolved_instance_id, resolved_client = _legacy_order(instance_id, client)
    return UploadResourceSync(resolved_instance_id, resolved_client)
