"""Wire-level test seam: route a client's requests through ``httpx.MockTransport`` and record them."""

import json
from typing import Any, Callable, List, Optional

import httpx

from blindpay import BlindPay, BlindPaySync

API_KEY = "test_key"
INSTANCE_ID = "in_000000000000"


class Recorder:
    def __init__(self, status: int = 200, body: Any = None, raw: Optional[bytes] = None) -> None:
        self.requests: List[httpx.Request] = []
        self._status = status
        self._content = raw if raw is not None else json.dumps(body if body is not None else {}).encode()

    def __call__(self, request: httpx.Request) -> httpx.Response:
        request.read()
        self.requests.append(request)
        return httpx.Response(self._status, content=self._content, headers={"Content-Type": "application/json"})

    @property
    def last(self) -> httpx.Request:
        assert self.requests, "no request was sent"
        return self.requests[-1]


Handler = Callable[[httpx.Request], httpx.Response]


def async_client(handler: Handler, **settings: Any) -> BlindPay:
    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return BlindPay(api_key=API_KEY, instance_id=INSTANCE_ID, http_client=http_client, **settings)


def sync_client(handler: Handler, **settings: Any) -> BlindPaySync:
    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    return BlindPaySync(api_key=API_KEY, instance_id=INSTANCE_ID, http_client=http_client, **settings)
