"""Wire-level test seam: route a client's requests through ``httpx.MockTransport`` and record them."""

import json
from typing import Any, Callable, List, Optional

import httpx

from blindpay import BlindPay, BlindPaySync
from blindpay.client import ApiClientImpl, ApiClientImplSync

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


def async_client(handler: Handler) -> BlindPay:
    client = BlindPay(api_key=API_KEY, instance_id=INSTANCE_ID)
    client._api = ApiClientImpl(client._base_url, client._headers, transport=httpx.MockTransport(handler))
    return client


def sync_client(handler: Handler) -> BlindPaySync:
    client = BlindPaySync(api_key=API_KEY, instance_id=INSTANCE_ID)
    client.close()
    client._api = ApiClientImplSync(client._base_url, client._headers, transport=httpx.MockTransport(handler))
    return client
