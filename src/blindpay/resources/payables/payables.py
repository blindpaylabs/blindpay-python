from typing import Any, AsyncIterator, Dict, Iterator, List, Optional, Union

from typing_extensions import Literal, NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, build_query, path_param
from ..._internal.pagination import async_auto_paging_iter, auto_paging_iter
from ...types import BlindpayApiResponse, Currency, PaginationMetadata, PaginationParams

PayableStatus = Literal["draft", "processing", "completed", "canceled"]
PayableType = Literal["boleto", "pix_code", "invoice"]
PayableLastAttemptStatus = Literal["failed", "refunded"]
PayableBankAccountType = Literal["ach", "wire"]


class PayableParty(TypedDict):
    legal_name: NotRequired[Optional[str]]
    address_line_1: NotRequired[Optional[str]]
    address_line_2: NotRequired[Optional[str]]
    city: NotRequired[Optional[str]]
    state_province_region: NotRequired[Optional[str]]
    postal_code: NotRequired[Optional[str]]
    country: NotRequired[Optional[str]]
    tax_id: NotRequired[Optional[str]]


class PayableLineItem(TypedDict):
    name: str
    quantity: int
    price: Optional[int]
    """Unit price in cents."""


class PayableBankAccount(TypedDict):
    type: Union[PayableBankAccountType, str]
    beneficiary_name: NotRequired[Optional[str]]
    routing_number: NotRequired[Optional[str]]
    account_number: NotRequired[Optional[str]]
    account_type: NotRequired[Optional[str]]


# "from" is a Python keyword, so the wire key lives in a functional TypedDict base.
_PayableFrom = TypedDict("_PayableFrom", {"from": NotRequired[Optional[PayableParty]]})


class Payable(_PayableFrom):
    """A bill to pay (boleto, PIX code or invoice). Amounts are integer cents."""

    id: str
    instance_id: str
    customer_id: str
    to: NotRequired[Optional[PayableParty]]
    currency: Union[Currency, str]
    line_items: NotRequired[List[PayableLineItem]]
    note: NotRequired[Optional[str]]
    discount: NotRequired[Optional[int]]
    taxes: NotRequired[Optional[int]]
    boleto_barcode: NotRequired[Optional[str]]
    pix_qrcode: NotRequired[Optional[str]]
    document_file: NotRequired[Optional[str]]
    due_date: NotRequired[Optional[str]]
    scheduled_at: NotRequired[Optional[str]]
    status: Union[PayableStatus, str]
    created_at: NotRequired[Optional[str]]
    updated_at: NotRequired[Optional[str]]
    amount: Optional[int]
    payout_id: NotRequired[Optional[str]]
    bank_account: NotRequired[Optional[PayableBankAccount]]
    last_attempt_status: NotRequired[Optional[Union[PayableLastAttemptStatus, str]]]
    first_name: NotRequired[Optional[str]]
    last_name: NotRequired[Optional[str]]
    legal_name: NotRequired[Optional[str]]


class CreatePayableInput(_PayableFrom):
    """Pass at least one of ``boleto_barcode``, ``pix_qrcode`` or ``document_file`` (or line items). Amounts
    (``line_items[].price``, ``discount``, ``taxes``) are integer cents. ``bank_account`` takes the same fields as a
    bank-account create body."""

    customer_id: str
    currency: Currency
    to: NotRequired[Optional[PayableParty]]
    line_items: NotRequired[List[PayableLineItem]]
    note: NotRequired[Optional[str]]
    discount: NotRequired[Optional[int]]
    taxes: NotRequired[Optional[int]]
    boleto_barcode: NotRequired[Optional[str]]
    pix_qrcode: NotRequired[Optional[str]]
    document_file: NotRequired[Optional[str]]
    due_date: NotRequired[Optional[str]]
    scheduled_at: NotRequired[Optional[str]]
    bank_account: NotRequired[Optional[Dict[str, Any]]]


class ListPayablesInput(PaginationParams, total=False):
    status: PayableStatus
    customer_id: str
    customer_name: str
    type: PayableType
    beneficiary_name: str


class ListPayablesResponse(TypedDict):
    data: List[Payable]
    pagination: PaginationMetadata


class PayablesResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def create(
        self, data: CreatePayableInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[Payable]:
        return await self._client.post(f"/instances/{self._instance_id}/payables", data, options=options)

    async def list(
        self, params: Optional[ListPayablesInput] = None, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[Union[ListPayablesResponse, List[Payable]]]:
        query_string = build_query(params)
        return await self._client.get(f"/instances/{self._instance_id}/payables{query_string}", options=options)

    def list_auto_paging(self, params: Optional[ListPayablesInput] = None) -> AsyncIterator[Payable]:
        return async_auto_paging_iter(self.list, params)

    async def get(self, payable_id: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[Payable]:
        return await self._client.get(
            f"/instances/{self._instance_id}/payables/{path_param(payable_id)}", options=options
        )

    async def delete(self, payable_id: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[Payable]:
        return await self._client.delete(
            f"/instances/{self._instance_id}/payables/{path_param(payable_id)}", options=options
        )


class PayablesResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def create(
        self, data: CreatePayableInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[Payable]:
        return self._client.post(f"/instances/{self._instance_id}/payables", data, options=options)

    def list(
        self, params: Optional[ListPayablesInput] = None, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[Union[ListPayablesResponse, List[Payable]]]:
        query_string = build_query(params)
        return self._client.get(f"/instances/{self._instance_id}/payables{query_string}", options=options)

    def list_auto_paging(self, params: Optional[ListPayablesInput] = None) -> Iterator[Payable]:
        return auto_paging_iter(self.list, params)

    def get(self, payable_id: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[Payable]:
        return self._client.get(f"/instances/{self._instance_id}/payables/{path_param(payable_id)}", options=options)

    def delete(self, payable_id: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[Payable]:
        return self._client.delete(f"/instances/{self._instance_id}/payables/{path_param(payable_id)}", options=options)


def create_payables_resource(instance_id: str, client: InternalApiClient) -> PayablesResource:
    return PayablesResource(instance_id, client)


def create_payables_resource_sync(instance_id: str, client: InternalApiClientSync) -> PayablesResourceSync:
    return PayablesResourceSync(instance_id, client)
