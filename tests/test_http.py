"""Wire-level checks of the HTTP layer shared by every resource, in both clients."""

import json

import pytest

import blindpay
from blindpay._internal.http import build_query, path_param
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


class TestPathAndQuery:
    @pytest.mark.asyncio
    async def test_path_params_are_percent_encoded(self):
        recorder = Recorder(body={})
        client = async_client(recorder)

        await client.payouts.get("a/b?c")
        await client.customers.bank_accounts.delete("cu/1", "ba 2")

        assert recorder.requests[0].url.raw_path == b"/v1/instances/in_000000000000/payouts/a%2Fb%3Fc"
        assert recorder.last.url.raw_path == b"/v1/instances/in_000000000000/customers/cu%2F1/bank-accounts/ba%202"

    def test_sync_path_params_are_percent_encoded(self):
        recorder = Recorder(body={})
        client = sync_client(recorder)

        client.wallets.custodial.get({"customer_id": "cu/1", "id": "wa/2"})

        assert recorder.last.url.raw_path == b"/v1/instances/in_000000000000/customers/cu%2F1/wallets/wa%2F2"

    @pytest.mark.asyncio
    async def test_list_sends_only_the_params_that_are_set(self):
        recorder = Recorder(body=[])
        client = async_client(recorder)

        await client.payouts.list({"limit": "10", "starting_after": "po_000000000000", "customer_id": None})  # type: ignore[arg-type]

        assert recorder.last.url.query == b"limit=10&starting_after=po_000000000000"

    def test_sync_list_without_params_sends_no_query(self):
        recorder = Recorder(body=[])
        client = sync_client(recorder)

        client.payouts.list()
        client.payouts.list({})

        assert [r.url.query for r in recorder.requests] == [b"", b""]

    def test_build_query(self):
        assert build_query(None) == ""
        assert build_query({"a": None, "b": ""}) == ""
        assert (
            build_query({"limit": 10, "flag": True, "off": False, "q": "a b&c"})
            == "?limit=10&flag=true&off=false&q=a+b%26c"
        )

    def test_path_param(self):
        assert path_param("in_000000000000") == "in_000000000000"
        assert path_param("a/b c%") == "a%2Fb%20c%25"


class TestListFilters:
    def test_bank_account_list_filters(self):
        recorder = Recorder(body=[])
        client = sync_client(recorder)

        client.customers.bank_accounts.list("cu_000000000000", {"status": "approved", "type": "pix", "country": "BR"})

        assert recorder.last.url.query == b"status=approved&type=pix&country=BR"

    @pytest.mark.asyncio
    async def test_payin_track_sends_the_checkout_token_only_when_given(self):
        recorder = Recorder(body={})
        client = async_client(recorder)

        await client.payins.get_track("pi_000000000000")
        await client.payins.get_track("pi_000000000000", checkout_token="ct_1")

        assert [r.url.query for r in recorder.requests] == [b"", b"checkout_token=ct_1"]

    def test_transfer_and_payout_filters(self):
        recorder = Recorder(body={"data": [], "pagination": {"has_more": False}})
        client = sync_client(recorder)

        client.transfers.list({"wallet_id": "wa_000000000000", "network": "base", "token": "USDC"})
        client.payouts.list({"status": "completed", "payment_method": "pix", "country": "BR"})

        assert [r.url.query for r in recorder.requests] == [
            b"wallet_id=wa_000000000000&network=base&token=USDC",
            b"status=completed&payment_method=pix&country=BR",
        ]
