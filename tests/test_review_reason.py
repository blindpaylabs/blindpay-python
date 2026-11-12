"""``review_reason`` (spec ``7e49addd9``) on the limit-increase GET response and both ``limitIncrease.*`` webhooks."""

import json
from typing import Any, Dict, List, cast

import pytest

from blindpay import (
    LimitIncreaseNewWebhookEvent,
    LimitIncreaseRequest,
    LimitIncreaseUpdateWebhookEvent,
    webhooks,
)
from tests.spec_fixtures import SPEC_DIR, assert_matches_spec, response_variants, value_errors
from tests.test_webhook_events import NOW, SECRET, signed

GET_OP = "GET /v1/instances/{instance_id}/customers/{customer_id}/limit-increase"


def _webhook_variants(event: str) -> Dict[str, Any]:
    document = json.loads((SPEC_DIR / "webhooks" / f"{event}.json").read_text())
    return cast(Dict[str, Any], document["variants"])


def test_get_limit_increase_requests_decodes_review_reason():
    variants = response_variants(GET_OP)
    full = cast(List[Dict[str, Any]], variants["full"])
    nulls = cast(List[Dict[str, Any]], variants["nullables_null"])

    assert "review_reason" in LimitIncreaseRequest.__annotations__
    # The GET returns a list: check the item type against each variant's first item.
    assert_matches_spec(
        LimitIncreaseRequest,
        {name: cast(List[Dict[str, Any]], variants[name])[0] for name in ("full", "required_only", "nullables_null")},
    )
    assert value_errors(List[LimitIncreaseRequest], full) == []
    assert value_errors(List[LimitIncreaseRequest], nulls) == []
    assert isinstance(full[0]["review_reason"], str) and full[0]["review_reason"]
    assert all(item.get("review_reason") is None for item in nulls)


@pytest.mark.parametrize(
    "event,typed",
    [("limitIncrease.new", LimitIncreaseNewWebhookEvent), ("limitIncrease.update", LimitIncreaseUpdateWebhookEvent)],
)
def test_limit_increase_webhooks_carry_review_reason(event: str, typed: Any):
    variants = _webhook_variants(event)
    assert "review_reason" in typed.__annotations__
    assert_matches_spec(typed, variants)

    for name in ("full", "nullables_null"):
        body = json.dumps(variants[name]).encode()
        parsed = cast(Dict[str, Any], webhooks.construct_event(body, signed(body), SECRET, now=NOW))
        assert value_errors(typed, parsed) == [], name
        if name == "full":
            assert isinstance(parsed["review_reason"], str) and parsed["review_reason"]
        else:
            assert parsed.get("review_reason") is None
