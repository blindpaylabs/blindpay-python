"""Auto-pagination shared by every ``list_auto_paging`` method, in both clients.

A pager sends ``limit`` (default 100) so the API answers with the ``{data, pagination}`` envelope, yields every item
of the page, then requests the next page with ``starting_after = pagination.next_page`` while ``has_more`` is true.
It only pages forward. Each page goes through the client's normal retry policy; an error that survives it is raised
as ``BlindPayApiError``, because an iterator can't return a result dict.
"""

from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
    cast,
)

from ..types import BlindpayApiResponse
from .exceptions import BlindPayApiError, BlindPayError

T = TypeVar("T")

DEFAULT_PAGE_SIZE = 100

PageFetcher = Callable[[Any], BlindpayApiResponse[Any]]
AsyncPageFetcher = Callable[[Any], Awaitable[BlindpayApiResponse[Any]]]


def _first_page_params(params: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    query = {key: value for key, value in (params or {}).items() if value is not None}
    if query.pop("ending_before", None):
        raise BlindPayError("list_auto_paging only pages forward; pass starting_after, not ending_before")
    query.setdefault("limit", DEFAULT_PAGE_SIZE)
    return query


def _read_page(response: BlindpayApiResponse[Any]) -> Tuple[List[Any], Optional[str]]:
    if response["error"] is not None:
        raise BlindPayApiError(response["error"])
    page: object = response["data"]
    if isinstance(page, list):
        return cast(List[Any], page), None  # bare array: the whole collection in one response
    if not isinstance(page, dict):
        return [], None
    envelope = cast(Dict[str, Any], page)
    pagination = cast(Dict[str, Any], envelope.get("pagination") or {})
    cursor: object = pagination.get("next_page") if pagination.get("has_more") else None
    items = cast(List[Any], envelope.get("data") or [])
    return items, cursor if isinstance(cursor, str) and cursor else None


def auto_paging_iter(fetch: PageFetcher, params: Optional[Mapping[str, Any]]) -> Iterator[Any]:
    """Validates ``params`` now (not on the first ``next()``) and returns the item iterator."""
    query = _first_page_params(params)

    def items() -> Iterator[Any]:
        page_query = query
        while True:
            page, cursor = _read_page(fetch(page_query))
            yield from page
            if cursor is None:
                return
            page_query = {**page_query, "starting_after": cursor}

    return items()


def async_auto_paging_iter(fetch: AsyncPageFetcher, params: Optional[Mapping[str, Any]]) -> AsyncIterator[Any]:
    """Async twin of ``auto_paging_iter``: validates ``params`` now and returns an async item iterator."""
    query = _first_page_params(params)

    async def items() -> AsyncIterator[Any]:
        page_query = query
        while True:
            page, cursor = _read_page(await fetch(page_query))
            for item in page:
                yield item
            if cursor is None:
                return
            page_query = {**page_query, "starting_after": cursor}

    return items()
