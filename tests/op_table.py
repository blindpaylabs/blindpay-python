# ruff: noqa: ARG005 -- GET entries ignore the options argument every Call receives.
"""Every SDK method, keyed by the spec operation it calls.

One table drives the request-options guard test, the op-coverage test and the coverage report. Each entry calls
the method with minimal arguments on either client (``client`` is ``BlindPay`` or ``BlindPaySync``) and states the
exact path the call must hit. Ids are distinct per kind so a swapped argument shows up as a wrong path.
"""

from dataclasses import dataclass
from typing import Any, Callable, List, Optional

from blindpay import RequestOptions

INSTANCE = "in_000000000000"
CUSTOMER = "cu_000000000000"
BANK_ACCOUNT = "ba_000000000000"
ITEM = "it_000000000000"
MEMBER = "us_000000000000"

Call = Callable[[Any, Optional[RequestOptions]], Any]


NO_BODY_CHECK: Any = object()


@dataclass(frozen=True)
class Op:
    operation: str  # "METHOD /v1/path" exactly as in reference/sdk-surface.txt and fixtures/index.json
    method: str  # accessor on the client, e.g. "payouts.create_evm"
    call: Call
    path: str  # the exact raw path the call sends (query string excluded)
    multipart: bool = False
    note: str = ""
    body: Any = NO_BODY_CHECK  # the exact JSON body the call must send
    query: Optional[str] = None  # the exact query string the call must send

    @property
    def http_method(self) -> str:
        return self.operation.split(" ", 1)[0]

    @property
    def mutating(self) -> bool:
        return self.http_method != "GET"


V1 = "/v1"
# Only the spec's required keys: no wallet addresses, no virtual_account_set.
PARTNER_FEE = {
    "name": "fee",
    "payin_flat_fee": 0,
    "payin_percentage_fee": 100,
    "payout_flat_fee": 50,
    "payout_percentage_fee": 0,
}
INST = f"{V1}/instances/{INSTANCE}"
CUST = f"{INST}/customers/{CUSTOMER}"

BANK_ACCOUNT_CREATES = [
    "create_pix",
    "create_argentina_transfers",
    "create_spei",
    "create_colombia_ach",
    "create_ach",
    "create_wire",
    "create_international_swift",
    "create_rtp",
    "create_pix_safe",
    "create_ted",
    "create_sepa",
    "create_faster_payments",
]


def _bank_account_create(name: str) -> Call:
    return lambda c, o: getattr(c.customers.bank_accounts, name)({"customer_id": CUSTOMER, "name": "Acme"}, o)


OPS: List[Op] = [
    # available
    Op(
        "GET /v1/available/bank-details",
        "available.get_bank_details",
        lambda c, o: c.available.get_bank_details("pix"),
        f"{V1}/available/bank-details",
    ),
    Op(
        "GET /v1/available/naics",
        "available.get_naics_codes",
        lambda c, o: c.available.get_naics_codes(),
        f"{V1}/available/naics",
    ),
    Op("GET /v1/available/rails", "available.get_rails", lambda c, o: c.available.get_rails(), f"{V1}/available/rails"),
    Op(
        "GET /v1/available/swift/{swift}",
        "available.get_swift_code_bank_details",
        lambda c, o: c.available.get_swift_code_bank_details("BOFAUS3N"),
        f"{V1}/available/swift/BOFAUS3N",
    ),
    # bank accounts
    *[
        Op(
            "POST /v1/instances/{instance_id}/customers/{customer_id}/bank-accounts",
            f"customers.bank_accounts.{name}",
            _bank_account_create(name),
            f"{CUST}/bank-accounts",
        )
        for name in BANK_ACCOUNT_CREATES
    ],
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/bank-accounts",
        "customers.bank_accounts.list",
        lambda c, o: c.customers.bank_accounts.list(CUSTOMER),
        f"{CUST}/bank-accounts",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/bank-accounts/{id}",
        "customers.bank_accounts.get",
        lambda c, o: c.customers.bank_accounts.get(CUSTOMER, ITEM),
        f"{CUST}/bank-accounts/{ITEM}",
    ),
    Op(
        "DELETE /v1/instances/{instance_id}/customers/{customer_id}/bank-accounts/{id}",
        "customers.bank_accounts.delete",
        lambda c, o: c.customers.bank_accounts.delete(CUSTOMER, ITEM, o),
        f"{CUST}/bank-accounts/{ITEM}",
    ),
    # blockchain wallets
    Op(
        "POST /v1/instances/{instance_id}/customers/{customer_id}/blockchain-wallets",
        "wallets.blockchain.create_with_address",
        lambda c, o: c.wallets.blockchain.create_with_address(
            {"customer_id": CUSTOMER, "name": "w", "network": "base", "address": "0x0"}, o
        ),
        f"{CUST}/blockchain-wallets",
    ),
    Op(
        "POST /v1/instances/{instance_id}/customers/{customer_id}/blockchain-wallets",
        "wallets.blockchain.create_with_hash",
        lambda c, o: c.wallets.blockchain.create_with_hash(
            {"customer_id": CUSTOMER, "name": "w", "network": "base", "signature_tx_hash": "0x0"}, o
        ),
        f"{CUST}/blockchain-wallets",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/blockchain-wallets",
        "wallets.blockchain.list",
        lambda c, o: c.wallets.blockchain.list(CUSTOMER),
        f"{CUST}/blockchain-wallets",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/blockchain-wallets/sign-message",
        "wallets.blockchain.get_wallet_message",
        lambda c, o: c.wallets.blockchain.get_wallet_message(CUSTOMER),
        f"{CUST}/blockchain-wallets/sign-message",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/blockchain-wallets/{id}",
        "wallets.blockchain.get",
        lambda c, o: c.wallets.blockchain.get({"customer_id": CUSTOMER, "id": ITEM}),
        f"{CUST}/blockchain-wallets/{ITEM}",
    ),
    Op(
        "DELETE /v1/instances/{instance_id}/customers/{customer_id}/blockchain-wallets/{id}",
        "wallets.blockchain.delete",
        lambda c, o: c.wallets.blockchain.delete({"customer_id": CUSTOMER, "id": ITEM}, o),
        f"{CUST}/blockchain-wallets/{ITEM}",
    ),
    # customers
    Op(
        "POST /v1/instances/{instance_id}/customers",
        "customers.create_individual_with_standard_kyc",
        lambda c, o: c.customers.create_individual_with_standard_kyc({"email": "a@example.com", "country": "US"}, o),
        f"{INST}/customers",
    ),
    Op(
        "POST /v1/instances/{instance_id}/customers",
        "customers.create_individual_with_enhanced_kyc",
        lambda c, o: c.customers.create_individual_with_enhanced_kyc({"email": "a@example.com", "country": "US"}, o),
        f"{INST}/customers",
    ),
    Op(
        "POST /v1/instances/{instance_id}/customers",
        "customers.create_business_with_standard_kyb",
        lambda c, o: c.customers.create_business_with_standard_kyb({"email": "a@example.com", "country": "US"}, o),
        f"{INST}/customers",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers",
        "customers.list",
        lambda c, o: c.customers.list(),
        f"{INST}/customers",
    ),
    Op(
        "POST /v1/instances/{instance_id}/customers/{customer_id}/limit-increase",
        "customers.request_limit_increase",
        lambda c, o: c.customers.request_limit_increase(
            {"customer_id": CUSTOMER, "per_transaction": 1, "daily": 1, "monthly": 1}, o
        ),
        f"{CUST}/limit-increase",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/limit-increase",
        "customers.get_limit_increase_requests",
        lambda c, o: c.customers.get_limit_increase_requests(CUSTOMER),
        f"{CUST}/limit-increase",
    ),
    Op("GET /v1/instances/{instance_id}/customers/{id}", "customers.get", lambda c, o: c.customers.get(CUSTOMER), CUST),
    Op(
        "PUT /v1/instances/{instance_id}/customers/{id}",
        "customers.update",
        lambda c, o: c.customers.update({"customer_id": CUSTOMER, "email": "a@example.com"}, o),
        CUST,
    ),
    Op(
        "DELETE /v1/instances/{instance_id}/customers/{id}",
        "customers.delete",
        lambda c, o: c.customers.delete(CUSTOMER, o),
        CUST,
    ),
    Op(
        "GET /v1/instances/{instance_id}/limits/customers/{id}",
        "customers.get_limits",
        lambda c, o: c.customers.get_limits(CUSTOMER),
        f"{INST}/limits/customers/{CUSTOMER}",
    ),
    Op(
        "GET /v1/instances/{instance_id}/limits/customers/{id}",
        "limits.get_customer_limits",
        lambda c, o: c.limits.get_customer_limits(CUSTOMER),
        f"{INST}/limits/customers/{CUSTOMER}",
        note="duplicate of customers.get_limits",
    ),
    # fees
    Op("GET /v1/instances/{instance_id}/billing/fees", "fees.get", lambda c, o: c.fees.get(), f"{INST}/billing/fees"),
    # instances
    Op("PUT /v1/instances/{id}", "instances.update", lambda c, o: c.instances.update({"name": "Acme"}, o), INST),
    Op("DELETE /v1/instances/{id}", "instances.delete", lambda c, o: c.instances.delete(o), INST),
    Op(
        "GET /v1/instances/{id}/members",
        "instances.get_members",
        lambda c, o: c.instances.get_members(),
        f"{INST}/members",
    ),
    Op(
        "DELETE /v1/instances/{id}/members/{user_id}",
        "instances.delete_member",
        lambda c, o: c.instances.delete_member(MEMBER, o),
        f"{INST}/members/{MEMBER}",
    ),
    Op(
        "PUT /v1/instances/{id}/members/{user_id}",
        "instances.update_member_role",
        lambda c, o: c.instances.update_member_role(MEMBER, "admin", o),
        f"{INST}/members/{MEMBER}",
    ),
    Op(
        "POST /v1/instances/{id}/ownership",
        "instances.migrate_ownership",
        lambda c, o: c.instances.migrate_ownership({"new_owner_id": MEMBER}, o),
        f"{INST}/ownership",
    ),
    Op(
        "POST /v1/instances/{id}/ownership",
        "ownership.migrate",
        lambda c, o: c.ownership.migrate({"new_owner_id": MEMBER}, o),
        f"{INST}/ownership",
        note="duplicate of instances.migrate_ownership",
    ),
    # offramp wallets
    Op(
        "POST /v1/instances/{instance_id}/customers/{customer_id}/bank-accounts/{bank_account_id}/offramp-wallets",
        "wallets.offramp.create",
        lambda c, o: c.wallets.offramp.create(
            {"customer_id": CUSTOMER, "bank_account_id": BANK_ACCOUNT, "network": "tron", "partner_fee_id": "pf_1"}, o
        ),
        f"{CUST}/bank-accounts/{BANK_ACCOUNT}/offramp-wallets",
        body={"network": "tron", "partner_fee_id": "pf_1"},
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/bank-accounts/{bank_account_id}/offramp-wallets",
        "wallets.offramp.list",
        lambda c, o: c.wallets.offramp.list({"customer_id": CUSTOMER, "bank_account_id": BANK_ACCOUNT}),
        f"{CUST}/bank-accounts/{BANK_ACCOUNT}/offramp-wallets",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/bank-accounts/{bank_account_id}/offramp-wallets/{id}",
        "wallets.offramp.get",
        lambda c, o: c.wallets.offramp.get({"customer_id": CUSTOMER, "bank_account_id": BANK_ACCOUNT, "id": ITEM}),
        f"{CUST}/bank-accounts/{BANK_ACCOUNT}/offramp-wallets/{ITEM}",
    ),
    # partner fees
    Op(
        "POST /v1/instances/{instance_id}/partner-fees",
        "partner_fees.create",
        lambda c, o: c.partner_fees.create(PARTNER_FEE, o),
        f"{INST}/partner-fees",
        body=PARTNER_FEE,
    ),
    Op(
        "GET /v1/instances/{instance_id}/partner-fees",
        "partner_fees.list",
        lambda c, o: c.partner_fees.list(),
        f"{INST}/partner-fees",
    ),
    Op(
        "GET /v1/instances/{instance_id}/partner-fees/{id}",
        "partner_fees.get",
        lambda c, o: c.partner_fees.get(ITEM),
        f"{INST}/partner-fees/{ITEM}",
    ),
    Op(
        "DELETE /v1/instances/{instance_id}/partner-fees/{id}",
        "partner_fees.delete",
        lambda c, o: c.partner_fees.delete(ITEM, o),
        f"{INST}/partner-fees/{ITEM}",
    ),
    # payin quotes
    Op(
        "POST /v1/instances/{instance_id}/payin-quotes",
        "payins.quotes.create",
        lambda c, o: c.payins.quotes.create({"blockchain_wallet_id": ITEM}, o),
        f"{INST}/payin-quotes",
    ),
    Op(
        "POST /v1/instances/{instance_id}/payin-quotes/fx",
        "payins.quotes.get_fx_rate",
        lambda c, o: c.payins.quotes.get_fx_rate(
            {"currency_type": "sender", "from_currency": "BRL", "to": "USDC", "request_amount": 1000}, o
        ),
        f"{INST}/payin-quotes/fx",
    ),
    # payins
    Op(
        "GET /v1/e/payins/{id}",
        "payins.get_track",
        lambda c, o: c.payins.get_track(ITEM),
        f"{V1}/e/payins/{ITEM}",
        note="tracking endpoint: 401 for server-side callers in production",
    ),
    Op("GET /v1/instances/{instance_id}/payins", "payins.list", lambda c, o: c.payins.list(), f"{INST}/payins"),
    Op(
        "POST /v1/instances/{instance_id}/payins/evm",
        "payins.create_evm",
        lambda c, o: c.payins.create_evm(ITEM, o),
        f"{INST}/payins/evm",
    ),
    Op(
        "GET /v1/instances/{instance_id}/payins/{id}",
        "payins.get",
        lambda c, o: c.payins.get(ITEM),
        f"{INST}/payins/{ITEM}",
    ),
    # payouts
    Op(
        "GET /v1/e/payouts/{id}",
        "payouts.get_track",
        lambda c, o: c.payouts.get_track(ITEM),
        f"{V1}/e/payouts/{ITEM}",
        note="tracking endpoint: 401 for server-side callers in production",
    ),
    Op("GET /v1/instances/{instance_id}/payouts", "payouts.list", lambda c, o: c.payouts.list(), f"{INST}/payouts"),
    Op(
        "POST /v1/instances/{instance_id}/payouts/evm",
        "payouts.create_evm",
        lambda c, o: c.payouts.create_evm({"quote_id": ITEM, "sender_wallet_address": "0x0"}, o),
        f"{INST}/payouts/evm",
    ),
    Op(
        "POST /v1/instances/{instance_id}/payouts/solana",
        "payouts.create_solana",
        lambda c, o: c.payouts.create_solana({"quote_id": ITEM, "sender_wallet_address": "So1"}, o),
        f"{INST}/payouts/solana",
    ),
    Op(
        "POST /v1/instances/{instance_id}/payouts/stellar",
        "payouts.create_stellar",
        lambda c, o: c.payouts.create_stellar({"quote_id": ITEM, "sender_wallet_address": "G0"}, o),
        f"{INST}/payouts/stellar",
    ),
    Op(
        "POST /v1/instances/{instance_id}/payouts/stellar/authorize",
        "payouts.authorize_stellar_token",
        lambda c, o: c.payouts.authorize_stellar_token({"quote_id": ITEM, "sender_wallet_address": "G0"}, o),
        f"{INST}/payouts/stellar/authorize",
    ),
    Op(
        "GET /v1/instances/{instance_id}/payouts/{id}",
        "payouts.get",
        lambda c, o: c.payouts.get(ITEM),
        f"{INST}/payouts/{ITEM}",
    ),
    Op(
        "POST /v1/instances/{instance_id}/payouts/{id}/documents",
        "payouts.submit_documents",
        lambda c, o: c.payouts.submit_documents({"payout_id": ITEM, "transaction_document_type": "invoice"}, o),
        f"{INST}/payouts/{ITEM}/documents",
    ),
    # quotes
    Op(
        "POST /v1/instances/{instance_id}/quotes",
        "quotes.create",
        lambda c, o: c.quotes.create({"bank_account_id": BANK_ACCOUNT}, o),
        f"{INST}/quotes",
    ),
    Op(
        "POST /v1/instances/{instance_id}/quotes/fx",
        "quotes.get_fx_rate",
        lambda c, o: c.quotes.get_fx_rate(
            {"currency_type": "sender", "from_currency": "USDC", "to": "BRL", "request_amount": 1000}, o
        ),
        f"{INST}/quotes/fx",
    ),
    # blockchain helpers
    Op(
        "POST /v1/instances/{instance_id}/mint-usdb-solana",
        "wallets.blockchain.mint_usdb_solana",
        lambda c, o: c.wallets.blockchain.mint_usdb_solana({"address": "So1", "amount": "1"}, o),
        f"{INST}/mint-usdb-solana",
    ),
    Op(
        "POST /v1/instances/{instance_id}/prepare-delegate-solana",
        "wallets.blockchain.prepare_solana_delegation_transaction",
        lambda c, o: c.wallets.blockchain.prepare_solana_delegation_transaction(
            {"owner_address": "So1", "quote_id": "qu_1"}, o
        ),
        f"{INST}/prepare-delegate-solana",
        body={"owner_address": "So1", "quote_id": "qu_1"},
    ),
    Op(
        "POST /v1/instances/{instance_id}/create-asset-trustline",
        "wallets.blockchain.create_asset_trustline",
        lambda c, o: c.wallets.blockchain.create_asset_trustline("G0", o),
        f"{INST}/create-asset-trustline",
    ),
    Op(
        "POST /v1/instances/{instance_id}/mint-usdb-stellar",
        "wallets.blockchain.mint_usdb_stellar",
        lambda c, o: c.wallets.blockchain.mint_usdb_stellar({"address": "G0", "amount": "1"}, o),
        f"{INST}/mint-usdb-stellar",
        body={"address": "G0", "amount": "1"},
    ),
    # terms of service
    Op(
        "POST /v1/e/instances/{instance_id}/tos",
        "instances.terms_of_service.initiate",
        lambda c, o: c.instances.terms_of_service.initiate({"idempotency_key": "tos-1"}, o),
        f"{V1}/e/instances/{INSTANCE}/tos",
    ),
    Op(
        "POST /v1/e/instances/{instance_id}/tos",
        "terms_of_service.initiate",
        lambda c, o: c.terms_of_service.initiate({"idempotency_key": "tos-1"}, o),
        f"{V1}/e/instances/{INSTANCE}/tos",
        note="duplicate of instances.terms_of_service.initiate",
    ),
    # transfers
    Op(
        "POST /v1/instances/{instance_id}/transfer-quotes",
        "transfers.create_quote",
        lambda c, o: c.transfers.create_quote({"wallet_id": ITEM}, o),
        f"{INST}/transfer-quotes",
    ),
    Op(
        "GET /v1/e/transfers/{id}",
        "transfers.get_track",
        lambda c, o: c.transfers.get_track(ITEM),
        f"{V1}/e/transfers/{ITEM}",
        note="tracking endpoint: 401 for server-side callers in production",
    ),
    Op(
        "GET /v1/instances/{instance_id}/transfers",
        "transfers.list",
        lambda c, o: c.transfers.list(),
        f"{INST}/transfers",
    ),
    Op(
        "POST /v1/instances/{instance_id}/transfers",
        "transfers.create",
        lambda c, o: c.transfers.create({"transfer_quote_id": ITEM}, o),
        f"{INST}/transfers",
    ),
    Op(
        "GET /v1/instances/{instance_id}/transfers/{id}",
        "transfers.get",
        lambda c, o: c.transfers.get(ITEM),
        f"{INST}/transfers/{ITEM}",
    ),
    # upload
    Op(
        "POST /v1/upload",
        "upload.create",
        lambda c, o: c.upload.create({"bucket": "avatar", "file": b"%PDF-1.4"}, o),
        f"{V1}/upload",
        multipart=True,
    ),
    Op(
        "POST /v1/upload/analyze",
        "upload.analyze",
        lambda c, o: c.upload.analyze({"type": "invoice", "file": b"%PDF-1.4"}, o),
        f"{V1}/upload/analyze",
        multipart=True,
    ),
    # virtual accounts
    Op(
        "POST /v1/instances/{instance_id}/customers/{customer_id}/virtual-accounts",
        "virtual_accounts.create",
        lambda c, o: c.virtual_accounts.create({"customer_id": CUSTOMER, "token": "USDC"}, o),
        f"{CUST}/virtual-accounts",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/virtual-accounts",
        "virtual_accounts.list",
        lambda c, o: c.virtual_accounts.list(CUSTOMER),
        f"{CUST}/virtual-accounts",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/virtual-accounts/{id}",
        "virtual_accounts.get",
        lambda c, o: c.virtual_accounts.get(CUSTOMER, ITEM),
        f"{CUST}/virtual-accounts/{ITEM}",
    ),
    Op(
        "PUT /v1/instances/{instance_id}/customers/{customer_id}/virtual-accounts/{id}",
        "virtual_accounts.update",
        lambda c, o: c.virtual_accounts.update(CUSTOMER, ITEM, {"token": "USDC"}, o),
        f"{CUST}/virtual-accounts/{ITEM}",
    ),
    # custodial wallets
    Op(
        "POST /v1/instances/{instance_id}/customers/{customer_id}/wallets",
        "wallets.custodial.create",
        lambda c, o: c.wallets.custodial.create({"customer_id": CUSTOMER, "name": "w", "network": "base"}, o),
        f"{CUST}/wallets",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/wallets",
        "wallets.custodial.list",
        lambda c, o: c.wallets.custodial.list(CUSTOMER),
        f"{CUST}/wallets",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/wallets/{id}",
        "wallets.custodial.get",
        lambda c, o: c.wallets.custodial.get({"customer_id": CUSTOMER, "id": ITEM}),
        f"{CUST}/wallets/{ITEM}",
    ),
    Op(
        "DELETE /v1/instances/{instance_id}/customers/{customer_id}/wallets/{id}",
        "wallets.custodial.delete",
        lambda c, o: c.wallets.custodial.delete({"customer_id": CUSTOMER, "id": ITEM}, o),
        f"{CUST}/wallets/{ITEM}",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/wallets/{id}/balance",
        "wallets.custodial.get_balance",
        lambda c, o: c.wallets.custodial.get_balance({"customer_id": CUSTOMER, "id": ITEM}),
        f"{CUST}/wallets/{ITEM}/balance",
    ),
    # webhook endpoints
    Op(
        "POST /v1/instances/{instance_id}/webhook-endpoints",
        "instances.webhook_endpoints.create",
        lambda c, o: c.instances.webhook_endpoints.create(
            {"url": "https://example.com/hook", "events": ["payout.new"]}, o
        ),
        f"{INST}/webhook-endpoints",
    ),
    Op(
        "GET /v1/instances/{instance_id}/webhook-endpoints",
        "instances.webhook_endpoints.list",
        lambda c, o: c.instances.webhook_endpoints.list(),
        f"{INST}/webhook-endpoints",
    ),
    Op(
        "GET /v1/instances/{instance_id}/webhook-endpoints/portal-access",
        "instances.webhook_endpoints.get_portal_access_url",
        lambda c, o: c.instances.webhook_endpoints.get_portal_access_url(),
        f"{INST}/webhook-endpoints/portal-access",
    ),
    Op(
        "DELETE /v1/instances/{instance_id}/webhook-endpoints/{id}",
        "instances.webhook_endpoints.delete",
        lambda c, o: c.instances.webhook_endpoints.delete(ITEM, o),
        f"{INST}/webhook-endpoints/{ITEM}",
    ),
    Op(
        "GET /v1/instances/{instance_id}/webhook-endpoints/{id}/secret",
        "instances.webhook_endpoints.get_secret",
        lambda c, o: c.instances.webhook_endpoints.get_secret(ITEM),
        f"{INST}/webhook-endpoints/{ITEM}/secret",
    ),
    # --- added for 94/94
    Op("GET /v1/instances/{id}", "instances.get", lambda c, o: c.instances.get(), INST),
    Op(
        "GET /v1/instances/{instance_id}/onboarding/business_details",
        "instances.onboarding.get_business_details",
        lambda c, o: c.instances.onboarding.get_business_details(),
        f"{INST}/onboarding/business_details",
    ),
    Op(
        "GET /v1/instances/{instance_id}/onboarding/business_profile",
        "instances.onboarding.get_business_profile",
        lambda c, o: c.instances.onboarding.get_business_profile(),
        f"{INST}/onboarding/business_profile",
    ),
    Op(
        "GET /v1/instances/{instance_id}/onboarding/ownership_documents",
        "instances.onboarding.get_ownership_documents",
        lambda c, o: c.instances.onboarding.get_ownership_documents(),
        f"{INST}/onboarding/ownership_documents",
    ),
    Op("GET /v1/instances/{instance_id}/rfi", "instances.rfi.get", lambda c, o: c.instances.rfi.get(), f"{INST}/rfi"),
    Op(
        "POST /v1/instances/{instance_id}/rfi",
        "instances.rfi.submit",
        lambda c, o: c.instances.rfi.submit({"response": {"tax_id": "123"}}, o),
        f"{INST}/rfi",
        body={"tax_id": "123"},
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/rfi",
        "customers.rfi.get",
        lambda c, o: c.customers.rfi.get(CUSTOMER),
        f"{CUST}/rfi",
    ),
    Op(
        "POST /v1/instances/{instance_id}/customers/{customer_id}/rfi",
        "customers.rfi.submit",
        lambda c, o: c.customers.rfi.submit(
            {"customer_id": CUSTOMER, "response": {"docs": ["https://example.com/a.pdf"]}}, o
        ),
        f"{CUST}/rfi",
        body={"docs": ["https://example.com/a.pdf"]},
    ),
    Op(
        "POST /v1/instances/{instance_id}/customers/{customer_id}/bank-accounts/plaid",
        "customers.bank_accounts.create_plaid_link",
        lambda c, o: c.customers.bank_accounts.create_plaid_link(
            {"customer_id": CUSTOMER, "redirect_url": "https://example.com/done"}, o
        ),
        f"{CUST}/bank-accounts/plaid",
        body={"redirect_url": "https://example.com/done"},
    ),
    Op(
        "PATCH /v1/instances/{instance_id}/customers/{customer_id}/blockchain-wallets/{id}",
        "wallets.blockchain.set_self_custody",
        lambda c, o: c.wallets.blockchain.set_self_custody(
            {"customer_id": CUSTOMER, "id": ITEM, "is_self_custody": True}, o
        ),
        f"{CUST}/blockchain-wallets/{ITEM}",
        body={"is_self_custody": True},
    ),
    Op(
        "PUT /v1/instances/{instance_id}/customers/{customer_id}/bank-accounts/{bank_account_id}/offramp-wallets/{id}",
        "wallets.offramp.update",
        lambda c, o: c.wallets.offramp.update(
            {"customer_id": CUSTOMER, "bank_account_id": BANK_ACCOUNT, "id": ITEM, "partner_fee_id": None}, o
        ),
        f"{CUST}/bank-accounts/{BANK_ACCOUNT}/offramp-wallets/{ITEM}",
        body={"partner_fee_id": None},
    ),
    Op(
        "POST /v1/presign",
        "upload.presign",
        lambda c, o: c.upload.presign({"file_url": "https://example.com/a.pdf"}, o),
        f"{V1}/presign",
        body={"file_url": "https://example.com/a.pdf"},
        query="instance_id=in_000000000000",
    ),
    Op(
        "GET /v1/instances/{instance_id}/customers/{customer_id}/wallets/{id}/deposits",
        "wallets.custodial.get_deposits",
        lambda c, o: c.wallets.custodial.get_deposits({"customer_id": CUSTOMER, "id": ITEM}),
        f"{CUST}/wallets/{ITEM}/deposits",
        query="",
    ),
    Op(
        "POST /v1/instances/{instance_id}/payables",
        "payables.create",
        lambda c, o: c.payables.create(
            {"customer_id": CUSTOMER, "currency": "BRL", "boleto_barcode": "0", "from": {"legal_name": "Acme"}}, o
        ),
        f"{INST}/payables",
        body={"customer_id": CUSTOMER, "currency": "BRL", "boleto_barcode": "0", "from": {"legal_name": "Acme"}},
    ),
    Op(
        "GET /v1/instances/{instance_id}/payables",
        "payables.list",
        lambda c, o: c.payables.list(),
        f"{INST}/payables",
        query="",
    ),
    Op(
        "GET /v1/instances/{instance_id}/payables/{id}",
        "payables.get",
        lambda c, o: c.payables.get(ITEM),
        f"{INST}/payables/{ITEM}",
    ),
    Op(
        "DELETE /v1/instances/{instance_id}/payables/{id}",
        "payables.delete",
        lambda c, o: c.payables.delete(ITEM, o),
        f"{INST}/payables/{ITEM}",
    ),
]
