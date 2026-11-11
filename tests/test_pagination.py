"""List envelopes (bare array or {data, pagination}) and the ``list_auto_paging`` pagers, in both clients."""

import json
from typing import Any, Callable, Dict, List, Optional
from urllib.parse import parse_qs

import httpx
import pytest

from blindpay import BlindPayApiError, BlindPayError
from tests.http_mock import async_client, sync_client

PAGINATION_END = {"has_more": False, "next_page": None, "prev_page": None}

# accessor name on the client -> path segment of its list route
PAGERS = {
    "payables": "payables",
    "payouts": "payouts",
    "payins": "payins",
    "customers": "customers",
    "transfers": "transfers",
}


class Pages:
    """Serves ``pages`` as an envelope keyed by ``starting_after``, recording every query."""

    def __init__(self, pages: List[List[str]], fail_on_page: Optional[int] = None) -> None:
        self.pages = pages
        self.fail_on_page = fail_on_page
        self.queries: List[Dict[str, List[str]]] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        query = parse_qs(request.url.query.decode())
        self.queries.append(query)
        cursor = query.get("starting_after", [None])[0]
        index = 0 if cursor is None else next(i + 1 for i, page in enumerate(self.pages) if page[-1] == cursor)
        if index == self.fail_on_page:
            body = {"success": False, "code": "INTERNAL_ERROR", "message": "internal_error"}
            return httpx.Response(400, content=json.dumps(body).encode())
        has_more = index < len(self.pages) - 1
        envelope = {
            "data": [{"id": item} for item in self.pages[index]],
            "pagination": {
                "has_more": has_more,
                "next_page": self.pages[index][-1] if has_more else None,
                "prev_page": cursor,
            },
        }
        return httpx.Response(200, content=json.dumps(envelope).encode())


async def collect(
    kind: str, handler: Callable[[httpx.Request], httpx.Response], resource: str, params: Any
) -> List[str]:
    if kind == "async":
        client: Any = async_client(handler)
        return [item["id"] async for item in getattr(client, resource).list_auto_paging(params)]
    client = sync_client(handler)
    return [item["id"] for item in getattr(client, resource).list_auto_paging(params)]


@pytest.mark.parametrize("kind", ["async", "sync"])
@pytest.mark.parametrize("resource", sorted(PAGERS))
class TestAutoPaging:
    async def test_follows_next_page_while_has_more(self, kind: str, resource: str):
        pages = Pages([["a1", "a2"], ["b1", "b2"], ["c1"]])

        ids = await collect(kind, pages, resource, None)

        assert ids == ["a1", "a2", "b1", "b2", "c1"]
        assert [q.get("starting_after") for q in pages.queries] == [None, ["a2"], ["b2"]]
        assert all(q["limit"] == ["100"] for q in pages.queries)

    async def test_keeps_filters_and_caller_limit_on_every_page(self, kind: str, resource: str):
        pages = Pages([["a1"], ["b1"]])

        await collect(kind, pages, resource, {"limit": 10, "customer_id": "cu_000000000000", "status": None})

        for query in pages.queries:
            assert query["limit"] == ["10"]
            assert query["customer_id"] == ["cu_000000000000"]
            assert "status" not in query

    async def test_starts_after_the_caller_cursor(self, kind: str, resource: str):
        pages = Pages([["a1"], ["b1"]])

        ids = await collect(kind, pages, resource, {"starting_after": "a1"})

        assert ids == ["b1"]

    async def test_error_page_raises_with_the_api_error(self, kind: str, resource: str):
        pages = Pages([["a1"], ["b1"]], fail_on_page=1)

        with pytest.raises(BlindPayApiError) as raised:
            await collect(kind, pages, resource, None)

        assert raised.value.status == 400
        assert raised.value.code == "INTERNAL_ERROR"

    async def test_ending_before_is_rejected_before_any_request(self, kind: str, resource: str):
        pages = Pages([["a1"]])
        client: Any = async_client(pages) if kind == "async" else sync_client(pages)

        with pytest.raises(BlindPayError, match="forward"):
            getattr(client, resource).list_auto_paging({"ending_before": "a1"})

        assert pages.queries == []

    async def test_bare_array_is_yielded_whole(self, kind: str, resource: str):
        def bare(_request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, content=json.dumps([{"id": "a1"}, {"id": "a2"}]).encode())

        assert await collect(kind, bare, resource, None) == ["a1", "a2"]


@pytest.mark.parametrize("kind", ["async", "sync"])
class TestListShapes:
    async def test_list_returns_both_envelope_and_bare_array(self, kind: str):
        responses = [
            httpx.Response(200, content=b'[{"id": "po_1"}]'),
            httpx.Response(200, content=json.dumps({"data": [{"id": "po_1"}], "pagination": PAGINATION_END}).encode()),
        ]

        def serve(_request: httpx.Request) -> httpx.Response:
            return responses.pop(0)

        client: Any = async_client(serve) if kind == "async" else sync_client(serve)

        bare = client.payouts.list()
        paged = client.payouts.list({"limit": 10})
        if kind == "async":
            bare, paged = await bare, await paged

        assert bare["data"] == [{"id": "po_1"}]
        assert paged["data"]["pagination"]["has_more"] is False

    async def test_pager_pages_go_through_the_retry_policy(self, kind: str):
        pages = Pages([["a1"]])
        calls: List[int] = []

        def flaky(request: httpx.Request) -> httpx.Response:
            calls.append(1)
            return httpx.Response(503) if len(calls) == 1 else pages(request)

        client: Any = async_client(flaky) if kind == "async" else sync_client(flaky)
        if kind == "async":

            async def no_sleep(_seconds: float) -> None:
                return None

            client._api._sleep = no_sleep
            ids = [p["id"] async for p in client.payouts.list_auto_paging()]
        else:
            sleeps: List[float] = []
            client._api._sleep = sleeps.append
            ids = [p["id"] for p in client.payouts.list_auto_paging()]

        assert ids == ["a1"]
        assert len(calls) == 2


@pytest.mark.parametrize("kind", ["async", "sync"])
class TestWalletDeposits:
    async def test_get_deposits_auto_paging_follows_the_cursor_and_keeps_filters(self, kind: str):
        pages = Pages([["d1", "d2"], ["d3"]])
        params = {"customer_id": "cu_000000000000", "id": "wa_000000000000", "token": "USDC"}

        if kind == "async":
            client: Any = async_client(pages)
            ids = [d["id"] async for d in client.wallets.custodial.get_deposits_auto_paging(params)]
        else:
            client = sync_client(pages)
            ids = [d["id"] for d in client.wallets.custodial.get_deposits_auto_paging(params)]

        assert ids == ["d1", "d2", "d3"]
        assert [q.get("starting_after") for q in pages.queries] == [None, ["d2"]]
        assert all(q["token"] == ["USDC"] and q["limit"] == ["100"] for q in pages.queries)
        assert all("customer_id" not in q and "id" not in q for q in pages.queries)
