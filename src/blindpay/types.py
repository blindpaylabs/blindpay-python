from typing import Any, Dict, Generic, List, Literal, Optional, TypeVar, Union

from typing_extensions import NotRequired, TypedDict

from .error_codes import RetryClass

T = TypeVar("T")


class ErrorResponse(TypedDict):
    """The ``error`` half of every result. The SDK always fills every key; only ``message`` is typed as required
    so hand-built errors (e.g. in tests) stay valid.

    - ``status``: HTTP status, or 0 when no response arrived (network error, timeout).
    - ``code``: the API's stable UPPERCASE error code, or an ``SDK_*`` code for client-side failures.
    - ``errors``: the API's detail list (empty when absent).
    - ``request_id``: the ``X-Request-Id`` response header.
    - ``idempotency_key``: the key the request carried (yours or auto-generated). Resend with it to resume safely.
    - ``retryable``: the request may succeed if resent with the same ``idempotency_key``. For a create or payout
      that returned a 5xx, look the resource up before resending.
    - ``retry_class``: the API's classification of ``code`` (``RetryClass``), ``UNKNOWN`` for no code, an ``SDK_*``
      code or a code this SDK version doesn't know. ``retryable`` is the SDK's decision for this exact request.
    """

    message: str
    status: NotRequired[int]
    code: NotRequired[Optional[str]]
    description: NotRequired[Optional[str]]
    errors: NotRequired[List[Any]]
    trace_id: NotRequired[Optional[str]]
    request_id: NotRequired[Optional[str]]
    idempotency_key: NotRequired[Optional[str]]
    retryable: NotRequired[bool]
    retry_class: NotRequired[RetryClass]


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
    "solana",
    "solana_devnet",
    "arc",
    "arc_testnet",
    "tempo",
    "tempo_testnet",
]

StablecoinToken = Literal["USDC", "USDT", "USDB", "EURB", "EURC"]

TransactionDocumentType = Literal[
    "invoice", "purchase_order", "delivery_slip", "contract", "customs_declaration", "bill_of_lading", "others"
]

BankAccountType = Literal["checking", "saving"]

Currency = Literal["USDC", "USDT", "USDB", "BRL", "USD", "MXN", "COP", "ARS", "GBP", "EUR"]

Rail = Literal[
    "wire",
    "ach",
    "pix",
    "pix_safe",
    "spei_bitso",
    "transfers_bitso",
    "ach_cop_bitso",
    "international_swift",
    "rtp",
    "ted",
    "sepa",
    "faster_payments",
]

AccountClass = Literal["individual", "business"]

TransactionStatus = Literal["refunded", "processing", "completed", "failed", "on_hold", "pending_review"]

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

PaginationLimit = Literal["10", "50", "100", "200", "500", "1000"]
PaginationOffset = Literal["0", "10", "50", "100", "200", "500", "1000"]


class PaginationParams(TypedDict, total=False):
    """Cursor pagination. Sending any of ``limit``, ``starting_after`` or ``ending_before`` makes the API answer
    with the ``{data, pagination}`` envelope; without them some lists return a bare array of every row.

    - ``limit``: page size, an int or its string form (``10, 50, 100, 200, 500, 1000``).
    - ``starting_after``: the previous page's ``pagination.next_page``.
    - ``offset``: deprecated, ignored by the API; use ``starting_after``.
    """

    limit: Union[PaginationLimit, int]
    offset: PaginationOffset
    starting_after: str
    ending_before: str


class PaginationMetadata(TypedDict):
    has_more: bool
    next_page: NotRequired[Optional[str]]
    """Pass it as ``starting_after`` to get the next page; absent or null when ``has_more`` is false."""
    prev_page: NotRequired[Optional[str]]


class CardInstruction(TypedDict):
    """How to collect a card payin: tokenize the card with ``tokenization_key`` or send the payer to
    ``checkout_url``."""

    provider: str
    tokenization_key: str
    checkout_public_key: NotRequired[Optional[str]]
    checkout_token: NotRequired[Optional[str]]
    checkout_url: NotRequired[Optional[str]]


class TrackingTransaction(TypedDict):
    step: str
    status: NotRequired[Optional[str]]
    transaction_hash: NotRequired[Optional[str]]
    completed_at: NotRequired[Optional[str]]
    card_instruction: NotRequired[Optional[CardInstruction]]
    card_evidence: NotRequired[Optional[Dict[str, Any]]]
    card_claim_at: NotRequired[Optional[str]]
    card_failed_attempts: NotRequired[Optional[int]]
    card_gates_failed_at: NotRequired[Optional[str]]
    provider_name: NotRequired[Optional[str]]
    pse_instruction: NotRequired[Optional[Dict[str, Any]]]
    ted_instruction: NotRequired[Optional[Dict[str, Any]]]
    transfers_instruction: NotRequired[Optional[Dict[str, Any]]]
    description: NotRequired[Optional[str]]
    end_to_end_id: NotRequired[Optional[str]]
    external_id: NotRequired[Optional[str]]
    provider_transaction_id: NotRequired[Optional[str]]
    sender_account_number: NotRequired[Optional[str]]
    sender_bank_code: NotRequired[Optional[str]]
    sender_bank_name: NotRequired[Optional[str]]
    sender_name: NotRequired[Optional[str]]
    sender_tax_id: NotRequired[Optional[str]]
    trace_number: NotRequired[Optional[str]]
    transaction_reference: NotRequired[Optional[str]]
    ledger_in_transaction_id: NotRequired[Optional[str]]
    ledger_out_transaction_id: NotRequired[Optional[str]]
    provider_error_reason: NotRequired[Optional[str]]


class TrackingPayment(TypedDict):
    step: str
    provider_name: NotRequired[Optional[str]]
    provider_transaction_id: NotRequired[Optional[str]]
    provider_status: NotRequired[Optional[str]]
    estimated_time_of_arrival: NotRequired[Optional[str]]
    completed_at: NotRequired[Optional[str]]
    refund_review_reason: NotRequired[Optional[str]]
    review_context: NotRequired[Optional[Dict[str, Any]]]
    review_contexts: NotRequired[Optional[Dict[str, Any]]]
    review_sources: NotRequired[Optional[List[str]]]
    refund_review_actioned_at: NotRequired[Optional[str]]
    refund_review_detected_at: NotRequired[Optional[str]]
    returned_amount: NotRequired[Optional[int]]
    review_source: NotRequired[Optional[str]]
    approved_risk_sources: NotRequired[Optional[List[str]]]
    coelsa_id: NotRequired[Optional[str]]
    end_to_end_id: NotRequired[Optional[str]]
    provider_clearing_system: NotRequired[Optional[str]]
    provider_error_reason: NotRequired[Optional[str]]
    provider_imad: NotRequired[Optional[str]]
    provider_reference: NotRequired[Optional[str]]
    provider_uetr: NotRequired[Optional[str]]
    recipient_account_number: NotRequired[Optional[str]]
    recipient_account_type: NotRequired[Optional[str]]
    recipient_bank_code: NotRequired[Optional[str]]
    recipient_branch_code: NotRequired[Optional[str]]
    recipient_name: NotRequired[Optional[str]]
    recipient_tax_id: NotRequired[Optional[str]]


class TrackingLiquidity(TypedDict):
    step: str
    provider_transaction_id: Optional[str]
    provider_status: Optional[str]
    estimated_time_of_arrival: Optional[str]
    completed_at: Optional[str]


class TrackingComplete(TypedDict):
    step: str
    status: NotRequired[Optional[str]]
    transaction_hash: NotRequired[Optional[str]]
    completed_at: NotRequired[Optional[str]]
    provider_transaction_id: NotRequired[Optional[str]]
    refund_reason: NotRequired[Optional[str]]


class TrackingPartnerFee(TypedDict):
    step: str
    transaction_hash: str
    completed_at: str


RecipientRelationship = Literal[
    "first_party",
    "employee",
    "independent_contractor",
    "vendor_or_supplier",
    "customer",
    "subsidiary_or_affiliate",
    "merchant_or_partner",
    "landlord",
    "family",
    "other",
]

BankingPartner = Literal["cfsb", "citi", "hsbc", "jpmorgan", "portage", "ssb", "bre_b", "portage_g", "spei"]

PaymentMethod = Literal[
    "ach", "wire", "pix", "spei", "transfers", "pse", "international_swift", "rtp", "ted", "ach_pull", "bre_b", "card"
]

KycStatus = Literal["awaiting_contract", "compliance_request"]

AipriseDocumentType = Literal[
    "ADDRESS_PROOF_DOCUMENT",
    "BANK_STATEMENT_DOCUMENT",
    "OTHER",
    "SOURCE_OF_FUNDS_DOCUMENT",
    "TAX_CERTIFICATE",
    "USER_SELFIE",
    "VISA_DOCUMENT",
]

ApprovalRate = Literal["high", "low", "medium"]

ManualExecutionStatus = Literal["failed", "concluded", "pending"]
