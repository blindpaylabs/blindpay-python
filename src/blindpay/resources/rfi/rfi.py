from typing import Dict, List, Optional, Union

from typing_extensions import Literal, NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, path_param
from ...types import BlindpayApiResponse

RfiStatus = Literal["pending", "submitted", "expired", "cancelled"]
RfiSubmitFailureReason = Literal["no_pending_rfi", "already_resolved"]
RfiCustomerType = Literal["individual", "business"]

RfiResponseMap = Dict[str, Union[str, List[str]]]
"""Answers keyed by ``RfiField.key``: a string, or a list of strings for ``multiple`` fields (file URLs from
``upload.create`` for document fields)."""


class RfiFieldItem(TypedDict):
    label: str
    value: str


class RfiField(TypedDict):
    key: str
    label: str
    regex: NotRequired[str]
    required: bool
    items: NotRequired[List[RfiFieldItem]]
    multiple: NotRequired[bool]


class RfiSection(TypedDict):
    title: str
    description: str
    supporting_document: NotRequired[str]
    fields: List[RfiField]


class InstanceRfi(TypedDict):
    """A request for information BlindPay's compliance team opened on the instance."""

    id: str
    instance_id: str
    status: Union[RfiStatus, str]
    request: List[RfiSection]
    response: RfiResponseMap
    expires_at: str
    submitted_at: Optional[str]
    created_at: str


class CustomerRfi(TypedDict):
    """A request for information BlindPay's compliance team opened on a customer."""

    id: str
    customer_id: str
    instance_id: str
    status: Union[RfiStatus, str]
    request: List[RfiSection]
    response: RfiResponseMap
    expires_at: str
    submitted_at: Optional[str]
    created_at: str
    customer_type: NotRequired[Union[RfiCustomerType, str]]
    customer_kyc_status: NotRequired[str]


class SubmitRfiResponse(TypedDict):
    """``success: False`` with a ``reason`` means there is nothing to answer: refetch with ``get`` instead of
    retrying."""

    success: bool
    reason: NotRequired[Union[RfiSubmitFailureReason, str]]


class SubmitInstanceRfiInput(TypedDict):
    response: RfiResponseMap


class SubmitCustomerRfiInput(TypedDict):
    customer_id: str
    response: RfiResponseMap


class InstanceRfiResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def get(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[Optional[InstanceRfi]]:
        """The open RFI for this instance, or ``None`` when there is none."""
        return await self._client.get(f"/instances/{self._instance_id}/rfi", options=options)

    async def submit(
        self, data: SubmitInstanceRfiInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[SubmitRfiResponse]:
        """Answers the open RFI. The answers map is the whole request body."""
        return await self._client.post(f"/instances/{self._instance_id}/rfi", data["response"], options=options)


class InstanceRfiResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def get(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[Optional[InstanceRfi]]:
        """The open RFI for this instance, or ``None`` when there is none."""
        return self._client.get(f"/instances/{self._instance_id}/rfi", options=options)

    def submit(
        self, data: SubmitInstanceRfiInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[SubmitRfiResponse]:
        """Answers the open RFI. The answers map is the whole request body."""
        return self._client.post(f"/instances/{self._instance_id}/rfi", data["response"], options=options)


class CustomerRfiResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def get(
        self, customer_id: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[Optional[CustomerRfi]]:
        """The customer's open RFI, or ``None`` when there is none."""
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/rfi", options=options
        )

    async def submit(
        self, data: SubmitCustomerRfiInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[SubmitRfiResponse]:
        """Answers the customer's open RFI; on success the customer's ``kyc_status`` goes back to ``verifying``."""
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(data['customer_id'])}/rfi",
            data["response"],
            options=options,
        )


class CustomerRfiResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def get(
        self, customer_id: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[Optional[CustomerRfi]]:
        """The customer's open RFI, or ``None`` when there is none."""
        return self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/rfi", options=options
        )

    def submit(
        self, data: SubmitCustomerRfiInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[SubmitRfiResponse]:
        """Answers the customer's open RFI; on success the customer's ``kyc_status`` goes back to ``verifying``."""
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(data['customer_id'])}/rfi",
            data["response"],
            options=options,
        )


def create_instance_rfi_resource(instance_id: str, client: InternalApiClient) -> InstanceRfiResource:
    return InstanceRfiResource(instance_id, client)


def create_instance_rfi_resource_sync(instance_id: str, client: InternalApiClientSync) -> InstanceRfiResourceSync:
    return InstanceRfiResourceSync(instance_id, client)


def create_customer_rfi_resource(instance_id: str, client: InternalApiClient) -> CustomerRfiResource:
    return CustomerRfiResource(instance_id, client)


def create_customer_rfi_resource_sync(instance_id: str, client: InternalApiClientSync) -> CustomerRfiResourceSync:
    return CustomerRfiResourceSync(instance_id, client)
