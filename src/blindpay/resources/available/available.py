from typing import List, Literal, Optional, Union

from typing_extensions import NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, build_query, path_param
from ...types import BlindpayApiResponse, Rail

BankDetailKey = Literal[
    "type",
    "name",
    "pix_key",
    "beneficiary_name",
    "routing_number",
    "account_number",
    "account_type",
    "account_class",
    "address_line_1",
    "address_line_2",
    "city",
    "state_province_region",
    "country",
    "postal_code",
    "checkbook_account_id",
    "checkbook_user_key",
    "spei_protocol",
    "spei_institution_code",
    "spei_clabe",
    "transfers_type",
    "transfers_account",
    "ach_cop_beneficiary_first_name",
    "ach_cop_beneficiary_last_name",
    "ach_cop_document_id",
    "ach_cop_document_type",
    "ach_cop_email",
    "ach_cop_bank_code",
    "ach_cop_bank_account",
    "swift_code_bic",
    "swift_account_holder_name",
    "swift_account_number_iban",
    "swift_beneficiary_address_line_1",
    "swift_beneficiary_address_line_2",
    "swift_beneficiary_country",
    "swift_beneficiary_city",
    "swift_beneficiary_state_province_region",
    "swift_beneficiary_postal_code",
    "swift_bank_name",
    "swift_bank_address_line_1",
    "swift_bank_address_line_2",
    "swift_bank_country",
    "swift_bank_city",
    "swift_bank_state_province_region",
    "swift_bank_postal_code",
    "swift_intermediary_bank_swift_code_bic",
    "swift_intermediary_bank_account_number_iban",
    "swift_intermediary_bank_name",
    "swift_intermediary_bank_country",
]


class BankDetailItem(TypedDict):
    label: str
    value: str
    is_active: Optional[bool]


class BankDetail(TypedDict):
    label: str
    regex: str
    key: Union[BankDetailKey, str]
    items: NotRequired[Optional[List[BankDetailItem]]]
    required: NotRequired[Optional[bool]]


class RailInfo(TypedDict):
    label: str
    value: Union[Rail, str]
    country: str


GetBankDetailsResponse = List[BankDetail]
GetRailsResponse = List[RailInfo]


class SwiftCodeBankDetail(TypedDict):
    id: str
    bank: str
    city: str
    branch: str
    swiftCode: str
    swiftCodeLink: str
    country: str
    countrySlug: str


GetSwiftCodeBankDetailsResponse = List[SwiftCodeBankDetail]


class NaicsCode(TypedDict):
    code: NotRequired[str]
    title: NotRequired[str]


GetNaicsCodesResponse = List[NaicsCode]


class AvailableResource:
    def __init__(self, client: InternalApiClient):
        self._client = client

    async def get_bank_details(
        self, rail: Rail, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[GetBankDetailsResponse]:
        return await self._client.get(f"/available/bank-details{build_query({'rail': rail})}", options=options)

    async def get_rails(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[GetRailsResponse]:
        return await self._client.get("/available/rails", options=options)

    async def get_swift_code_bank_details(
        self, swift: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[GetSwiftCodeBankDetailsResponse]:
        return await self._client.get(f"/available/swift/{path_param(swift)}", options=options)

    async def get_naics_codes(
        self, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[GetNaicsCodesResponse]:
        return await self._client.get("/available/naics", options=options)


class AvailableResourceSync:
    """Synchronous version of AvailableResource"""

    def __init__(self, client: InternalApiClientSync):
        self._client = client

    def get_bank_details(
        self, rail: Rail, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[GetBankDetailsResponse]:
        return self._client.get(f"/available/bank-details{build_query({'rail': rail})}", options=options)

    def get_rails(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[GetRailsResponse]:
        return self._client.get("/available/rails", options=options)

    def get_swift_code_bank_details(
        self, swift: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[GetSwiftCodeBankDetailsResponse]:
        return self._client.get(f"/available/swift/{path_param(swift)}", options=options)

    def get_naics_codes(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[GetNaicsCodesResponse]:
        return self._client.get("/available/naics", options=options)


def create_available_resource(client: InternalApiClient) -> AvailableResource:
    return AvailableResource(client)


def create_available_resource_sync(client: InternalApiClientSync) -> AvailableResourceSync:
    return AvailableResourceSync(client)
