"""Op-level tests driven by ``tests/op_table.py`` (plan Appendix A8), in both clients.

- Guard (C2): every mutating method forwards its request options (headers, timeout, idempotency key) to the wire,
  and the table lists every mutating method in the SDK, so a new method can't skip ``options``.
- Op coverage: every method sends the right HTTP method to the exact path, and every response fixture variant of
  its operation comes back as ``data`` without an error.
"""

import ast
import inspect
import json
import typing
from pathlib import Path
from typing import Any, Dict, List, Set

import httpx
import pytest

from blindpay import RequestOptions
from blindpay.types import BlindpaySuccessResponse
from tests.http_mock import async_client, sync_client
from tests.op_table import OPS, Op
from tests.spec_fixtures import SPEC_DIR, load_index, variant_errors

SRC = Path(__file__).resolve().parent.parent / "src" / "blindpay" / "resources"
MUTATING_VERBS = {"post", "put", "patch", "delete", "post_multipart"}
KINDS = ["async", "sync"]

GUARD_OPTIONS: RequestOptions = {"headers": {"X-Guard": "forwarded"}, "idempotency_key": "guard-key", "timeout": 7}


class Recorder:
    def __init__(self, body: Any = None) -> None:
        self.requests: List[httpx.Request] = []
        self.body = body

    def __call__(self, request: httpx.Request) -> httpx.Response:
        request.read()
        self.requests.append(request)
        return httpx.Response(200, content=json.dumps(self.body if self.body is not None else {}).encode())


async def run(kind: str, op: Op, recorder: Recorder, options: Any = None) -> Any:
    client: Any = async_client(recorder) if kind == "async" else sync_client(recorder)
    result = op.call(client, options)
    return await result if kind == "async" else result


def resolve(client: Any, accessor: str) -> Any:
    target = client
    for part in accessor.split("."):
        target = getattr(target, part)
    return target


def mutating_methods_in_source() -> Set[str]:
    """``Class.method`` for every public resource method whose first client call is a mutating verb."""
    found: Set[str] = set()
    for path in SRC.rglob("*.py"):
        for cls in ast.parse(path.read_text()).body:
            if not isinstance(cls, ast.ClassDef):
                continue
            for fn in cls.body:
                if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) or fn.name.startswith("_"):
                    continue
                for node in ast.walk(fn):
                    func = node.func if isinstance(node, ast.Call) else None
                    if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Attribute):
                        if func.value.attr == "_client":
                            if func.attr in MUTATING_VERBS:
                                found.add(f"{cls.name}.{fn.name}")
                            break
    return found


MUTATING = [op for op in OPS if op.mutating]


class TestGuard:
    def test_table_lists_every_mutating_method_of_both_clients(self):
        listed: Set[str] = set()
        for op in MUTATING:
            for client in (async_client(Recorder()), sync_client(Recorder())):
                listed.add(resolve(client, op.method).__func__.__qualname__)

        assert listed == mutating_methods_in_source()

    @pytest.mark.parametrize("qualname", sorted(mutating_methods_in_source()))
    def test_every_mutating_method_takes_options_last(self, qualname: str):
        class_name, method = qualname.split(".")
        module_classes: Dict[str, Any] = {}
        for op in MUTATING:
            for client in (async_client(Recorder()), sync_client(Recorder())):
                bound = resolve(client, op.method)
                module_classes[bound.__func__.__qualname__.split(".")[0]] = type(bound.__self__)
        parameters = list(inspect.signature(getattr(module_classes[class_name], method)).parameters.values())

        assert parameters[-1].name == "options"
        assert parameters[-1].default is None

    @pytest.mark.parametrize("kind", KINDS)
    @pytest.mark.parametrize("op", MUTATING, ids=[op.method for op in MUTATING])
    async def test_mutating_method_forwards_options(self, kind: str, op: Op):
        recorder = Recorder()

        await run(kind, op, recorder, GUARD_OPTIONS)

        request = recorder.requests[-1]
        assert request.headers["X-Guard"] == "forwarded"
        assert request.extensions["timeout"]["read"] == 7
        expected_key = None if op.multipart else "guard-key"
        assert request.headers.get("Idempotency-Key") == expected_key


def fixture_variants(operation: str) -> Dict[str, Any]:
    entry = load_index()["operations"][operation]
    document = json.loads((SPEC_DIR / (entry if isinstance(entry, str) else entry["file"])).read_text())
    variants: Dict[str, Any] = {}
    for status, response in document.get("responses", {}).items():
        if status.startswith("2"):
            variants.update({f"{status}:{name}": value for name, value in response["variants"].items()})
    return variants


class TestOperations:
    @pytest.mark.parametrize("kind", KINDS)
    @pytest.mark.parametrize("op", OPS, ids=[op.method for op in OPS])
    async def test_method_and_exact_path(self, kind: str, op: Op):
        recorder = Recorder()

        response = await run(kind, op, recorder)

        assert response["error"] is None
        request = recorder.requests[-1]
        assert request.method == op.http_method
        assert request.url.raw_path.split(b"?")[0].decode() == op.path

    @pytest.mark.parametrize("kind", KINDS)
    @pytest.mark.parametrize("op", OPS, ids=[op.method for op in OPS])
    async def test_every_fixture_variant_comes_back_as_data(self, kind: str, op: Op):
        variants = fixture_variants(op.operation)
        assert variants, f"no 2xx fixture for {op.operation}"
        for name, payload in variants.items():
            response = await run(kind, op, Recorder(payload))

            assert response == {"data": payload, "error": None}, name


def response_type(op: Op) -> Any:
    """``T`` from the method's ``BlindpayApiResponse[T]`` return annotation."""
    method = resolve(sync_client(Recorder()), op.method)
    for arm in typing.get_args(typing.get_type_hints(method)["return"]):
        if typing.get_origin(arm) is BlindpaySuccessResponse:
            return typing.get_args(arm)[0]
    raise AssertionError(f"{op.method} doesn't return BlindpayApiResponse[...]")


# Response types that don't yet match their spec fixtures (C7 open enums, C8 optional/nullable fields).
# Strict: fixing a type makes its entry fail until it's removed here. Must be empty when M3 is done.
KNOWN_DRIFT: Set[str] = {
    "available.get_bank_details",
    "available.get_naics_codes",
    "available.get_rails",
    "customers.bank_accounts.create_pix",
    "customers.bank_accounts.create_argentina_transfers",
    "customers.bank_accounts.create_spei",
    "customers.bank_accounts.create_colombia_ach",
    "customers.bank_accounts.create_ach",
    "customers.bank_accounts.create_wire",
    "customers.bank_accounts.create_international_swift",
    "customers.bank_accounts.create_rtp",
    "customers.bank_accounts.create_pix_safe",
    "customers.bank_accounts.create_ted",
    "customers.bank_accounts.create_sepa",
    "customers.bank_accounts.list",
    "customers.bank_accounts.get",
    "wallets.blockchain.create_with_address",
    "wallets.blockchain.create_with_hash",
    "wallets.blockchain.list",
    "wallets.blockchain.get",
    "wallets.blockchain.set_self_custody",
    "customers.list",
    "customers.get_limit_increase_requests",
    "customers.get",
    "fees.get",
    "instances.get_members",
    "wallets.offramp.create",
    "wallets.offramp.list",
    "wallets.offramp.get",
    "partner_fees.create",
    "partner_fees.list",
    "partner_fees.get",
    "payins.quotes.create",
    "payins.quotes.get_fx_rate",
    "payins.get_track",
    "payins.list",
    "payins.create_evm",
    "payins.get",
    "payouts.get_track",
    "payouts.list",
    "payouts.create_evm",
    "payouts.create_solana",
    "payouts.create_stellar",
    "payouts.get",
    "payouts.submit_documents",
    "quotes.create",
    "quotes.get_fx_rate",
    "wallets.blockchain.mint_usdb_solana",
    "wallets.blockchain.prepare_solana_delegation_transaction",
    "transfers.create_quote",
    "transfers.get_track",
    "transfers.list",
    "transfers.create",
    "transfers.get",
    "upload.analyze",
    "virtual_accounts.create",
    "virtual_accounts.list",
    "virtual_accounts.get",
    "wallets.custodial.create",
    "wallets.custodial.list",
    "wallets.custodial.get",
    "instances.webhook_endpoints.list",
}


@pytest.mark.parametrize("op", OPS, ids=[op.method for op in OPS])
def test_response_type_matches_every_fixture_variant(op: Op):
    """The static "decode" (plan §1.2, A8): each variant of the op's fixture against the method's response type.
    Required keys, nullability, open enums for ``unknown_enum``, decimals, and no fields the spec lacks."""
    errors = variant_errors(response_type(op), fixture_variants(op.operation))
    if op.method in KNOWN_DRIFT:
        assert errors, f"{op.method} now matches the spec: remove it from KNOWN_DRIFT"
        return
    assert not errors, "\n".join(sorted(set(errors)))
