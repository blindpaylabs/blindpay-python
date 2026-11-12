from typing import TYPE_CHECKING, Any, List, Optional

from ..error_codes import RetryClass, error_code_info

if TYPE_CHECKING:
    from ..types import ErrorResponse


def retry_class_of(code: Optional[str]) -> RetryClass:
    """The spec's retry class for ``code``; ``UNKNOWN`` for no code or one this SDK version doesn't know."""
    info = error_code_info(code)
    return info.retry if info is not None else RetryClass.UNKNOWN


class BlindPayError(Exception):
    """BlindPay SDK error"""

    def __init__(self, message: str):
        super().__init__(message)
        self.name = "BlindpayError"


class BlindPayApiError(BlindPayError):
    """An API error raised where a result dict can't be returned (auto-pagination iterators).

    Carries the same fields as ``ErrorResponse``; ``error`` holds the dict itself.
    """

    def __init__(self, error: "ErrorResponse"):
        super().__init__(error["message"])
        self.name = "BlindpayApiError"
        self.error = error
        self.status: int = error.get("status", 0)
        self.code: Optional[str] = error.get("code")
        self.description: Optional[str] = error.get("description")
        self.errors: List[Any] = error.get("errors", [])
        self.trace_id: Optional[str] = error.get("trace_id")
        self.request_id: Optional[str] = error.get("request_id")
        self.idempotency_key: Optional[str] = error.get("idempotency_key")
        self.retryable: bool = error.get("retryable", False)
        self.retry_class: RetryClass = error.get("retry_class") or retry_class_of(self.code)
