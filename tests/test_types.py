"""Type-surface regression tests: each of these constructs an explicitly
TypedDict-annotated literal, so pyright/mypy (both run over tests/) enforce
the shape at the assignment itself -- not just at runtime equality. This is
the proof that matters for a type-only fix: a wrong type here fails the type
checker, not just a test assertion.
"""

from blindpay.resources.custodial_wallets.custodial_wallets import CreateCustodialWalletInput
from blindpay.resources.payins.payins import BankDetails, CreateEvmPayinResponse, GetPayinTrackResponse, Payin
from blindpay.types import BankAccountType, PaginationMetadata

_BANK_DETAILS: BankDetails = {
    "routing_number": "0",
    "account_number": "0",
    "account_type": "checking",
    "swift_bic_code": "0",
    "ach": {"routing_number": "0", "account_number": "0"},
    "wire": {"routing_number": "0", "account_number": "0"},
    "rtp": {"routing_number": "0", "account_number": "0"},
    "beneficiary": {"name": "0", "address_line_1": "0", "address_line_2": None},
    "receiving_bank": {"name": "0", "address_line_1": "0", "address_line_2": None},
}


class TestPaginationMetadataAcceptsStringCursors:
    def test_string_next_page_and_prev_page(self):
        meta: PaginationMetadata = {
            "has_more": True,
            "next_page": "pi_123",
            "prev_page": "pi_123",
        }
        assert meta["next_page"] == "pi_123"
        assert meta["prev_page"] == "pi_123"

    def test_next_page_and_prev_page_are_nullable(self):
        meta: PaginationMetadata = {
            "has_more": False,
            "next_page": None,
            "prev_page": None,
        }
        assert meta["next_page"] is None
        assert meta["prev_page"] is None


class TestBillingFeeAmountIsNumeric:
    def test_payin_accepts_a_float(self):
        payin: Payin = {
            "customer_id": "cus_000000000000",
            "id": "pi_000000000000",
            "pix_code": None,
            "memo_code": None,
            "clabe": None,
            "status": "completed",
            "manual_execution_status": None,
            "payin_quote_id": "pq_000000000000",
            "instance_id": "in_000000000000",
            "tracking_transaction": None,
            "tracking_payment": None,
            "tracking_complete": None,
            "tracking_partner_fee": None,
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
            "image_url": None,
            "first_name": None,
            "last_name": None,
            "legal_name": None,
            "type": "ach",
            "payment_method": "ach",
            "sender_amount": 1000,
            "receiver_amount": 1000,
            "token": "USDC",
            "partner_fee_amount": 0,
            "total_fee_amount": 0,
            "commercial_quotation": 1,
            "blindpay_quotation": 1,
            "currency": "USD",
            "billing_fee": 0,
            "name": "John Doe",
            "address": "0x0",
            "network": "base",
            "blindpay_bank_details": _BANK_DETAILS,
            "is_otc": None,
            "billing_fee_amount": 50.0,
            "pse_document_type": None,
            "pse_full_name": None,
            "pse_payment_link": None,
            "pse_tax_id": None,
            "partner_fee_id": None,
        }
        assert payin["billing_fee_amount"] == 50.0

    def test_get_payin_track_response_billing_fee_amount_omitted_type_checks(self):
        # NotRequired: omitting the key entirely must still type-check.
        without: GetPayinTrackResponse = {
            "customer_id": "cus_000000000000",
            "id": "pi_000000000000",
            "pix_code": "0",
            "memo_code": "0",
            "clabe": "0",
            "status": "completed",
            "manual_execution_status": None,
            "payin_quote_id": "pq_000000000000",
            "instance_id": "in_000000000000",
            "tracking_transaction": {
                "step": "completed",
                "status": "completed",
                "transaction_hash": "0",
                "completed_at": "0",
            },
            "tracking_payment": {
                "step": "completed",
                "provider_name": "0",
                "provider_transaction_id": "0",
                "provider_status": "0",
                "estimated_time_of_arrival": "0",
                "completed_at": "0",
            },
            "tracking_complete": {
                "step": "completed",
                "status": "completed",
                "transaction_hash": "0",
                "completed_at": "0",
            },
            "tracking_partner_fee": {"step": "completed", "transaction_hash": "0", "completed_at": "0"},
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
            "image_url": "0",
            "first_name": "0",
            "last_name": "0",
            "legal_name": "0",
            "type": "ach",
            "payment_method": "ach",
            "sender_amount": 1000,
            "receiver_amount": 1000,
            "token": "USDC",
            "partner_fee_amount": 0,
            "total_fee_amount": 0,
            "commercial_quotation": 1,
            "blindpay_quotation": 1,
            "currency": "USD",
            "billing_fee": 0,
            "name": "John Doe",
            "address": "0x0",
            "network": "base",
            "blindpay_bank_details": _BANK_DETAILS,
            "partner_fee_id": None,
        }
        assert without.get("billing_fee_amount") is None

    def test_get_payin_track_response_billing_fee_amount_is_numeric_when_present(self):
        with_it: GetPayinTrackResponse = {
            "customer_id": "cus_000000000000",
            "id": "pi_000000000000",
            "pix_code": "0",
            "memo_code": "0",
            "clabe": "0",
            "status": "completed",
            "manual_execution_status": None,
            "payin_quote_id": "pq_000000000000",
            "instance_id": "in_000000000000",
            "tracking_transaction": {
                "step": "completed",
                "status": "completed",
                "transaction_hash": "0",
                "completed_at": "0",
            },
            "tracking_payment": {
                "step": "completed",
                "provider_name": "0",
                "provider_transaction_id": "0",
                "provider_status": "0",
                "estimated_time_of_arrival": "0",
                "completed_at": "0",
            },
            "tracking_complete": {
                "step": "completed",
                "status": "completed",
                "transaction_hash": "0",
                "completed_at": "0",
            },
            "tracking_partner_fee": {"step": "completed", "transaction_hash": "0", "completed_at": "0"},
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
            "image_url": "0",
            "first_name": "0",
            "last_name": "0",
            "legal_name": "0",
            "type": "ach",
            "payment_method": "ach",
            "sender_amount": 1000,
            "receiver_amount": 1000,
            "token": "USDC",
            "partner_fee_amount": 0,
            "total_fee_amount": 0,
            "commercial_quotation": 1,
            "blindpay_quotation": 1,
            "currency": "USD",
            "billing_fee": 0,
            "name": "John Doe",
            "address": "0x0",
            "network": "base",
            "blindpay_bank_details": _BANK_DETAILS,
            "partner_fee_id": None,
            "billing_fee_amount": 50.0,
        }
        assert with_it.get("billing_fee_amount") == 50.0

    def test_create_evm_payin_response_billing_fee_amount_is_optional_and_numeric(self):
        resp: CreateEvmPayinResponse = {
            "id": "pi_000000000000",
            "status": "completed",
            "pix_code": None,
            "memo_code": None,
            "clabe": None,
            "tracking_complete": None,
            "tracking_payment": None,
            "tracking_transaction": None,
            "tracking_partner_fee": None,
            "blindpay_bank_details": _BANK_DETAILS,
            "customer_id": "cus_000000000000",
            "receiver_amount": 1000,
            "billing_fee_amount": 50.0,
        }
        assert resp.get("billing_fee_amount") == 50.0


class TestBankAccountTypeUsesSingularSaving:
    def test_saving_is_a_valid_value(self):
        value: BankAccountType = "saving"
        assert value == "saving"


class TestCreateCustodialWalletInputRequiresName:
    def test_name_is_required_and_sent(self):
        data: CreateCustodialWalletInput = {
            "customer_id": "cus_000000000000",
            "network": "base",
            "name": "My Wallet",
        }
        assert data["name"] == "My Wallet"

    def test_external_id_is_optional(self):
        data: CreateCustodialWalletInput = {
            "customer_id": "cus_000000000000",
            "network": "base",
            "name": "My Wallet",
        }
        assert "external_id" not in data

        with_external_id: CreateCustodialWalletInput = {
            "customer_id": "cus_000000000000",
            "network": "base",
            "name": "My Wallet",
            "external_id": "your-database-id",
        }
        assert with_external_id.get("external_id") == "your-database-id"
