"""Retry policy, idempotency keys and error shape, in both clients.

Every test runs against ``httpx.MockTransport`` with a recording fake sleep, so nothing touches the network or
really sleeps. ``Client`` drives the async and the sync client through one interface.
"""

import asyncio
import json
import uuid
from pathlib import Path
from typing import Any, AsyncIterator, Callable, Dict, Iterator, List, Optional, Union

import httpx
import pytest

from blindpay import BlindPayError
from blindpay._internal.http import backoff
from tests.http_mock import async_client, sync_client

ERRORS_DIR = Path(__file__).parent / "fixtures" / "spec" / "errors"

Outcome = Union[int, httpx.Response, Exception]


def error_fixture(name: str) -> httpx.Response:
    fixture: Dict[str, Any] = json.loads((ERRORS_DIR / f"{name}.json").read_text())
    headers: Dict[str, str] = {"Content-Type": "application/json", **fixture.get("headers", {})}
    if "raw_body" in fixture:
        return httpx.Response(fixture["status"], content=fixture["raw_body"].encode(), headers=headers)
    return httpx.Response(fixture["status"], content=json.dumps(fixture["body"]).encode(), headers=headers)


def json_response(status: int, body: Any, headers: Optional[Dict[str, str]] = None) -> httpx.Response:
    return httpx.Response(status, content=json.dumps(body).encode(), headers=headers or {})


class Script:
    """Answers each request with the next scripted outcome: a status code, a response, or a raised exception."""

    def __init__(self, *outcomes: Outcome) -> None:
        self.outcomes = list(outcomes)
        self.requests: List[httpx.Request] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        request.read()
        self.requests.append(request)
        outcome = self.outcomes.pop(0) if len(self.outcomes) > 1 else self.outcomes[0]
        if isinstance(outcome, Exception):
            raise outcome
        if isinstance(outcome, int):
            return json_response(outcome, {"id": "tr_000000000000"} if outcome < 300 else {"message": "boom"})
        return outcome

    @property
    def keys(self) -> List[Optional[str]]:
        return [r.headers.get("Idempotency-Key") for r in self.requests]


class Client:
    """One interface over BlindPay and BlindPaySync, with a recording fake sleep."""

    def __init__(self, kind: str, script: Script, **settings: Any) -> None:
        self.kind = kind
        self.sleeps: List[float] = []
        if kind == "async":
            self.client: Any = async_client(script, **settings)

            async def fake_sleep(seconds: float) -> None:
                self.sleeps.append(seconds)

            self.client._api._sleep = fake_sleep
        else:
            self.client = sync_client(script, **settings)
            self.client._api._sleep = self.sleeps.append

    async def call(self, fn: Callable[[Any], Any]) -> Any:
        result = fn(self.client)
        return await result if self.kind == "async" else result

    async def get(self) -> Any:
        return await self.call(lambda c: c.payouts.get("po_000000000000"))

    async def create(self, options: Optional[Dict[str, Any]] = None) -> Any:
        return await self.call(lambda c: c.transfers.create({"transfer_quote_id": "qu_000000000000"}, options))

    async def delete(self) -> Any:
        return await self.call(lambda c: c.partner_fees.delete("fe_000000000000"))

    async def upload(self) -> Any:
        return await self.call(lambda c: c.upload.create({"bucket": "avatar", "file": b"%PDF-1.4"}))


KINDS = ["async", "sync"]


def connect_error() -> httpx.ConnectError:
    return httpx.ConnectError("connection refused")


def read_timeout() -> httpx.ReadTimeout:
    return httpx.ReadTimeout("timed out")


@pytest.mark.parametrize("kind", KINDS)
class TestGetRetries:
    async def test_retried_on_503_then_succeeds(self, kind: str):
        script = Script(503, 200)
        client = Client(kind, script)

        response = await client.get()

        assert response["error"] is None
        assert len(script.requests) == 2
        assert len(client.sleeps) == 1
        assert script.keys == [None, None]  # GETs never carry an Idempotency-Key

    @pytest.mark.parametrize("status", [408, 429, 500, 502, 503, 504])
    async def test_retryable_statuses(self, kind: str, status: int):
        script = Script(status, 200)

        response = await Client(kind, script).get()

        assert response["error"] is None
        assert len(script.requests) == 2

    @pytest.mark.parametrize("error", [connect_error, read_timeout])
    async def test_retried_on_connection_errors_and_timeouts(self, kind: str, error: Callable[[], Exception]):
        script = Script(error(), 200)

        response = await Client(kind, script).get()

        assert response["error"] is None
        assert len(script.requests) == 2

    async def test_gives_up_after_max_retries(self, kind: str):
        script = Script(503)
        client = Client(kind, script)

        response = await client.get()

        assert len(script.requests) == 3
        assert response["error"]["status"] == 503
        assert response["error"]["retryable"] is True
        assert client.sleeps[0] <= backoff(0, 1.0) and client.sleeps[1] <= backoff(1, 1.0)

    async def test_terminal_5xx_code_is_not_retried(self, kind: str):
        script = Script(json_response(502, {"success": False, "code": "PAYINS_CARD_PAYMENT_PENDING", "message": "x"}))

        response = await Client(kind, script).get()

        assert len(script.requests) == 1
        assert response["error"]["retryable"] is False

    @pytest.mark.parametrize("status", [400, 401, 404, 409, 422])
    async def test_other_4xx_are_not_retried(self, kind: str, status: int):
        script = Script(status)

        await Client(kind, script).get()

        assert len(script.requests) == 1

    async def test_retry_after_up_to_60_seconds_is_honoured(self, kind: str):
        script = Script(json_response(503, {"message": "x"}, {"Retry-After": "7"}), 200)
        client = Client(kind, script)

        await client.get()

        assert client.sleeps == [7.0]

    @pytest.mark.parametrize("retry_after", ["61", "120", "Wed, 21 Oct 2026 07:28:00 GMT", "-1", "1.5"])
    async def test_other_retry_after_values_fall_back_to_backoff(self, kind: str, retry_after: str):
        script = Script(json_response(503, {"message": "x"}, {"Retry-After": retry_after}), 200)
        client = Client(kind, script)

        await client.get()

        assert len(client.sleeps) == 1 and 0.25 <= client.sleeps[0] <= 0.5

    async def test_max_retries_zero_disables_retries(self, kind: str):
        script = Script(503, 200)

        response = await Client(kind, script, max_retries=0).get()

        assert len(script.requests) == 1
        assert response["error"]["status"] == 503


@pytest.mark.parametrize("kind", KINDS)
class TestMutationRetries:
    @pytest.mark.parametrize("status", [500, 502, 503, 504])
    async def test_5xx_is_never_retried_and_returns_the_key(self, kind: str, status: int):
        script = Script(status, 200)

        response = await Client(kind, script).create()

        assert len(script.requests) == 1
        error = response["error"]
        assert error["status"] == status
        assert error["retryable"] is True
        assert error["idempotency_key"] == script.keys[0]
        assert uuid.UUID(error["idempotency_key"]).version == 4

    @pytest.mark.parametrize("error", [connect_error, read_timeout])
    async def test_no_response_is_retried_with_the_same_auto_key(self, kind: str, error: Callable[[], Exception]):
        script = Script(error(), 200)

        response = await Client(kind, script).create()

        assert response["error"] is None
        assert len(script.requests) == 2
        assert script.keys[0] is not None and script.keys[0] == script.keys[1]
        assert script.requests[0].content == script.requests[1].content  # identical bytes

    async def test_429_is_retried_after_retry_after_with_the_same_key(self, kind: str):
        script = Script(error_fixture("rate_limited_429"), 200)
        client = Client(kind, script)

        response = await client.create()

        assert response["error"] is None
        assert client.sleeps == [2.0]
        assert script.keys[0] is not None and script.keys[0] == script.keys[1]

    async def test_in_flight_409_is_retried(self, kind: str):
        script = Script(error_fixture("idempotency_in_flight_409"), 200)
        client = Client(kind, script)

        response = await client.create()

        assert response["error"] is None
        assert client.sleeps == [1.0]
        assert script.keys[0] == script.keys[1]

    async def test_in_flight_409_with_long_retry_after_falls_back_to_backoff(self, kind: str):
        in_flight = json_response(
            409, {"success": False, "message": "idempotency_key_in_flight"}, {"Retry-After": "120"}
        )
        script = Script(in_flight)
        client = Client(kind, script)

        response = await client.create()

        assert len(script.requests) == 3
        assert all(s <= 1.0 for s in client.sleeps)
        assert response["error"]["retryable"] is True
        assert response["error"]["idempotency_key"] == script.keys[0]

    async def test_other_409_is_not_retried(self, kind: str):
        script = Script(
            json_response(409, {"success": False, "code": "WALLETS_SELF_CUSTODY_ALREADY_SET", "message": "x"})
        )

        response = await Client(kind, script).create()

        assert len(script.requests) == 1
        assert response["error"]["retryable"] is False

    @pytest.mark.parametrize("fixture", ["idempotency_payload_mismatch_422", "idempotency_key_invalid_400"])
    async def test_terminal_4xx_are_not_retried(self, kind: str, fixture: str):
        script = Script(error_fixture(fixture))

        response = await Client(kind, script).create()

        assert len(script.requests) == 1
        assert response["error"]["retryable"] is False
        assert response["error"]["code"] is None  # idempotency errors carry no code

    async def test_mutation_408_is_not_retried(self, kind: str):
        script = Script(408, 200)

        await Client(kind, script).create()

        assert len(script.requests) == 1

    async def test_caller_key_is_sent_as_is(self, kind: str):
        script = Script(read_timeout(), 200)

        await Client(kind, script).create({"idempotency_key": "order-42"})

        assert script.keys == ["order-42", "order-42"]

    async def test_body_less_delete_gets_a_key(self, kind: str):
        script = Script(200)

        await Client(kind, script).delete()

        assert script.requests[0].method == "DELETE"
        assert script.keys[0] is not None
        assert "Content-Type" not in script.requests[0].headers

    async def test_without_retries_no_key_is_generated_and_nothing_is_retried(self, kind: str):
        script = Script(connect_error(), 200)

        response = await Client(kind, script, max_retries=0).create()

        assert len(script.requests) == 1
        assert script.keys == [None]
        assert response["error"]["idempotency_key"] is None

    @pytest.mark.parametrize("key", ["", "x" * 256])
    async def test_invalid_caller_key_is_rejected_before_sending(self, kind: str, key: str):
        script = Script(200)

        with pytest.raises(BlindPayError, match="idempotency_key"):
            await Client(kind, script).create({"idempotency_key": key})

        assert script.requests == []

    async def test_key_of_255_characters_is_accepted(self, kind: str):
        script = Script(200)

        await Client(kind, script).create({"idempotency_key": "x" * 255})

        assert script.keys == ["x" * 255]


@pytest.mark.parametrize("kind", KINDS)
class TestMultipart:
    async def test_5xx_is_not_retried_and_carries_no_key(self, kind: str):
        script = Script(503, 200)

        response = await Client(kind, script).upload()

        assert len(script.requests) == 1
        assert script.keys == [None]
        assert response["error"]["idempotency_key"] is None

    async def test_connect_error_is_retried(self, kind: str):
        script = Script(connect_error(), 200)

        response = await Client(kind, script).upload()

        assert response["error"] is None
        assert len(script.requests) == 2

    async def test_timeout_is_not_retried(self, kind: str):
        script = Script(read_timeout(), 200)

        response = await Client(kind, script).upload()

        assert len(script.requests) == 1
        assert response["error"]["code"] == "SDK_TIMEOUT"


@pytest.mark.parametrize("kind", KINDS)
class TestErrors:
    async def test_api_error_envelope(self, kind: str):
        script = Script(
            httpx.Response(
                404,
                content=error_fixture("api_error_envelope").content,
                headers={"X-Request-Id": "req_000000000000"},
            )
        )

        response = await Client(kind, script).get()

        assert response["data"] is None
        assert response["error"] == {
            "message": "customer_not_found",
            "status": 404,
            "code": "CUSTOMERS_NOT_FOUND",
            "description": "The customer was not found.",
            "errors": [],
            "trace_id": "0af7651916cd43dd8448eb211c80319c",
            "request_id": "req_000000000000",
            "idempotency_key": None,
            "retryable": False,
        }

    async def test_auth_error_without_trace_id(self, kind: str):
        response = await Client(kind, Script(error_fixture("auth_401_no_trace_id"))).get()

        error = response["error"]
        assert (error["status"], error["code"], error["trace_id"], error["errors"]) == (
            401,
            "AUTH_INVALID_API_KEY",
            None,
            [],
        )
        assert error["retryable"] is False

    async def test_internal_error_without_errors(self, kind: str):
        script = Script(error_fixture("internal_error_no_errors_500"))

        response = await Client(kind, script, max_retries=0).get()

        assert response["error"]["errors"] == []
        assert response["error"]["code"] == "INTERNAL_ERROR"

    async def test_non_json_502_keeps_the_status(self, kind: str):
        script = Script(error_fixture("non_json_502"))

        response = await Client(kind, script).create()

        assert len(script.requests) == 1
        assert response["error"]["status"] == 502
        assert response["error"]["message"] == "Bad Gateway"
        assert response["error"]["retryable"] is True

    async def test_empty_204_is_success_without_data(self, kind: str):
        response = await Client(kind, Script(error_fixture("empty_204"))).delete()

        assert response == {"data": None, "error": None}

    async def test_network_error_has_status_0_and_the_key(self, kind: str):
        script = Script(connect_error())

        response = await Client(kind, script).create()

        error = response["error"]
        assert len(script.requests) == 3
        assert (error["status"], error["code"], error["retryable"]) == (0, "SDK_CONNECTION_ERROR", True)
        assert error["idempotency_key"] == script.keys[0]

    async def test_error_never_echoes_the_api_key(self, kind: str):
        response = await Client(kind, Script(error_fixture("auth_401_no_trace_id"))).create()

        assert "test_key" not in repr(response)


@pytest.mark.parametrize("kind", KINDS)
class TestRequestOptions:
    async def test_timeout_defaults_to_60_seconds_per_attempt(self, kind: str):
        script = Script(200)

        await Client(kind, script).get()

        assert script.requests[0].extensions["timeout"]["read"] == 60.0

    async def test_per_request_timeout_and_headers(self, kind: str):
        script = Script(200)

        await Client(kind, script, timeout=30).create({"timeout": 5, "headers": {"X-Trace": "abc"}})

        assert script.requests[0].extensions["timeout"]["read"] == 5
        assert script.requests[0].headers["X-Trace"] == "abc"

    async def test_options_never_leak_into_other_requests(self, kind: str):
        script = Script(200)
        client = Client(kind, script)

        await client.create({"headers": {"X-Trace": "abc"}, "idempotency_key": "k1"})
        await client.create()

        assert "X-Trace" not in script.requests[1].headers
        assert script.keys[1] not in (None, "k1")


class TestCancellation:
    async def test_cancelling_stops_the_backoff_sleep(self):
        script = Script(503)
        client = async_client(script, max_retries=5)

        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(client.payouts.get("po_000000000000"), timeout=0.05)

        assert len(script.requests) == 1  # real asyncio.sleep backoff was cancelled before the retry


class TestBackoff:
    def test_backoff_doubles_and_caps_at_8_seconds(self):
        assert [backoff(a, 1.0) for a in range(6)] == [0.5, 1.0, 2.0, 4.0, 8.0, 8.0]
        assert backoff(0, 0.5) == 0.25


class TestClientSettings:
    @pytest.mark.parametrize("settings", [{"timeout": 0}, {"max_retries": -1}])
    def test_invalid_settings_are_rejected(self, settings: Dict[str, Any]):
        with pytest.raises(BlindPayError):
            sync_client(Script(200), **settings)

    @pytest.mark.parametrize(
        "base_url", ["https://proxy.example", "https://proxy.example/", "https://proxy.example/v1"]
    )
    def test_base_url(self, base_url: str):
        script = Script(200)

        sync_client(script, base_url=base_url).payouts.get("po_000000000000")

        assert (
            str(script.requests[0].url) == "https://proxy.example/v1/instances/in_000000000000/payouts/po_000000000000"
        )

    def test_repr_redacts_the_api_key(self):
        client = sync_client(Script(200))

        assert "test_key" not in repr(client)
        assert "***" in repr(client)


class FailingBody(httpx.SyncByteStream, httpx.AsyncByteStream):
    """A body that breaks after the status line has arrived."""

    def __iter__(self) -> Iterator[bytes]:
        raise httpx.ReadError("connection reset while reading the body")
        yield b""  # pragma: no cover

    async def __aiter__(self) -> AsyncIterator[bytes]:
        raise httpx.ReadError("connection reset while reading the body")
        yield b""  # pragma: no cover


def broken_body(status: int) -> httpx.Response:
    return httpx.Response(status, stream=FailingBody())


@pytest.mark.parametrize("kind", KINDS)
class TestBodyReadFailures:
    @pytest.mark.parametrize("status", [200, 500, 503])
    async def test_mutation_is_not_retried_once_a_status_arrived(self, kind: str, status: int):
        script = Script(broken_body(status), 200)

        response = await Client(kind, script).create()

        assert len(script.requests) == 1
        error = response["error"]
        assert (error["status"], error["code"], error["retryable"]) == (status, "SDK_RESPONSE_READ_ERROR", True)
        assert error["idempotency_key"] == script.keys[0]

    async def test_get_is_retried(self, kind: str):
        script = Script(broken_body(503), 200)

        response = await Client(kind, script).get()

        assert response["error"] is None
        assert len(script.requests) == 2

    async def test_local_protocol_error_is_not_retried(self, kind: str):
        script = Script(httpx.LocalProtocolError("illegal header value"), 200)

        response = await Client(kind, script).get()

        assert len(script.requests) == 1
        assert response["error"]["code"] == "SDK_ERROR"


@pytest.mark.parametrize("kind", KINDS)
class TestKeyAndHeaderValidation:
    @pytest.mark.parametrize("key", ["   ", " order-1", "order-1 ", "order-1\n", "order\x00-1", "órder-1"])
    async def test_malformed_key_is_rejected_before_sending(self, kind: str, key: str):
        script = Script(200)

        with pytest.raises(BlindPayError, match="idempotency_key"):
            await Client(kind, script).create({"idempotency_key": key})

        assert script.requests == []

    @pytest.mark.parametrize("name", ["authorization", "AUTHORIZATION", "user-agent", "User-Agent", "idempotency-key"])
    async def test_protected_headers_cannot_be_overridden(self, kind: str, name: str):
        script = Script(200)

        with pytest.raises(BlindPayError, match="set by the client"):
            await Client(kind, script).create({"headers": {name: "x"}})

        assert script.requests == []

    async def test_other_headers_merge_case_insensitively(self, kind: str):
        script = Script(200)

        await Client(kind, script).create({"headers": {"accept": "application/json; v=2"}})

        assert script.requests[0].headers.get_list("accept") == ["application/json; v=2"]


@pytest.mark.parametrize("kind", KINDS)
class TestRetryableFlag:
    """``retryable`` promises that resending may succeed; it depends on the method and the key, not only the status."""

    async def test_keyed_mutation_408_is_not_retryable(self, kind: str):
        response = await Client(kind, Script(408)).create()

        assert response["error"]["status"] == 408
        assert response["error"]["retryable"] is False

    @pytest.mark.parametrize("status", [500, 503])
    async def test_unkeyed_mutation_5xx_is_not_retryable(self, kind: str, status: int):
        script = Script(status)

        response = await Client(kind, script, max_retries=0).create()

        assert script.keys == [None]
        assert response["error"]["retryable"] is False

    async def test_unkeyed_mutation_connection_error_is_not_retryable(self, kind: str):
        response = await Client(kind, Script(connect_error()), max_retries=0).create()

        assert response["error"]["code"] == "SDK_CONNECTION_ERROR"
        assert response["error"]["retryable"] is False

    async def test_4xx_with_an_unreadable_body_is_classified_by_its_status(self, kind: str):
        response = await Client(kind, Script(broken_body(400))).create()

        assert response["error"]["status"] == 400
        assert response["error"]["retryable"] is False

    @pytest.mark.parametrize("timeout", [0, -1])
    async def test_non_positive_per_request_timeout_is_rejected_before_sending(self, kind: str, timeout: float):
        script = Script(200)

        with pytest.raises(BlindPayError, match="timeout"):
            await Client(kind, script).create({"timeout": timeout})

        assert script.requests == []
