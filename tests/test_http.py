"""Wire-level checks of the HTTP layer shared by every resource, in both clients."""

import json

import pytest

import blindpay
from tests.http_mock import Recorder, async_client, sync_client


class TestContentType:
    @pytest.mark.asyncio
    async def test_json_body_sends_json_content_type(self):
        recorder = Recorder(body={"id": "tr_000000000000"})
        client = async_client(recorder)

        await client.transfers.create({"transfer_quote_id": "qu_000000000000"})

        assert recorder.last.headers["Content-Type"] == "application/json"
        assert json.loads(recorder.last.read()) == {"transfer_quote_id": "qu_000000000000"}

    @pytest.mark.asyncio
    async def test_get_sends_no_content_type(self):
        recorder = Recorder(body=[])
        client = async_client(recorder)

        await client.available.get_rails()

        assert recorder.last.method == "GET"
        assert "Content-Type" not in recorder.last.headers
        assert recorder.last.headers["Accept"] == "application/json"

    def test_sync_json_body_sends_json_content_type(self):
        recorder = Recorder(body={"id": "tr_000000000000"})
        client = sync_client(recorder)

        client.transfers.create({"transfer_quote_id": "qu_000000000000"})

        assert recorder.last.headers["Content-Type"] == "application/json"

    def test_sync_get_sends_no_content_type(self):
        recorder = Recorder(body=[])
        client = sync_client(recorder)

        client.available.get_rails()

        assert "Content-Type" not in recorder.last.headers


class TestHeaders:
    @pytest.mark.asyncio
    async def test_user_agent_and_authorization_on_the_wire(self):
        recorder = Recorder(body=[])
        client = async_client(recorder)

        await client.available.get_rails()

        assert recorder.last.headers["User-Agent"] == f"blindpay-python/{blindpay.__version__}"
        assert recorder.last.headers["Authorization"] == "Bearer test_key"

    def test_sync_user_agent_and_authorization_on_the_wire(self):
        recorder = Recorder(body=[])
        client = sync_client(recorder)

        client.available.get_rails()

        assert recorder.last.headers["User-Agent"] == f"blindpay-python/{blindpay.__version__}"
        assert recorder.last.headers["Authorization"] == "Bearer test_key"
