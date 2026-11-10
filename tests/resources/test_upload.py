"""Upload and analyze send multipart/form-data (POST /v1/upload, POST /v1/upload/analyze) with ?instance_id=."""

import io
from typing import Any, Dict

import pytest

from blindpay.resources.upload import UploadAnalyzeOutput, UploadResponse
from tests.http_mock import INSTANCE_ID, Recorder, async_client, sync_client
from tests.spec_fixtures import assert_matches_spec, response_variants

PDF = b"%PDF-1.7\n%test document\n"
PNG = b"\x89PNG\r\n\x1a\nfake"

UPLOAD = response_variants("POST /v1/upload")
ANALYZE = response_variants("POST /v1/upload/analyze")


def assert_multipart(request: Any, path: str, fields: Dict[str, str], filename: str, content_type: str) -> None:
    assert request.method == "POST"
    assert request.url.path == path
    assert dict(request.url.params) == {"instance_id": INSTANCE_ID}
    assert request.headers["Content-Type"].startswith("multipart/form-data; boundary=")
    assert request.headers["Authorization"] == "Bearer test_key"
    assert "Idempotency-Key" not in request.headers
    body = request.content
    for name, value in fields.items():
        assert f'Content-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode() in body
    file_header = f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: {content_type}'
    assert file_header.encode() in body


class TestUploadTypesMatchSpec:
    def test_upload_response(self):
        assert_matches_spec(UploadResponse, UPLOAD)

    def test_analyze_response(self):
        assert_matches_spec(UploadAnalyzeOutput, ANALYZE)


class TestUpload:
    @pytest.mark.asyncio
    async def test_create_sends_multipart(self):
        recorder = Recorder(body=UPLOAD["full"])
        client = async_client(recorder)

        response = await client.upload.create({"bucket": "documents", "file": PDF, "filename": "invoice.pdf"})

        assert response["error"] is None
        assert response["data"] == UPLOAD["full"]
        assert_multipart(recorder.last, "/v1/upload", {"bucket": "documents"}, "invoice.pdf", "application/pdf")
        assert PDF in recorder.last.content

    @pytest.mark.asyncio
    async def test_create_sniffs_content_type_from_bytes(self):
        recorder = Recorder(body=UPLOAD["full"])
        client = async_client(recorder)

        await client.upload.create({"bucket": "avatar", "file": PNG})

        assert_multipart(recorder.last, "/v1/upload", {"bucket": "avatar"}, "file", "image/png")

    @pytest.mark.asyncio
    async def test_create_sniffs_content_type_from_unnamed_stream(self):
        recorder = Recorder(body=UPLOAD["full"])
        client = async_client(recorder)
        stream = io.BytesIO(PDF)

        await client.upload.create({"bucket": "documents", "file": stream})

        assert_multipart(recorder.last, "/v1/upload", {"bucket": "documents"}, "file", "application/pdf")
        assert PDF in recorder.last.content

    @pytest.mark.asyncio
    async def test_create_reads_file_objects(self, tmp_path: Any):
        path = tmp_path / "id-front.png"
        path.write_bytes(PNG)
        recorder = Recorder(body=UPLOAD["full"])
        client = async_client(recorder)

        with path.open("rb") as handle:
            await client.upload.create({"bucket": "onboarding", "file": handle})

        assert_multipart(recorder.last, "/v1/upload", {"bucket": "onboarding"}, "id-front.png", "image/png")
        assert PNG in recorder.last.content

    @pytest.mark.asyncio
    async def test_analyze_sends_multipart_with_json_metadata(self):
        recorder = Recorder(body=ANALYZE["full"])
        client = async_client(recorder)

        response = await client.upload.analyze(
            {"file": PDF, "type": "proof_of_address", "metadata": {"full_name": "Jane Doe"}}
        )

        assert response["error"] is None
        assert response["data"] == ANALYZE["full"]
        assert_multipart(
            recorder.last,
            "/v1/upload/analyze",
            {"type": "proof_of_address", "metadata": '{"full_name": "Jane Doe"}'},
            "file",
            "application/pdf",
        )

    @pytest.mark.asyncio
    async def test_analyze_omits_absent_metadata(self):
        recorder = Recorder(body=ANALYZE["full"])
        client = async_client(recorder)

        await client.upload.analyze({"file": PDF, "type": "invoice", "content_type": "application/pdf"})

        assert b'name="metadata"' not in recorder.last.content

    @pytest.mark.asyncio
    async def test_error_response(self):
        recorder = Recorder(status=400, body={"success": False, "message": "file_type_not_allowed"})
        client = async_client(recorder)

        response = await client.upload.create({"bucket": "avatar", "file": b"plain text"})

        assert response["data"] is None
        assert response["error"] == {"message": "file_type_not_allowed"}
        assert_multipart(recorder.last, "/v1/upload", {"bucket": "avatar"}, "file", "application/octet-stream")


class TestUploadSync:
    def test_create_sends_multipart(self):
        recorder = Recorder(body=UPLOAD["full"])
        client = sync_client(recorder)

        response = client.upload.create({"bucket": "limit_increase", "file": PDF, "filename": "statement.pdf"})

        assert response["error"] is None
        assert response["data"] == UPLOAD["full"]
        assert_multipart(recorder.last, "/v1/upload", {"bucket": "limit_increase"}, "statement.pdf", "application/pdf")

    def test_analyze_sends_multipart_with_string_metadata(self):
        recorder = Recorder(body=ANALYZE["full"])
        client = sync_client(recorder)

        response = client.upload.analyze(
            {"file": PNG, "type": "selfie", "metadata": '{"full_name":"Jane Doe"}', "filename": "selfie.png"}
        )

        assert response["error"] is None
        assert response["data"] == ANALYZE["full"]
        assert_multipart(
            recorder.last,
            "/v1/upload/analyze",
            {"type": "selfie", "metadata": '{"full_name":"Jane Doe"}'},
            "selfie.png",
            "image/png",
        )
