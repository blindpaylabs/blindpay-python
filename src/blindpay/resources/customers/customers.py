from typing import AsyncIterator, Iterator, List, Optional, Union

from typing_extensions import Literal, NotRequired, TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, build_query, path_param
from ..._internal.pagination import async_auto_paging_iter, auto_paging_iter
from ...types import (
    BlindpayApiResponse,
    Country,
    PaginationMetadata,
    PaginationParams,
)

IndividualType = Literal["individual"]
BusinessType = Literal["business"]
StandardKycType = Literal["standard"]
EnhancedKycType = Literal["enhanced"]
KycType = Literal["light", "standard", "enhanced"]
KycStatus = Literal[
    "awaiting_contract",
    "compliance_request",
    "approved",
    "approved_rfi",
    "deprecated",
    "pending_review",
    "rejected",
    "verifying",
]

ProofOfAddressDocType = Literal[
    "UTILITY_BILL", "BANK_STATEMENT", "RENTAL_AGREEMENT", "TAX_DOCUMENT", "GOVERNMENT_CORRESPONDENCE"
]

PurposeOfTransactions = Literal[
    "business_transactions",
    "charitable_donations",
    "investment_purposes",
    "payments_to_friends_or_family_abroad",
    "personal_or_living_expenses",
    "protect_wealth",
    "purchase_good_and_services",
    "receive_payment_for_freelancing",
    "receive_salary",
    "other",
]

SourceOfFundsDocType = Literal[
    "business_income",
    "gambling_proceeds",
    "gifts",
    "government_benefits",
    "inheritance",
    "investment_loans",
    "pension_retirement",
    "salary",
    "sale_of_assets_real_estate",
    "savings",
    "esops",
    "investment_proceeds",
    "someone_else_funds",
]

SoleProprietorDocType = Literal["bank_statement", "master_service_agreement", "salary_slip"]

IdentificationDocument = Literal["PASSPORT", "ID_CARD", "DRIVERS"]

OwnerRole = Literal["beneficial_controlling", "beneficial_owner", "controlling_person"]

LimitIncreaseRequestStatus = Literal["in_review", "approved", "rejected"]

LimitIncreaseRequestSupportingDocumentType = Literal[
    "individual_bank_statement",
    "individual_tax_return",
    "individual_proof_of_income",
    "business_bank_statement",
    "business_financial_statements",
    "business_tax_return",
    "business_accounts_receivable",
    "business_contract",
    "business_merchant_processor_statement",
    "business_shareholder_loan",
    "individual_blockchain_wallet_statement",
    "individual_crypto_exchange_statement",
    "individual_employment_letter",
    "individual_investment_statement",
    "individual_pay_stub",
]

CustomerStatus = Literal[
    "verifying",
    "approved",
    "rejected",
    "deprecated",
    "pending_review",
    "awaiting_contract",
    "compliance_request",
    "approved_rfi",
]

AccountPurpose = Literal[
    "charitable_donations",
    "ecommerce_retail_payments",
    "investment_purposes",
    "business_expenses",
    "payments_to_friends_or_family_abroad",
    "personal_or_living_expenses",
    "protect_wealth",
    "purchase_goods_and_services",
    "receive_payments_for_goods_and_services",
    "tax_optimization",
    "third_party_money_transmission",
    "payroll",
    "treasury_management",
    "other",
]

CustomerBusinessType = Literal["corporation", "llc", "partnership", "sole_proprietorship", "trust", "non_profit"]

BusinessIndustry = Literal[
    "111998",
    "112120",
    "113310",
    "115114",
    "541211",
    "541810",
    "541430",
    "541715",
    "541930",
    "561422",
    "561311",
    "561612",
    "561740",
    "561730",
    "236115",
    "236220",
    "237310",
    "238210",
    "811111",
    "812111",
    "812112",
    "532111",
    "624410",
    "541922",
    "811210",
    "812199",
    "611110",
    "611310",
    "611410",
    "611710",
    "211120",
    "212114",
    "221310",
    "562111",
    "562920",
    "213112",
    "522110",
    "522210",
    "522320",
    "523150",
    "523940",
    "523999",
    "524113",
    "813110",
    "813211",
    "813219",
    "551112",
    "721110",
    "722511",
    "722513",
    "561510",
    "713110",
    "713210",
    "712110",
    "711110",
    "711211",
    "621111",
    "621210",
    "622110",
    "623110",
    "621511",
    "623220",
    "541940",
    "621399",
    "621910",
    "541110",
    "311421",
    "337121",
    "322220",
    "339920",
    "334210",
    "339930",
    "312130",
    "334111",
    "334118",
    "325412",
    "339112",
    "336110",
    "336390",
    "315990",
    "313110",
    "339910",
    "516120",
    "513130",
    "512250",
    "519130",
    "711410",
    "711510",
    "531110",
    "531120",
    "531130",
    "531190",
    "531210",
    "531311",
    "531312",
    "531320",
    "531390",
    "454110",
    "445110",
    "455110",
    "457110",
    "449210",
    "444110",
    "459210",
    "459120",
    "445320",
    "458110",
    "458210",
    "458310",
    "455219",
    "424210",
    "456110",
    "541511",
    "541512",
    "541519",
    "518210",
    "511210",
    "517111",
    "517112",
    "517410",
    "481111",
    "483111",
    "485210",
    "488510",
    "484121",
    "493110",
    "423430",
    "423690",
    "423110",
    "423830",
    "423840",
    "423510",
    "424690",
    "424990",
    "424410",
    "424480",
    "423940",
    "541611",
    "541618",
    "541330",
    "541990",
    "541214",
    "561499",
    "dapp",
    "exchange",
    "gambling",
    "gaming",
    "infra",
    "marketplace",
    "neo_bank",
    "other",
    "saas",
    "social",
    "wallet",
    "111120",
    "111219",
    "111336",
    "111421",
    "112111",
    "112210",
    "112310",
    "112410",
    "112519",
    "112990",
    "113110",
    "113210",
    "114119",
    "114210",
    "115113",
    "115210",
    "115310",
    "211130",
    "212290",
    "212390",
    "213113",
    "221122",
    "221210",
    "221320",
    "236118",
    "236210",
    "237130",
    "237210",
    "237990",
    "238191",
    "238391",
    "238991",
    "311119",
    "311212",
    "311314",
    "311422",
    "311511",
    "311612",
    "311710",
    "311811",
    "311999",
    "312111",
    "312230",
    "313240",
    "313310",
    "314120",
    "314999",
    "315120",
    "315250",
    "316110",
    "316210",
    "316990",
    "321113",
    "321211",
    "321918",
    "322120",
    "322299",
    "323120",
    "324110",
    "325180",
    "325220",
    "325320",
    "325510",
    "325611",
    "325998",
    "326111",
    "326220",
    "327120",
    "327212",
    "327310",
    "327410",
    "327999",
    "331110",
    "331210",
    "331313",
    "331410",
    "331511",
    "332111",
    "332215",
    "332311",
    "332410",
    "332510",
    "332613",
    "332710",
    "332812",
    "332999",
    "333111",
    "333248",
    "333310",
    "333413",
    "333517",
    "333611",
    "333618",
    "334310",
    "334413",
    "334511",
    "334610",
    "335131",
    "335220",
    "335311",
    "335999",
    "336211",
    "336412",
    "336510",
    "336611",
    "336999",
    "337122",
    "337214",
    "337920",
    "339999",
    "423120",
    "423220",
    "423310",
    "423490",
    "423520",
    "423620",
    "423710",
    "423990",
    "424110",
    "424310",
    "424490",
    "424590",
    "424720",
    "424820",
    "425120",
    "441110",
    "441227",
    "441330",
    "444180",
    "444240",
    "445132",
    "445298",
    "449110",
    "449129",
    "454390",
    "456120",
    "458320",
    "459310",
    "459410",
    "459510",
    "459999",
    "481211",
    "482111",
    "483112",
    "483212",
    "484110",
    "484220",
    "485119",
    "485310",
    "485410",
    "485510",
    "485999",
    "486110",
    "486210",
    "486990",
    "487110",
    "487210",
    "487990",
    "488190",
    "488210",
    "488390",
    "488490",
    "488999",
    "492110",
    "492210",
    "493190",
    "512199",
    "512290",
    "513210",
    "515210",
    "517810",
    "519290",
    "521110",
    "522130",
    "522298",
    "522390",
    "523210",
    "524128",
    "524298",
    "525190",
    "525910",
    "532289",
    "532310",
    "532490",
    "533110",
    "541199",
    "541213",
    "541219",
    "541310",
    "541490",
    "541690",
    "541720",
    "551114",
    "561110",
    "561210",
    "561599",
    "561611",
    "561790",
    "561990",
    "562211",
    "562998",
    "611210",
    "611420",
    "611519",
    "611699",
    "621498",
    "621610",
    "621999",
    "622210",
    "622310",
    "623210",
    "623311",
    "623990",
    "624190",
    "624230",
    "624310",
    "711190",
    "711219",
    "711310",
    "712120",
    "713290",
    "713990",
    "721199",
    "721211",
    "721310",
    "722310",
    "722410",
    "811198",
    "811310",
    "811411",
    "812210",
    "812320",
    "812990",
    "813319",
    "813410",
    "813930",
    "814110",
    "921140",
    "922190",
    "923130",
    "924110",
    "925120",
    "926110",
    "927110",
    "928110",
    "446120",
]

EstimatedAnnualRevenue = Literal[
    "0_99999",
    "100000_999999",
    "1000000_9999999",
    "10000000_49999999",
    "50000000_249999999",
    "250000000_plus",
]

SourceOfWealth = Literal[
    "business_dividends_or_profits",
    "investments",
    "asset_sales",
    "client_investor_contributions",
    "gambling",
    "charitable_contributions",
    "inheritance",
    "affiliate_or_royalty_income",
    "salary_or_wages",
    "savings",
]

TaxType = Literal["SSN", "ITIN"]

AmlStatus = Literal["clear", "hit", "error"]


class FraudWarning(TypedDict):
    id: Optional[str]
    name: Optional[str]
    operation: Optional[str]
    score: Optional[float]


class AmlHits(TypedDict):
    has_sanction_match: bool
    has_pep_match: bool
    has_watchlist_match: bool
    has_crimelist_match: bool
    has_adversemedia_match: bool


class KycWarning(TypedDict):
    code: Optional[str]
    message: Optional[str]
    resolution_status: Optional[str]
    warning_id: Optional[str]


class TransactionLimit(TypedDict):
    per_transaction: Optional[float]
    daily: Optional[float]
    monthly: Optional[float]


class Owner(TypedDict):
    id: str
    instance_id: str
    customer_id: NotRequired[str]
    role: OwnerRole
    first_name: str
    last_name: str
    date_of_birth: str
    tax_id: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Country
    postal_code: str
    id_doc_country: Country
    id_doc_type: IdentificationDocument
    id_doc_front_file: str
    id_doc_back_file: Optional[str]
    proof_of_address_doc_type: ProofOfAddressDocType
    proof_of_address_doc_file: str
    ownership_percentage: Optional[int]
    title: Optional[str]
    tax_type: Optional[TaxType]


CustomerCnaeConditionStatus = Literal["pending", "passed", "failed", "cancelled"]
VirtualAccountPreapprovalStatus = Literal["in_review", "approved", "rejected"]
VirtualAccountPreapprovalBankingPartner = Literal["jpmorgan", "portage"]


class CustomerCnaeCode(TypedDict):
    code: str
    description: str


class CustomerCnaeSet(TypedDict):
    primary: CustomerCnaeCode
    secondary: List[CustomerCnaeCode]


class CustomerCnaeCondition(TypedDict):
    """Present when a Brazilian business was approved on condition that its CNAE is corrected by ``due_at``."""

    status: Union[CustomerCnaeConditionStatus, str]
    expected_cnaes: List[str]
    cnae_at_approval: CustomerCnaeSet
    result_cnae: Optional[CustomerCnaeSet]
    due_at: str
    created_at: str
    reviewed_at: Optional[str]


class CustomerVirtualAccountPreapproval(TypedDict):
    status: Union[VirtualAccountPreapprovalStatus, str]
    banking_partners: List[Union[VirtualAccountPreapprovalBankingPartner, str]]
    rejection_reason: Optional[str]
    reviewed_at: Optional[str]


class IndividualWithStandardKYC(TypedDict):
    id: str
    type: Union[IndividualType, str]
    kyc_type: Union[StandardKycType, str]
    kyc_status: Union[KycStatus, str]
    kyc_warnings: NotRequired[Optional[List[KycWarning]]]
    email: str
    tax_id: NotRequired[Optional[str]]
    address_line_1: NotRequired[Optional[str]]
    address_line_2: NotRequired[Optional[str]]
    city: NotRequired[Optional[str]]
    state_province_region: NotRequired[Optional[str]]
    country: Union[Country, str]
    postal_code: NotRequired[Optional[str]]
    ip_address: NotRequired[Optional[str]]
    image_url: NotRequired[Optional[str]]
    phone_number: NotRequired[Optional[str]]
    proof_of_address_doc_type: NotRequired[Optional[Union[ProofOfAddressDocType, str]]]
    proof_of_address_doc_file: NotRequired[Optional[str]]
    first_name: NotRequired[Optional[str]]
    last_name: NotRequired[Optional[str]]
    date_of_birth: NotRequired[Optional[str]]
    id_doc_country: NotRequired[Optional[Union[Country, str]]]
    id_doc_type: NotRequired[Optional[Union[IdentificationDocument, str]]]
    id_doc_front_file: NotRequired[Optional[str]]
    id_doc_back_file: NotRequired[Optional[str]]
    aiprise_validation_key: NotRequired[str]
    instance_id: str
    tos_id: NotRequired[Optional[str]]
    created_at: NotRequired[Optional[str]]
    updated_at: NotRequired[Optional[str]]
    limit: TransactionLimit
    fraud_warnings: NotRequired[Optional[List[FraudWarning]]]
    selfie_file: NotRequired[Optional[str]]
    is_fbo: NotRequired[Optional[bool]]
    account_purpose: NotRequired[Optional[Union[AccountPurpose, str]]]
    account_purpose_other: NotRequired[Optional[str]]
    business_type: NotRequired[Optional[Union[CustomerBusinessType, str]]]
    business_description: NotRequired[Optional[str]]
    business_industry: NotRequired[Optional[BusinessIndustry]]
    estimated_annual_revenue: NotRequired[Optional[Union[EstimatedAnnualRevenue, str]]]
    source_of_wealth: NotRequired[Optional[Union[SourceOfWealth, str]]]
    publicly_traded: NotRequired[Optional[bool]]
    occupation: NotRequired[Optional[str]]
    external_id: NotRequired[Optional[str]]
    aml_status: NotRequired[Optional[Union[AmlStatus, str]]]
    aml_hits: NotRequired[Optional[AmlHits]]
    is_tos_accepted: NotRequired[Optional[bool]]
    cnae_condition: NotRequired[Optional[CustomerCnaeCondition]]
    is_nested: NotRequired[Optional[bool]]
    virtual_account_preapproval: NotRequired[Optional[CustomerVirtualAccountPreapproval]]


class IndividualWithEnhancedKYC(TypedDict):
    id: str
    type: IndividualType
    kyc_type: EnhancedKycType
    kyc_status: KycStatus
    kyc_warnings: Optional[List[KycWarning]]
    email: str
    tax_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Country
    postal_code: Optional[str]
    ip_address: Optional[str]
    image_url: Optional[str]
    phone_number: Optional[str]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    proof_of_address_doc_file: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: str
    id_doc_country: Optional[Country]
    id_doc_type: Optional[IdentificationDocument]
    id_doc_front_file: Optional[str]
    id_doc_back_file: Optional[str]
    aiprise_validation_key: str
    instance_id: str
    source_of_funds_doc_type: Optional[str]
    source_of_funds_doc_file: Optional[str]
    individual_holding_doc_front_file: str
    purpose_of_transactions: Optional[PurposeOfTransactions]
    purpose_of_transactions_explanation: Optional[str]
    tos_id: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    limit: TransactionLimit
    fraud_warnings: Optional[List[FraudWarning]]
    selfie_file: Optional[str]
    is_fbo: Optional[bool]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[CustomerBusinessType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]
    external_id: Optional[str]
    aml_status: Optional[AmlStatus]
    aml_hits: Optional[AmlHits]
    is_tos_accepted: Optional[bool]
    cnae_condition: NotRequired[Optional[CustomerCnaeCondition]]
    is_nested: NotRequired[Optional[bool]]
    virtual_account_preapproval: NotRequired[Optional[CustomerVirtualAccountPreapproval]]


class BusinessWithStandardKYB(TypedDict):
    id: str
    type: BusinessType
    kyc_type: StandardKycType
    kyc_status: KycStatus
    kyc_warnings: Optional[List[KycWarning]]
    email: str
    tax_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Country
    postal_code: Optional[str]
    ip_address: Optional[str]
    image_url: Optional[str]
    phone_number: Optional[str]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    proof_of_address_doc_file: Optional[str]
    legal_name: Optional[str]
    alternate_name: Optional[str]
    formation_date: str
    website: Optional[str]
    owners: Optional[List[Owner]]
    incorporation_doc_file: Optional[str]
    proof_of_ownership_doc_file: Optional[str]
    external_id: Optional[str]
    instance_id: str
    tos_id: Optional[str]
    aiprise_validation_key: str
    created_at: Optional[str]
    updated_at: Optional[str]
    limit: TransactionLimit
    fraud_warnings: Optional[List[FraudWarning]]
    selfie_file: Optional[str]
    is_fbo: Optional[bool]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[CustomerBusinessType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]
    aml_status: Optional[AmlStatus]
    aml_hits: Optional[AmlHits]
    is_tos_accepted: Optional[bool]
    cnae_condition: NotRequired[Optional[CustomerCnaeCondition]]
    is_nested: NotRequired[Optional[bool]]
    virtual_account_preapproval: NotRequired[Optional[CustomerVirtualAccountPreapproval]]


class CreateIndividualWithStandardKYCInput(TypedDict):
    external_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    country: Country
    date_of_birth: str
    email: str
    first_name: Optional[str]
    phone_number: Optional[str]
    id_doc_country: Optional[Country]
    id_doc_front_file: Optional[str]
    id_doc_type: Optional[IdentificationDocument]
    id_doc_back_file: Optional[str]
    last_name: Optional[str]
    postal_code: Optional[str]
    proof_of_address_doc_file: Optional[str]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    state_province_region: Optional[str]
    tax_id: Optional[str]
    tos_id: Optional[str]
    ip_address: Optional[str]
    image_url: Optional[str]
    selfie_file: Optional[str]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    occupation: Optional[str]


class CreateIndividualWithStandardKYCResponse(TypedDict):
    id: str


class CreateIndividualWithEnhancedKYCInput(TypedDict):
    external_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    country: Country
    date_of_birth: str
    email: str
    first_name: Optional[str]
    id_doc_country: Optional[Country]
    id_doc_front_file: Optional[str]
    id_doc_type: Optional[IdentificationDocument]
    id_doc_back_file: Optional[str]
    individual_holding_doc_front_file: str
    last_name: Optional[str]
    postal_code: Optional[str]
    phone_number: Optional[str]
    proof_of_address_doc_file: Optional[str]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    purpose_of_transactions: Optional[PurposeOfTransactions]
    source_of_funds_doc_file: Optional[str]
    source_of_funds_doc_type: Optional[SourceOfFundsDocType]
    purpose_of_transactions_explanation: Optional[str]
    state_province_region: Optional[str]
    tax_id: Optional[str]
    tos_id: Optional[str]
    ip_address: Optional[str]
    image_url: Optional[str]
    selfie_file: Optional[str]
    is_fbo: Optional[bool]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    occupation: Optional[str]


class CreateIndividualWithEnhancedKYCResponse(TypedDict):
    id: str


class CreateBusinessWithStandardKYBInput(TypedDict):
    external_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    alternate_name: Optional[str]
    city: Optional[str]
    country: Country
    email: str
    formation_date: str
    incorporation_doc_file: Optional[str]
    legal_name: Optional[str]
    owners: Optional[List[Owner]]
    postal_code: Optional[str]
    proof_of_address_doc_file: Optional[str]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    proof_of_ownership_doc_file: Optional[str]
    state_province_region: Optional[str]
    tax_id: Optional[str]
    tos_id: Optional[str]
    website: Optional[str]
    ip_address: Optional[str]
    image_url: Optional[str]
    phone_number: Optional[str]
    selfie_file: Optional[str]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[CustomerBusinessType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]


class CreateBusinessWithStandardKYBResponse(TypedDict):
    id: str


ListCustomersResponse = List[Union[IndividualWithStandardKYC, IndividualWithEnhancedKYC, BusinessWithStandardKYB]]


class ListCustomersPaginatedResponse(TypedDict):
    data: List[Union[IndividualWithStandardKYC, IndividualWithEnhancedKYC, BusinessWithStandardKYB]]
    pagination: PaginationMetadata


class ListCustomersInput(PaginationParams, total=False):
    full_name: str
    customer_name: str
    status: CustomerStatus
    customer_id: str
    bank_account_id: str
    country: str


GetCustomerResponse = Union[IndividualWithStandardKYC, IndividualWithEnhancedKYC, BusinessWithStandardKYB]


class OwnerUpdate(TypedDict):
    id: str
    first_name: str
    last_name: str
    role: OwnerRole
    date_of_birth: str
    tax_id: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    state_province_region: str
    country: Country
    postal_code: str
    id_doc_country: Country
    id_doc_type: IdentificationDocument
    id_doc_front_file: str
    id_doc_back_file: Optional[str]
    ownership_percentage: Optional[int]
    title: Optional[str]
    tax_type: Optional[TaxType]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    proof_of_address_doc_file: Optional[str]


class UpdateCustomerInput(TypedDict):
    customer_id: str
    email: Optional[str]
    tax_id: Optional[str]
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    state_province_region: Optional[str]
    country: Optional[Country]
    postal_code: Optional[str]
    ip_address: Optional[str]
    image_url: Optional[str]
    phone_number: Optional[str]
    proof_of_address_doc_type: Optional[ProofOfAddressDocType]
    proof_of_address_doc_file: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    date_of_birth: Optional[str]
    id_doc_country: Optional[Country]
    id_doc_type: Optional[IdentificationDocument]
    id_doc_front_file: Optional[str]
    id_doc_back_file: Optional[str]
    legal_name: Optional[str]
    alternate_name: Optional[str]
    formation_date: Optional[str]
    website: Optional[str]
    owners: Optional[List[OwnerUpdate]]
    incorporation_doc_file: Optional[str]
    proof_of_ownership_doc_file: Optional[str]
    source_of_funds_doc_type: Optional[SourceOfFundsDocType]
    source_of_funds_doc_file: Optional[str]
    individual_holding_doc_front_file: Optional[str]
    purpose_of_transactions: Optional[PurposeOfTransactions]
    purpose_of_transactions_explanation: Optional[str]
    external_id: Optional[str]
    tos_id: Optional[str]
    selfie_file: Optional[str]
    account_purpose: Optional[AccountPurpose]
    account_purpose_other: Optional[str]
    business_type: Optional[CustomerBusinessType]
    business_description: Optional[str]
    business_industry: Optional[BusinessIndustry]
    estimated_annual_revenue: Optional[EstimatedAnnualRevenue]
    source_of_wealth: Optional[SourceOfWealth]
    publicly_traded: Optional[bool]
    occupation: Optional[str]


class PayinLimit(TypedDict):
    daily: float
    monthly: float


class PayoutLimit(TypedDict):
    daily: float
    monthly: float


class Limits(TypedDict):
    payin: PayinLimit
    payout: PayoutLimit


class GetCustomerLimitsResponse(TypedDict):
    limits: Limits


class LimitIncreaseSupportingDocument(TypedDict):
    type: LimitIncreaseRequestSupportingDocumentType
    file: str
    """A file URL from ``upload.create``."""


class LimitIncreaseSupportingDocumentOut(TypedDict):
    type: Union[LimitIncreaseRequestSupportingDocumentType, str]
    file: str


class LimitIncreaseRequest(TypedDict):
    id: str
    customer_id: str
    status: Union[LimitIncreaseRequestStatus, str]
    daily: NotRequired[Optional[float]]
    monthly: NotRequired[Optional[float]]
    per_transaction: NotRequired[Optional[float]]
    supporting_document_file: NotRequired[Optional[str]]
    supporting_document_type: NotRequired[Optional[Union[LimitIncreaseRequestSupportingDocumentType, str]]]
    created_at: NotRequired[Optional[str]]
    updated_at: NotRequired[Optional[str]]
    supporting_documents: NotRequired[Optional[List[LimitIncreaseSupportingDocumentOut]]]


GetLimitIncreaseRequestsResponse = List[LimitIncreaseRequest]


class RequestLimitIncreaseInput(TypedDict):
    customer_id: str
    daily: Optional[float]
    monthly: Optional[float]
    per_transaction: Optional[float]
    supporting_document_file: str
    supporting_document_type: LimitIncreaseRequestSupportingDocumentType
    supporting_documents: NotRequired[List[LimitIncreaseSupportingDocument]]


class RequestLimitIncreaseResponse(TypedDict):
    id: str


class CustomersResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(
        self, params: Optional[ListCustomersInput] = None
    ) -> BlindpayApiResponse[Union[ListCustomersResponse, ListCustomersPaginatedResponse]]:
        query_string = build_query(params)
        return await self._client.get(f"/instances/{self._instance_id}/customers{query_string}")

    def list_auto_paging(self, params: Optional[ListCustomersInput] = None) -> AsyncIterator[GetCustomerResponse]:
        return async_auto_paging_iter(self.list, params)

    async def create_individual_with_standard_kyc(
        self, data: CreateIndividualWithStandardKYCInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateIndividualWithStandardKYCResponse]:
        payload = {"kyc_type": "standard", "type": "individual", **data}
        return await self._client.post(f"/instances/{self._instance_id}/customers", payload, options=options)

    async def create_individual_with_enhanced_kyc(
        self, data: CreateIndividualWithEnhancedKYCInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateIndividualWithEnhancedKYCResponse]:
        payload = {"kyc_type": "enhanced", "type": "individual", **data}
        return await self._client.post(f"/instances/{self._instance_id}/customers", payload, options=options)

    async def create_business_with_standard_kyb(
        self, data: CreateBusinessWithStandardKYBInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateBusinessWithStandardKYBResponse]:
        payload = {"kyc_type": "standard", "type": "business", **data}
        return await self._client.post(f"/instances/{self._instance_id}/customers", payload, options=options)

    async def get(self, customer_id: str) -> BlindpayApiResponse[GetCustomerResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/customers/{path_param(customer_id)}")

    async def update(
        self, data: UpdateCustomerInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        return await self._client.put(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}", payload, options=options
        )

    async def delete(self, customer_id: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
        return await self._client.delete(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}", options=options
        )

    async def get_limits(self, customer_id: str) -> BlindpayApiResponse[GetCustomerLimitsResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/limits/customers/{path_param(customer_id)}")

    async def get_limit_increase_requests(
        self, customer_id: str
    ) -> BlindpayApiResponse[GetLimitIncreaseRequestsResponse]:
        return await self._client.get(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/limit-increase"
        )

    async def request_limit_increase(
        self, data: RequestLimitIncreaseInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[RequestLimitIncreaseResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        return await self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/limit-increase",
            payload,
            options=options,
        )


class CustomersResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(
        self, params: Optional[ListCustomersInput] = None
    ) -> BlindpayApiResponse[Union[ListCustomersResponse, ListCustomersPaginatedResponse]]:
        query_string = build_query(params)
        return self._client.get(f"/instances/{self._instance_id}/customers{query_string}")

    def list_auto_paging(self, params: Optional[ListCustomersInput] = None) -> Iterator[GetCustomerResponse]:
        return auto_paging_iter(self.list, params)

    def create_individual_with_standard_kyc(
        self, data: CreateIndividualWithStandardKYCInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateIndividualWithStandardKYCResponse]:
        payload = {"kyc_type": "standard", "type": "individual", **data}
        return self._client.post(f"/instances/{self._instance_id}/customers", payload, options=options)

    def create_individual_with_enhanced_kyc(
        self, data: CreateIndividualWithEnhancedKYCInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateIndividualWithEnhancedKYCResponse]:
        payload = {"kyc_type": "enhanced", "type": "individual", **data}
        return self._client.post(f"/instances/{self._instance_id}/customers", payload, options=options)

    def create_business_with_standard_kyb(
        self, data: CreateBusinessWithStandardKYBInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[CreateBusinessWithStandardKYBResponse]:
        payload = {"kyc_type": "standard", "type": "business", **data}
        return self._client.post(f"/instances/{self._instance_id}/customers", payload, options=options)

    def get(self, customer_id: str) -> BlindpayApiResponse[GetCustomerResponse]:
        return self._client.get(f"/instances/{self._instance_id}/customers/{path_param(customer_id)}")

    def update(self, data: UpdateCustomerInput, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        return self._client.put(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}", payload, options=options
        )

    def delete(self, customer_id: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
        return self._client.delete(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}", options=options
        )

    def get_limits(self, customer_id: str) -> BlindpayApiResponse[GetCustomerLimitsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/limits/customers/{path_param(customer_id)}")

    def get_limit_increase_requests(self, customer_id: str) -> BlindpayApiResponse[GetLimitIncreaseRequestsResponse]:
        return self._client.get(f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/limit-increase")

    def request_limit_increase(
        self, data: RequestLimitIncreaseInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[RequestLimitIncreaseResponse]:
        customer_id = data["customer_id"]
        payload = {k: v for k, v in data.items() if k != "customer_id"}
        return self._client.post(
            f"/instances/{self._instance_id}/customers/{path_param(customer_id)}/limit-increase",
            payload,
            options=options,
        )


def create_customers_resource(instance_id: str, client: InternalApiClient) -> CustomersResource:
    return CustomersResource(instance_id, client)


def create_customers_resource_sync(instance_id: str, client: InternalApiClientSync) -> CustomersResourceSync:
    return CustomersResourceSync(instance_id, client)
