"""Request inputs follow the spec's ``required`` list (plan C8), checked through spec-map.json's type mapping."""

import importlib
import json
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple, cast

import pytest

ROOT = Path(__file__).resolve().parent.parent
SPEC: Dict[str, Any] = json.loads((ROOT / ".api-sync" / "spec-snapshot.json").read_text())
MAP: Dict[str, Any] = json.loads((ROOT / ".api-sync" / "spec-map.json").read_text())

# The spec's CreateBankAccountIn / CreateBlockchainWalletIn merge every variant into one optional-heavy schema. The
# route validates each variant with its own schema (e.g. CreatePixAccountSchemaIn requires pix_key,
# blindpay-v2/packages/api-contract/src/bank-account.schema.ts), so these per-variant helpers may require more.
PER_VARIANT_HELPERS = {
    "CreatePixInput",
    "CreateArgentinaTransfersInput",
    "CreateSpeiInput",
    "CreateColombiaAchInput",
    "CreateSepaInput",
    "CreatePixSafeInput",
    "CreateTedInput",
    "CreateFasterPaymentsInput",
    "CreateBlockchainWalletWithAddressInput",
    "CreateBlockchainWalletWithHashInput",
}


PATH_PARAMS = {"customer_id", "id", "bank_account_id", "payout_id", "virtual_account_id", "member_id"}


def request_schemas() -> Set[str]:
    names: Set[str] = set()
    for path in SPEC["paths"].values():
        item = cast(Dict[str, Any], path)
        for op in item.values():
            if not isinstance(op, dict) or cast(Dict[str, Any], op).get("x-sdk") is False:
                continue
            body = cast(Dict[str, Any], cast(Dict[str, Any], op).get("requestBody", {}))
            for content in cast(Dict[str, Dict[str, Any]], body.get("content", {})).values():
                ref = str(cast(Dict[str, Any], content.get("schema", {})).get("$ref", ""))
                if ref:
                    names.add(ref.split("/")[-1])
    return names


def cases() -> List[Tuple[str, str, str]]:
    out: List[Tuple[str, str, str]] = []
    wanted = request_schemas()
    for entry in MAP["types"]:
        names = entry["spec"] if isinstance(entry["spec"], list) else [entry["spec"]]
        if entry.get("specPath") or names[0] not in wanted:
            continue
        out.extend((names[0], site["file"], site["symbol"]) for site in entry["sdk"])
    return out


@pytest.mark.parametrize("schema,file,symbol", cases(), ids=[c[2] for c in cases()])
def test_input_required_keys_match_the_spec(schema: str, file: str, symbol: str):
    spec_schema = SPEC["components"]["schemas"][schema]
    properties = set(spec_schema.get("properties", {}))
    required = set(spec_schema.get("required", []))
    cls = getattr(importlib.import_module(file[len("src/") : -len(".py")].replace("/", ".")), symbol)

    under_required = sorted(set(cls.__optional_keys__) & required)
    # Keys the SDK moves into the URL (customer_id, id, ...) aren't body fields; anything else the spec lacks must
    # not be required (stale fields stay but optional, plan D13).
    not_in_spec = sorted(set(cls.__required_keys__) - properties - PATH_PARAMS)
    over_required = sorted((set(cls.__required_keys__) & properties) - required)

    assert not under_required, f"{symbol}: the spec requires {under_required}"
    assert not not_in_spec, f"{symbol}: requires {not_in_spec}, which the spec doesn't have"
    if symbol not in PER_VARIANT_HELPERS:
        assert not over_required, f"{symbol}: the spec makes {over_required} optional"
