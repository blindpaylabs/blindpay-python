"""Transport policy shared by the sync and async clients: request options, idempotency keys, the retry decision
table, and how responses become ``BlindpayApiResponse`` dicts.

Everything here is pure (no I/O), so both clients run the same rules and tests can exercise them directly.
"""

import json
import random
import uuid
from typing import Any, Dict, List, Mapping, Optional, Tuple, cast
from urllib.parse import quote, urlencode

import httpx
from typing_extensions import Literal, TypedDict

from ..types import BlindpayApiResponse, ErrorResponse
from .exceptions import BlindPayError

HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]

DEFAULT_BASE_URL = "https://api.blindpay.com"
DEFAULT_TIMEOUT = 60.0
DEFAULT_MAX_RETRIES = 2

MAX_IDEMPOTENCY_KEY_LENGTH = 255
MAX_RETRY_AFTER_SECONDS = 60
MUTATING_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})
RETRYABLE_GET_STATUSES = frozenset({408, 500, 502, 503, 504})
RETRYABLE_ERROR_STATUSES = frozenset({408, 429, 500, 502, 503, 504})
# 5xx codes the spec's error table classifies as terminal (never retried, never flagged retryable).
TERMINAL_5XX_CODES = frozenset({"PAYINS_CARD_PAYMENT_PENDING"})
IDEMPOTENCY_IN_FLIGHT = "idempotency_key_in_flight"
PROTECTED_HEADERS = frozenset({"authorization", "user-agent", "idempotency-key"})

NETWORK_ERRORS = (httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError)
CONNECT_ERRORS = (httpx.ConnectError, httpx.ConnectTimeout)


class RequestOptions(TypedDict, total=False):
    """Per-request options, accepted as the trailing ``options`` argument of every mutating method.

    - ``idempotency_key``: sent as ``Idempotency-Key`` (1-255 characters). When omitted and retries are on, the
      SDK generates a UUIDv4 before the first attempt, so a retried request can't execute twice. Ignored for
      multipart uploads, which the API never deduplicates.
    - ``timeout``: per-attempt timeout in seconds, overriding the client's.
    - ``headers``: extra headers for this request only.
    """

    idempotency_key: str
    timeout: float
    headers: Mapping[str, str]


def api_root(base_url: str) -> str:
    """``https://api.blindpay.com`` (or a proxy) -> the ``/v1`` root every resource path hangs off."""
    root = base_url.rstrip("/")
    if root.endswith("/v1"):
        root = root[: -len("/v1")]
    return f"{root}/v1"


def path_param(value: object) -> str:
    """Percent-encodes one path segment, so an id can never change the route (``a/b`` -> ``a%2Fb``)."""
    return quote(str(value), safe="")


def _query_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def build_query(params: Optional[Mapping[str, Any]]) -> str:
    """``?key=value&...`` for the params that are set, in insertion order, or ``""`` when none are.

    ``None`` and ``""`` are dropped (never sent as ``"None"``, ``"null"`` or an empty value), booleans become
    ``true``/``false`` and numbers their decimal form (``limit=10``). The one query helper every list method and
    auto-pager uses.
    """
    if not params:
        return ""
    pairs = [(key, _query_value(value)) for key, value in params.items() if value is not None and value != ""]
    return f"?{urlencode(pairs)}" if pairs else ""


def is_mutating(method: str) -> bool:
    return method in MUTATING_METHODS


def resolve_idempotency_key(
    method: str, options: Optional[RequestOptions], *, multipart: bool, max_retries: int
) -> Optional[str]:
    if not is_mutating(method) or multipart:
        return None
    key = cast(object, options.get("idempotency_key") if options else None)
    if key is not None:
        valid = (
            isinstance(key, str)
            and key.strip() == key != ""
            and len(key) <= MAX_IDEMPOTENCY_KEY_LENGTH
            and key.isascii()
            and key.isprintable()
        )
        if not valid:
            # The API silently ignores an empty key and rejects one over 255 characters; a padded key would be
            # trimmed in transit, so it could match a different stored request. None of them is ever sent.
            raise BlindPayError(
                "idempotency_key must be 1-255 printable ASCII characters with no leading or trailing whitespace"
            )
        return cast(str, key)
    return str(uuid.uuid4()) if max_retries > 0 else None


def build_headers(
    base: Mapping[str, str], options: Optional[RequestOptions], idempotency_key: Optional[str], *, json_body: bool
) -> Dict[str, str]:
    headers = dict(base)
    extra = options.get("headers") if options else None
    for name, value in (extra or {}).items():
        lowered = name.lower()
        if lowered in PROTECTED_HEADERS:
            raise BlindPayError(
                f"The {name} header is set by the client"
                + ("; pass idempotency_key in the request options instead" if lowered == "idempotency-key" else "")
            )
        for existing in [k for k in headers if k.lower() == lowered]:
            del headers[existing]  # header names are case-insensitive: replace, never duplicate
        headers[name] = value
    if json_body:
        headers["Content-Type"] = "application/json"
    if idempotency_key:
        headers["Idempotency-Key"] = idempotency_key
    return headers


def encode_json(body: Any) -> bytes:
    # Serialized once and resent byte-for-byte: the API hashes the raw body to match idempotent retries.
    return json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def request_timeout(options: Optional[RequestOptions], default: float) -> httpx.Timeout:
    timeout = options.get("timeout") if options else None
    return httpx.Timeout(default if timeout is None else timeout)


def backoff(attempt: int, jitter: Optional[float] = None) -> float:
    factor = random.uniform(0.5, 1.0) if jitter is None else jitter
    return min(8.0, 0.5 * 2.0**attempt) * factor


def parse_retry_after(value: Optional[str]) -> Optional[int]:
    if value is None:
        return None
    value = value.strip()
    return int(value) if value.isascii() and value.isdigit() else None


def _retry_after_or_backoff(response: httpx.Response, attempt: int) -> float:
    retry_after = parse_retry_after(response.headers.get("Retry-After"))
    if retry_after is not None and retry_after <= MAX_RETRY_AFTER_SECONDS:
        return float(retry_after)
    return backoff(attempt)


def _json_body(response: httpx.Response) -> Optional[Dict[str, Any]]:
    try:
        body = response.json()
    except ValueError:
        return None
    return cast(Dict[str, Any], body) if isinstance(body, dict) else None


def _is_in_flight(response: httpx.Response) -> bool:
    body = _json_body(response)
    return response.status_code == 409 and body is not None and body.get("message") == IDEMPOTENCY_IN_FLIGHT


def _error_code(response: httpx.Response) -> Optional[str]:
    body = _json_body(response)
    code = body.get("code") if body else None
    return code if isinstance(code, str) else None


def response_retry_delay(
    response: httpx.Response, *, method: str, idempotency_key: Optional[str], multipart: bool, attempt: int
) -> Optional[float]:
    """Seconds to wait before retrying this response, or None if it must not be retried."""
    if multipart:
        return None
    mutating = is_mutating(method)
    if mutating and not idempotency_key:
        return None
    status = response.status_code
    if _is_in_flight(response) or status == 429:
        return _retry_after_or_backoff(response, attempt)
    if mutating:
        # The API releases the idempotency key on any 5xx, so a same-key retry would run the handler again.
        return None
    if status >= 500 and _error_code(response) in TERMINAL_5XX_CODES:
        return None
    if status in RETRYABLE_GET_STATUSES:
        return _retry_after_or_backoff(response, attempt)
    return None


def exception_retry_delay(
    error: Exception, *, method: str, idempotency_key: Optional[str], multipart: bool, attempt: int
) -> Optional[float]:
    """Seconds to wait before retrying after a transport error, or None if it must not be retried."""
    if multipart:
        # Only a failure to connect proves nothing was sent; anything later may have reached the API.
        return backoff(attempt) if isinstance(error, CONNECT_ERRORS) else None
    if is_mutating(method) and not idempotency_key:
        return None
    return backoff(attempt) if isinstance(error, NETWORK_ERRORS) else None


def body_read_failure(
    response: httpx.Response,
    error: Exception,
    *,
    method: str,
    idempotency_key: Optional[str],
    multipart: bool,
    attempt: int,
) -> Tuple[Optional[float], ErrorResponse]:
    """The status line arrived but the body couldn't be read. The server answered, so for a mutation this is not
    "no response": after a 5xx the API has already released the idempotency key, so resending would run the
    operation again. Only GETs are retried. Returns (delay or None, the error to return if not retrying)."""
    delay = (
        None
        if multipart or is_mutating(method)
        else exception_retry_delay(
            error, method=method, idempotency_key=idempotency_key, multipart=multipart, attempt=attempt
        )
    )
    return delay, {
        "message": f"The response body couldn't be read: {error or type(error).__name__}",
        "status": response.status_code,
        "code": "SDK_RESPONSE_READ_ERROR",
        "description": None,
        "errors": [],
        "trace_id": None,
        "request_id": response.headers.get("X-Request-Id"),
        "idempotency_key": idempotency_key,
        "retryable": True,
    }


def _is_retryable_error(status: int, code: Optional[str], in_flight: bool) -> bool:
    if code in TERMINAL_5XX_CODES:
        return False
    return in_flight or status in RETRYABLE_ERROR_STATUSES


def error_from_response(response: httpx.Response, idempotency_key: Optional[str]) -> ErrorResponse:
    body = _json_body(response) or {}
    message = body.get("message")
    code = body.get("code")
    errors = body.get("errors")
    status = response.status_code
    code_value = code if isinstance(code, str) else None
    description = body.get("description")
    trace_id = body.get("trace_id")
    return {
        "message": message if isinstance(message, str) and message else (response.reason_phrase or f"HTTP {status}"),
        "status": status,
        "code": code_value,
        "description": description if isinstance(description, str) else None,
        "errors": cast(List[Any], errors) if isinstance(errors, list) else [],
        "trace_id": trace_id if isinstance(trace_id, str) else None,
        "request_id": response.headers.get("X-Request-Id"),
        "idempotency_key": idempotency_key,
        "retryable": _is_retryable_error(status, code_value, _is_in_flight(response)),
    }


def error_from_exception(error: Exception, idempotency_key: Optional[str]) -> ErrorResponse:
    timeout = isinstance(error, httpx.TimeoutException)
    network = timeout or isinstance(error, (httpx.NetworkError, httpx.RemoteProtocolError))
    return {
        "message": str(error) or type(error).__name__,
        "status": 0,
        "code": "SDK_TIMEOUT" if timeout else ("SDK_CONNECTION_ERROR" if network else "SDK_ERROR"),
        "description": None,
        "errors": [],
        "trace_id": None,
        "request_id": None,
        "idempotency_key": idempotency_key,
        "retryable": network,
    }


def success_from_response(response: httpx.Response, idempotency_key: Optional[str]) -> BlindpayApiResponse[Any]:
    if not response.content:
        return {"data": None, "error": None}
    try:
        return {"data": response.json(), "error": None}
    except ValueError:
        return {
            "data": None,
            "error": {
                "message": "The API returned a response that isn't valid JSON",
                "status": response.status_code,
                "code": "SDK_INVALID_RESPONSE",
                "description": None,
                "errors": [],
                "trace_id": None,
                "request_id": response.headers.get("X-Request-Id"),
                "idempotency_key": idempotency_key,
                "retryable": False,
            },
        }
