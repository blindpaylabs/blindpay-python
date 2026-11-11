from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from ..types import ErrorResponse


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
