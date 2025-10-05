from typing import Any, Dict, Optional, Protocol

from ..types import BlindpayApiResponse


class InternalApiClient(Protocol):
    """
    Internal API client interface that resources use to make HTTP requests.
    This interface is not exposed to SDK users.
    """

    async def get(self, path: str) -> BlindpayApiResponse[Any]:
        """Make a GET request"""
        ...

    async def post(self, path: str, body: Dict[str, Any]) -> BlindpayApiResponse[Any]:
        """Make a POST request"""
        ...

    async def put(self, path: str, body: Dict[str, Any]) -> BlindpayApiResponse[Any]:
        """Make a PUT request"""
        ...

    async def patch(self, path: str, body: Dict[str, Any]) -> BlindpayApiResponse[Any]:
        """Make a PATCH request"""
        ...

    async def delete(self, path: str, body: Optional[Dict[str, Any]] = None) -> BlindpayApiResponse[Any]:
        """Make a DELETE request"""
        ...


class InternalApiClientSync(Protocol):
    """Synchronous version of InternalApiClient"""

    def get(self, path: str) -> BlindpayApiResponse[Any]:
        """Make a GET request"""
        ...

    def post(self, path: str, body: Dict[str, Any]) -> BlindpayApiResponse[Any]:
        """Make a POST request"""
        ...

    def put(self, path: str, body: Dict[str, Any]) -> BlindpayApiResponse[Any]:
        """Make a PUT request"""
        ...

    def patch(self, path: str, body: Dict[str, Any]) -> BlindpayApiResponse[Any]:
        """Make a PATCH request"""
        ...

    def delete(self, path: str, body: Optional[Dict[str, Any]] = None) -> BlindpayApiResponse[Any]:
        """Make a DELETE request"""
        ...
