"""W2: typed error codes generated from the spec's ``Errors`` tag, checked against the shared oracle."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List

import httpx
import pytest

from blindpay import BlindPayApiError, ErrorCode, ErrorCodeInfo, RetryClass, error_code_info
from tests.http_mock import async_client, sync_client

ROOT = Path(__file__).resolve().parent.parent
GENERATOR = ROOT / ".api-sync" / "gen_error_codes.py"
SNAPSHOT = ROOT / ".api-sync" / "spec-snapshot.json"
ORACLE: List[Dict[str, Any]] = json.loads((Path(__file__).parent / "fixtures" / "error-codes.json").read_text())[
    "codes"
]


def test_every_spec_code_is_typed_with_its_status_and_retry_class():
    assert sorted(code.value for code in ErrorCode) == sorted(row["code"] for row in ORACLE)
    for row in ORACLE:
        assert error_code_info(row["code"]) == ErrorCodeInfo(row["status"], RetryClass(row["retry"])), row["code"]


def test_counts_match_the_oracle():
    retry = [info.retry for info in (error_code_info(code) for code in ErrorCode) if info is not None]
    assert len(ErrorCode) == 175
    assert (
        retry.count(RetryClass.ACTIONABLE),
        retry.count(RetryClass.TERMINAL),
        retry.count(RetryClass.RETRYABLE),
    ) == (
        96,
        61,
        18,
    )


def test_swap_minimum_code():
    info = error_code_info(ErrorCode.TRANSFERS_SWAP_AMOUNT_BELOW_MINIMUM)

    assert info == ErrorCodeInfo(status=400, retry=RetryClass.ACTIONABLE)
    assert error_code_info("TRANSFERS_SWAP_AMOUNT_BELOW_MINIMUM") == info


def test_codes_compare_and_print_as_their_wire_string():
    code = ErrorCode.QUOTES_EXPIRED

    assert code == "QUOTES_EXPIRED" and "QUOTES_EXPIRED" == code
    assert str(code) == f"{code}" == "QUOTES_EXPIRED"
    assert str(RetryClass.TERMINAL) == "terminal"
    assert json.dumps({"code": code, "retry": RetryClass.TERMINAL}) == '{"code": "QUOTES_EXPIRED", "retry": "terminal"}'


@pytest.mark.parametrize("code", [None, "", "SDK_TIMEOUT", "ZZ_CODE_FROM_A_NEWER_API"])
def test_unknown_codes_have_no_info(code: Any):
    assert error_code_info(code) is None


def _client(kind: str, handler: Callable[[httpx.Request], httpx.Response]) -> Any:
    return async_client(handler, max_retries=0) if kind == "async" else sync_client(handler, max_retries=0)


async def _get(kind: str, client: Any) -> Any:
    result = client.payouts.get("pa_000000000000")
    return await result if kind == "async" else result


@pytest.mark.parametrize("kind", ["async", "sync"])
@pytest.mark.parametrize(
    "body,expected",
    [
        ({"code": "TRANSFERS_SWAP_AMOUNT_BELOW_MINIMUM", "message": "fx_amount_below_minimum"}, RetryClass.ACTIONABLE),
        ({"code": "ZZ_CODE_FROM_A_NEWER_API", "message": "x"}, RetryClass.UNKNOWN),
        ({"message": "idempotency_key_reused"}, RetryClass.UNKNOWN),
    ],
)
async def test_error_responses_carry_the_retry_class(kind: str, body: Dict[str, Any], expected: RetryClass):
    client = _client(kind, lambda _request: httpx.Response(400, json=body))

    error = (await _get(kind, client))["error"]

    assert error["retry_class"] == expected
    assert error["code"] == body.get("code")  # unknown codes stay reachable as plain strings
    assert error["message"] == body["message"]
    if expected is RetryClass.ACTIONABLE:
        assert error["code"] == ErrorCode.TRANSFERS_SWAP_AMOUNT_BELOW_MINIMUM


@pytest.mark.parametrize("kind", ["async", "sync"])
async def test_transport_errors_are_unknown(kind: str):
    def refuse(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    error = (await _get(kind, _client(kind, refuse)))["error"]

    assert error["code"] == "SDK_CONNECTION_ERROR" and error["retry_class"] is RetryClass.UNKNOWN


def test_api_error_exposes_the_retry_class_even_for_hand_built_errors():
    assert BlindPayApiError({"message": "m", "code": "QUOTES_EXPIRED"}).retry_class is RetryClass.ACTIONABLE
    assert BlindPayApiError({"message": "m"}).retry_class is RetryClass.UNKNOWN


def _run(spec: Dict[str, Any], tmp_path: Path) -> "subprocess.CompletedProcess[str]":
    path = tmp_path / "spec.json"
    path.write_text(json.dumps(spec))
    return subprocess.run(
        [sys.executable, str(GENERATOR), "--spec", str(path), "--check"], capture_output=True, text=True, check=False
    )


def _with_errors_table(transform: Callable[[str], str]) -> Dict[str, Any]:
    spec: Dict[str, Any] = json.loads(SNAPSHOT.read_text())
    for tag in spec["tags"]:
        if tag["name"] == "Errors":
            tag["description"] = transform(tag["description"])
    return spec


def test_generator_check_passes_on_the_snapshot(tmp_path: Path):
    result = _run(json.loads(SNAPSHOT.read_text()), tmp_path)

    assert result.returncode == 0, result.stdout + result.stderr


def test_generator_check_fails_on_a_new_code(tmp_path: Path):
    row = "| `ZZ_NEW_CODE` | 400 | actionable | A code the SDK doesn't have yet. |"
    spec = _with_errors_table(lambda text: text.replace("| `AUTH_FORBIDDEN` |", f"{row}\n| `AUTH_FORBIDDEN` |", 1))

    assert _run(spec, tmp_path).returncode == 1


def _drop_rows(text: str) -> str:
    return "\n".join(line for line in text.splitlines() if not line.startswith("| `"))


def _bad_status(text: str) -> str:
    return text.replace("| `AUTH_FORBIDDEN` | 403 |", "| `AUTH_FORBIDDEN` | 4xx |")


def _duplicate(text: str) -> str:
    return text.replace("`AUTH_FORBIDDEN`", "`AUTH_EMAIL_ALREADY_REGISTERED`")


def _bad_retry(text: str) -> str:
    return text.replace("| 403 | terminal |", "| 403 | maybe |", 1)


@pytest.mark.parametrize(
    "transform,message",
    [
        (_drop_rows, "no error-code"),
        (_bad_status, "unparseable"),
        (_duplicate, "appears twice"),
        (_bad_retry, "unknown retry class"),
    ],
    ids=["empty-table", "bad-row", "duplicate", "bad-retry"],
)
def test_generator_refuses_a_broken_table(tmp_path: Path, transform: Callable[[str], str], message: str):
    result = _run(_with_errors_table(transform), tmp_path)

    assert result.returncode == 2 and message in result.stderr
