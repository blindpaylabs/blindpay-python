from typing import Generic, Literal, TypeVar, Union

from typing_extensions import TypedDict

T = TypeVar("T")


class ErrorResponse(TypedDict):
    message: str


class BlindpayErrorResponse(TypedDict):
    data: None
    error: ErrorResponse


class BlindpaySuccessResponse(TypedDict, Generic[T]):
    data: T
    error: None


BlindpayApiResponse = Union[BlindpayErrorResponse, BlindpaySuccessResponse[T]]

CurrencyType = Literal["sender", "receiver"]

Network = Literal[
    "base",
    "sepolia",
    "arbitrum_sepolia",
    "base_sepolia",
    "arbitrum",
    "polygon",
    "polygon_amoy",
    "ethereum",
    "stellar",
    "stellar_testnet",
    "tron",
]

StablecoinToken = Literal["USDC", "USDT", "USDB"]

TransactionDocumentType = Literal[
    "invoice", "purchase_order", "delivery_slip", "contract", "customs_declaration", "bill_of_lading", "others"
]

BankAccountType = Literal["checking", "savings"]

Currency = Literal["USDC", "USDT", "USDB", "BRL", "USD", "MXN", "COP", "ARS"]

Rail = Literal["wire", "ach", "pix", "spei_bitso", "transfers_bitso", "ach_cop_bitso", "international_swift", "rtp"]

AccountClass = Literal["individual", "business"]

TransactionStatus = Literal["refunded", "processing", "completed", "failed", "on_hold"]

SpeiProtocol = Literal["clabe", "debitcard", "phonenum"]

Country = Literal[
    "AF",
    "AL",
    "DZ",
    "AS",
    "AD",
    "AO",
    "AI",
    "AQ",
    "AG",
    "AR",
    "AM",
    "AW",
    "AU",
    "AT",
    "AZ",
    "BS",
    "BH",
    "BD",
    "BB",
    "BY",
    "BE",
    "BZ",
    "BJ",
    "BM",
    "BT",
    "BO",
    "BQ",
    "BA",
    "BW",
    "BV",
    "BR",
    "IO",
    "BN",
    "BG",
    "BF",
    "BI",
    "CV",
    "KH",
    "CM",
    "CA",
    "KY",
    "CF",
    "TD",
    "CL",
    "CN",
    "CX",
    "CC",
    "CO",
    "KM",
    "CD",
    "CG",
    "CK",
    "CR",
    "HR",
    "CU",
    "CW",
    "CY",
    "CZ",
    "CI",
    "DK",
    "DJ",
    "DM",
    "DO",
    "EC",
    "EG",
    "SV",
    "GQ",
    "ER",
    "EE",
    "SZ",
    "ET",
    "FK",
    "FO",
    "FJ",
    "FI",
    "FR",
    "GF",
    "PF",
    "TF",
    "GA",
    "GM",
    "GE",
    "DE",
    "GH",
    "GI",
    "GR",
    "GL",
    "GD",
    "GP",
    "GU",
    "GT",
    "GG",
    "GN",
    "GW",
    "GY",
    "HT",
    "HM",
    "VA",
    "HN",
    "HK",
    "HU",
    "IS",
    "IN",
    "ID",
    "IR",
    "IQ",
    "IE",
    "IM",
    "IL",
    "IT",
    "JM",
    "JP",
    "JE",
    "JO",
    "KZ",
    "KE",
    "KI",
    "KP",
    "KR",
    "KW",
    "KG",
    "LA",
    "LV",
    "LB",
    "LS",
    "LR",
    "LY",
    "LI",
    "LT",
    "LU",
    "MO",
    "MG",
    "MW",
    "MY",
    "MV",
    "ML",
    "MT",
    "MH",
    "MQ",
    "MR",
    "MU",
    "YT",
    "MX",
    "FM",
    "MD",
    "MC",
    "MN",
    "ME",
    "MS",
    "MA",
    "MZ",
    "MM",
    "NA",
    "NR",
    "NP",
    "NL",
    "NC",
    "NZ",
    "NI",
    "NE",
    "NG",
    "NU",
    "NF",
    "MP",
    "NO",
    "OM",
    "PK",
    "PW",
    "PS",
    "PA",
    "PG",
    "PY",
    "PE",
    "PH",
    "PN",
    "PL",
    "PT",
    "PR",
    "QA",
    "MK",
    "RO",
    "RU",
    "RW",
    "RE",
    "BL",
    "SH",
    "KN",
    "LC",
    "MF",
    "PM",
    "VC",
    "WS",
    "SM",
    "ST",
    "SA",
    "SN",
    "RS",
    "SC",
    "SL",
    "SG",
    "SX",
    "SK",
    "SI",
    "SB",
    "SO",
    "ZA",
    "GS",
    "SS",
    "ES",
    "LK",
    "SD",
    "SR",
    "SJ",
    "SE",
    "CH",
    "SY",
    "TW",
    "TJ",
    "TZ",
    "TH",
    "TL",
    "TG",
    "TK",
    "TO",
    "TT",
    "TN",
    "TR",
    "TM",
    "TC",
    "TV",
    "UG",
    "UA",
    "AE",
    "GB",
    "UM",
    "US",
    "UY",
    "UZ",
    "VU",
    "VE",
    "VN",
    "VG",
    "VI",
    "WF",
    "EH",
    "YE",
    "ZM",
    "ZW",
    "AX",
]

PaginationLimit = Literal["10", "50", "100", "200", "1000"]
PaginationOffset = Literal["0", "10", "50", "100", "200", "1000"]


class PaginationParams(TypedDict, total=False):
    limit: PaginationLimit
    offset: PaginationOffset
    starting_after: str
    ending_before: str


class PaginationMetadata(TypedDict):
    has_more: bool
    next_page: int
    prev_page: int


class TrackingTransaction(TypedDict):
    step: str
    status: str
    transaction_hash: str
    completed_at: str


class TrackingPayment(TypedDict):
    step: str
    provider_name: str
    provider_transaction_id: str
    provider_status: str
    estimated_time_of_arrival: str
    completed_at: str


class TrackingLiquidity(TypedDict):
    step: str
    provider_transaction_id: str
    provider_status: str
    estimated_time_of_arrival: str
    completed_at: str


class TrackingComplete(TypedDict):
    step: str
    status: str
    transaction_hash: str
    completed_at: str


class TrackingPartnerFee(TypedDict):
    step: str
    transaction_hash: str
    completed_at: str
