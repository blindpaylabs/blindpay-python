from typing import IO, Any, Mapping, Optional, Protocol, Tuple, Union

from ..types import BlindpayApiResponse

MultipartFile = Tuple[str, Union[bytes, IO[bytes]], str]
"""A multipart file part: (filename, content, content type)."""


class InternalApiClient(Protocol):
    """
    Internal API client interface that resources use to make HTTP requests.
    This interface is not exposed to SDK users.
    """

    async def get(self, path: str) -> BlindpayApiResponse[Any]:
        """Make a GET request"""
        ...

    async def post(self, path: str, body: Mapping[str, Any]) -> BlindpayApiResponse[Any]:
        """Make a POST request"""
        ...

    async def put(self, path: str, body: Mapping[str, Any]) -> BlindpayApiResponse[Any]:
        """Make a PUT request"""
        ...

    async def patch(self, path: str, body: Mapping[str, Any]) -> BlindpayApiResponse[Any]:
        """Make a PATCH request"""
        ...

    async def delete(self, path: str, body: Optional[Mapping[str, Any]] = None) -> BlindpayApiResponse[Any]:
        """Make a DELETE request"""
        ...

    async def post_multipart(
        self, path: str, data: Mapping[str, str], files: Mapping[str, MultipartFile]
    ) -> BlindpayApiResponse[Any]:
        """Make a multipart/form-data POST request"""
        ...


class InternalApiClientSync(Protocol):
    """Synchronous version of InternalApiClient"""

    def get(self, path: str) -> BlindpayApiResponse[Any]:
        """Make a GET request"""
        ...

    def post(self, path: str, body: Mapping[str, Any]) -> BlindpayApiResponse[Any]:
        """Make a POST request"""
        ...

    def put(self, path: str, body: Mapping[str, Any]) -> BlindpayApiResponse[Any]:
        """Make a PUT request"""
        ...

    def patch(self, path: str, body: Mapping[str, Any]) -> BlindpayApiResponse[Any]:
        """Make a PATCH request"""
        ...

    def delete(self, path: str, body: Optional[Mapping[str, Any]] = None) -> BlindpayApiResponse[Any]:
        """Make a DELETE request"""
        ...

    def post_multipart(
        self, path: str, data: Mapping[str, str], files: Mapping[str, MultipartFile]
    ) -> BlindpayApiResponse[Any]:
        """Make a multipart/form-data POST request"""
        ...
