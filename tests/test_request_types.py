"""Request inputs follow the spec's ``required`` list , checked through spec-map.json's type mapping."""

import importlib
import inspect
import json
import typing
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


# Body keys the SDK method sets itself (bank-account/customer helpers inject the discriminator).
INJECTED = {"type", "kyc_type", "is_account_abstraction"}

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
    # not be required (stale fields stay, but optional).
    not_in_spec = sorted(set(cls.__required_keys__) - properties - PATH_PARAMS)
    over_required = sorted((set(cls.__required_keys__) & properties) - required)

    assert not under_required, f"{symbol}: the spec requires {under_required}"
    undeclared = sorted(required - set(cls.__required_keys__) - set(cls.__optional_keys__) - INJECTED)
    assert not undeclared, f"{symbol}: the spec requires {undeclared}, which it doesn't declare"
    assert not not_in_spec, f"{symbol}: requires {not_in_spec}, which the spec doesn't have"
    if symbol not in PER_VARIANT_HELPERS:
        assert not over_required, f"{symbol}: the spec makes {over_required} optional"


# Inline request bodies (no ``$ref``, so spec-map.json can't name them): matched to the SDK method through op_table.
RENAMED = {"from_currency": "from"}  # Python keyword: the method sends the key under its wire name


def inline_bodies() -> List[Tuple[str, Dict[str, Any]]]:
    out: List[Tuple[str, Dict[str, Any]]] = []
    for path, item in cast(Dict[str, Dict[str, Any]], SPEC["paths"]).items():
        for verb, op in item.items():
            if not isinstance(op, dict) or cast(Dict[str, Any], op).get("x-sdk") is False:
                continue
            body = cast(Dict[str, Any], cast(Dict[str, Any], op).get("requestBody", {}))
            for content in cast(Dict[str, Dict[str, Any]], body.get("content", {})).values():
                schema = cast(Dict[str, Any], content.get("schema", {}))
                if "$ref" not in schema:
                    out.append((f"{verb.upper()} {path}", schema))
    return out


def _admits_int(hint: Any) -> bool:
    return hint is int or int in typing.get_args(hint)


def _declared_body(method: Any) -> Tuple[Dict[str, Any], Set[str]]:
    """``(wire key -> hint, required wire keys)`` for the method's body: its ``data`` TypedDict, or its plain params."""
    hints = typing.get_type_hints(method)
    if "data" in hints:
        cls = hints["data"]
        fields: Dict[str, Any] = {RENAMED.get(k, k): v for k, v in typing.get_type_hints(cls).items()}
        required_keys: Set[str] = {RENAMED.get(str(k), str(k)) for k in cls.__required_keys__}
        return fields, required_keys
    params = [p for p in inspect.signature(method).parameters.values() if p.name != "options"]
    return {p.name: hints[p.name] for p in params}, {p.name for p in params if p.default is inspect.Parameter.empty}


INLINE = inline_bodies()


def test_every_inline_body_is_found():
    assert len(INLINE) == 10


@pytest.mark.parametrize("operation,schema", INLINE, ids=[o for o, _ in INLINE])
def test_inline_body_keys_match_the_spec(operation: str, schema: Dict[str, Any]):
    from tests.http_mock import Recorder, sync_client
    from tests.op_table import OPS
    from tests.test_operations import resolve

    (op,) = [op for op in OPS if op.operation == operation]
    properties: Dict[str, Any] = schema.get("properties", {})
    if not properties:  # RFI submit: a free-form map of field ids to answers
        return
    required = set(schema.get("required", []))
    fields, sdk_required = _declared_body(resolve(sync_client(Recorder()), op.method))
    in_spec = set(fields) & set(properties)

    assert not required - sdk_required, f"{op.method}: the spec requires {sorted(required - sdk_required)}"
    over_required = sorted((sdk_required & in_spec) - required)
    assert not over_required, f"{op.method}: the spec makes {over_required} optional"
    assert not (sdk_required - set(properties) - PATH_PARAMS), f"{op.method}: requires keys the spec doesn't have"
    assert not set(properties) - set(fields), f"{op.method}: doesn't model {sorted(set(properties) - set(fields))}"
    integers = sorted(k for k in in_spec if properties[k].get("type") == "integer" and not _admits_int(fields[k]))
    assert not integers, f"{op.method}: the spec types {integers} as integer"


def test_spec_correct_inline_inputs_type_check():
    """pyright and mypy (strict, over tests/) reject this module if a spec-correct literal stops type-checking."""
    from blindpay import (
        CreateOfframpWalletInput,
        CreatePartnerFeeInput,
        GetFxRateInput,
        MintUsdbStellarInput,
        PrepareSolanaDelegationTransactionInput,
    )

    fee: CreatePartnerFeeInput = {
        "name": "fee",
        "payin_flat_fee": 0,
        "payin_percentage_fee": 100,
        "payout_flat_fee": 50,
        "payout_percentage_fee": 0,
    }
    legacy_fee: CreatePartnerFeeInput = {**fee, "evm_wallet_address": "0x0", "payin_flat_fee": 1.0}
    offramp: CreateOfframpWalletInput = {"customer_id": "cu_1", "bank_account_id": "ba_1", "network": "tron"}
    delegation: PrepareSolanaDelegationTransactionInput = {"owner_address": "So1", "quote_id": "qu_1"}
    mint: MintUsdbStellarInput = {"address": "G0", "amount": "1"}
    fx: GetFxRateInput = {"currency_type": "sender", "from_currency": "USDC", "to": "BRL", "request_amount": 1000}

    assert [fee, legacy_fee, offramp, delegation, mint, fx]
