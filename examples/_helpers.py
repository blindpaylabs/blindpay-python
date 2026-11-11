"""Shared by the examples: turn a ``{data, error}`` result into the data, or raise with the API's error."""

from typing import TypeVar

from blindpay import BlindpayApiResponse

T = TypeVar("T")


def unwrap(response: BlindpayApiResponse[T]) -> T:
    error = response["error"]
    if error is not None:
        raise RuntimeError(f"{error.get('code')}: {error['message']} (request {error.get('request_id')})")
    data = response["data"]
    assert data is not None
    return data
