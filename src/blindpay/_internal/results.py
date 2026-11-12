"""``unwrap``: read a result's ``data`` with a type every checker agrees on."""

from typing import TypeVar, cast

from ..types import BlindpayApiResponse
from .exceptions import BlindPayApiError

T = TypeVar("T")


def unwrap(response: BlindpayApiResponse[T]) -> T:
    """Return ``response["data"]``, or raise ``BlindPayApiError`` (same fields as the error dict) if it holds an error.

    mypy narrows ``response`` after ``if response["error"] is not None: return``, but pyright/Pylance doesn't narrow
    TypedDict unions on ``is None``, so ``response["data"]`` stays ``T | None`` there. ``unwrap(response)`` is ``T``
    in both, and after an ``error`` check it never raises.
    """
    error = response["error"]
    if error is not None:
        raise BlindPayApiError(error)
    return cast(T, response["data"])
