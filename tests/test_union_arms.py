"""Every arm of a discriminated response union is checked, not just the first one that happens to pass.

The customer fixtures are all ``individual``/``standard``, so ``value_errors`` alone only ever reaches
``IndividualWithStandardKYC``. ``test_every_customer_arm_matches_the_spec`` rewrites the discriminators of each
fixture variant to each arm's own values, so the enhanced-KYC and business arms are checked against the same
``CustomerOut`` shape.
"""

from typing import Any, Dict, FrozenSet, List, Set, Union, get_args

import pytest
from typing_extensions import Literal, NotRequired, TypedDict

from blindpay import GetCustomerResponse
from tests.spec_fixtures import discriminators, response_variants, value_errors

CUSTOMER_OP = "GET /v1/instances/{instance_id}/customers/{id}"
PHANTOM_KEYS = {"aiprise_validation_key", "individual_holding_doc_front_file"}

# Fields these arms type stricter than the spec's CustomerOut (required keys the spec makes optional, nullable
# fields typed non-null, closed Literals). Relaxing a response field breaks callers that index it under pyright, so
# these wait for the next major. The ledger must stay true: a fix that removes a gap deletes its entry.
KNOWN_ARM_GAPS: Dict[str, FrozenSet[str]] = {
    "IndividualWithEnhancedKYC": frozenset(
        """account_purpose account_purpose_other address_line_1 address_line_2 aml_hits aml_status
        business_description business_industry business_type city country created_at date_of_birth
        estimated_annual_revenue external_id first_name fraud_warnings id_doc_back_file id_doc_country
        id_doc_front_file id_doc_type image_url ip_address is_fbo is_tos_accepted kyc_status kyc_warnings last_name
        occupation phone_number postal_code proof_of_address_doc_file proof_of_address_doc_type publicly_traded
        purpose_of_transactions purpose_of_transactions_explanation selfie_file source_of_funds_doc_file
        source_of_funds_doc_type source_of_wealth state_province_region tax_id tos_id updated_at""".split()
    ),
    "BusinessWithStandardKYB": frozenset(
        """account_purpose account_purpose_other address_line_1 address_line_2 alternate_name aml_hits aml_status
        business_description business_industry business_type city country created_at estimated_annual_revenue
        external_id formation_date fraud_warnings image_url incorporation_doc_file ip_address is_fbo
        is_tos_accepted kyc_status kyc_warnings legal_name occupation owners owners[0].country
        owners[0].id_doc_country owners[0].id_doc_type owners[0].proof_of_address_doc_type owners[0].role
        owners[0].tax_type phone_number postal_code proof_of_address_doc_file proof_of_address_doc_type
        proof_of_ownership_doc_file publicly_traded selfie_file source_of_wealth state_province_region tax_id tos_id
        updated_at website""".split()
    ),
}


def arm_gaps(arm: Any) -> Set[str]:
    keys = discriminators(list(get_args(GetCustomerResponse)))
    gaps: Set[str] = set()
    for payload in response_variants(CUSTOMER_OP).values():
        probe = dict(payload, **{key: sorted(by_arm[arm])[0] for key, by_arm in keys.items()})
        gaps.update(error.split(":")[0].removeprefix("$.") for error in value_errors(arm, probe))
    return gaps


@pytest.mark.parametrize("arm", get_args(GetCustomerResponse), ids=lambda arm: arm.__name__)
def test_every_customer_arm_matches_the_spec(arm: Any):
    gaps = arm_gaps(arm)
    known = KNOWN_ARM_GAPS.get(arm.__name__, frozenset())

    assert not gaps & PHANTOM_KEYS, f"{arm.__name__} requires keys the API never sends: {sorted(gaps & PHANTOM_KEYS)}"
    assert sorted(gaps - known) == [], f"{arm.__name__}: new divergences from CustomerOut"
    assert sorted(known - gaps) == [], f"{arm.__name__}: fixed gaps still in KNOWN_ARM_GAPS"


class _Standard(TypedDict):
    kind: Literal["standard"]
    name: str


class _Enhanced(TypedDict):
    kind: Literal["enhanced"]
    name: str
    extra: str


class _Fallback(TypedDict):
    kind: str
    name: NotRequired[str]


def test_matching_arm_is_checked_even_when_another_arm_passes():
    union: Any = Union[_Standard, _Enhanced, _Fallback]
    payload = {"kind": "enhanced", "name": "x"}

    assert value_errors(union, payload) == ["$.extra: required by _Enhanced but absent"]
    assert value_errors(union, {"kind": "standard", "name": "x"}) == []


def test_unknown_discriminator_falls_back_to_any_arm():
    union: Any = Union[_Standard, _Enhanced, _Fallback]
    unmatched: List[Any] = [{"kind": "zz_unknown_value_from_future_api"}]

    assert value_errors(List[union], unmatched) == []
