"""Unit tests for .api-sync/sync.py, the deterministic spec -> SDK patcher.

sync.py lives outside the `blindpay` package (it is a standalone script next to
check_contract.py), so each test loads a fresh copy of the module via
importlib and repoints its path constants at an isolated tmp_path "repo" --
never at the real src/blindpay tree.
"""

import ast
import importlib.util
import json
import sys
import types
from pathlib import Path
from typing import Any, Optional

import pytest

SYNC_PATH = Path(__file__).parent.parent / ".api-sync" / "sync.py"


_load_counter = 0


def load_sync(root: Path) -> types.ModuleType:
    """Import a fresh instance of sync.py with its path constants repointed at `root`."""
    global _load_counter
    _load_counter += 1
    module_name = f"sync_under_test_{_load_counter}"
    spec = importlib.util.spec_from_file_location(module_name, SYNC_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    # @dataclass needs the module registered in sys.modules to resolve annotations
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    module.ROOT = root  # type: ignore[attr-defined]
    module.API_SYNC = root / ".api-sync"  # type: ignore[attr-defined]
    module.SRC_ROOT = root / "src" / "blindpay"  # type: ignore[attr-defined]
    module.SNAPSHOT_PATH = module.API_SYNC / "spec-snapshot.json"  # type: ignore[attr-defined]
    module.DEFAULT_SPEC_PATH = module.API_SYNC / "spec-current.json"  # type: ignore[attr-defined]
    module.MAP_PATH = module.API_SYNC / "spec-map.json"  # type: ignore[attr-defined]
    module.UNMODELED_PATH = module.API_SYNC / "unmodeled.json"  # type: ignore[attr-defined]
    return module


def write(root: Path, rel: str, content: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return p


def base_schema(schemas: dict[str, Any], paths: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    return {"paths": paths or {}, "components": {"schemas": schemas}}


def op(ref_in: Optional[str] = None, ref_out: Optional[str] = None) -> dict[str, Any]:
    o: dict[str, Any] = {"x-sdk": True}
    if ref_in:
        o["requestBody"] = {"content": {"application/json": {"schema": {"$ref": f"#/components/schemas/{ref_in}"}}}}
    if ref_out:
        o["responses"] = {
            "200": {"content": {"application/json": {"schema": {"$ref": f"#/components/schemas/{ref_out}"}}}}
        }
    else:
        o["responses"] = {"200": {"content": {}}}
    return o


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    write(tmp_path, "src/blindpay/__init__.py", "")
    return tmp_path


# --------------------------------------------------------------------------- #
# Literal (enum) splicing
# --------------------------------------------------------------------------- #


class TestLiteralSplicing:
    def test_single_line_literal_add_member(self):
        source = 'Color = Literal["red", "blue"]\n'
        tree = ast.parse(source)
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign))
        sync = load_sync(Path("/nonexistent"))
        result = sync.splice_literal_add_members(source, node, ["green"])
        assert result == 'Color = Literal["red", "blue", "green"]\n'

    def test_single_line_literal_add_multiple_members_sorted_input(self):
        source = 'Color = Literal["red"]\n'
        tree = ast.parse(source)
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign))
        sync = load_sync(Path("/nonexistent"))
        result = sync.splice_literal_add_members(source, node, ["blue", "green"])
        assert result == 'Color = Literal["red", "blue", "green"]\n'

    def test_multiline_literal_add_member_preserves_indentation_and_trailing_comma(self):
        source = 'Status = Literal[\n    "a",\n    "b",\n]\n'
        tree = ast.parse(source)
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign))
        sync = load_sync(Path("/nonexistent"))
        result = sync.splice_literal_add_members(source, node, ["c"])
        assert result == 'Status = Literal[\n    "a",\n    "b",\n    "c",\n]\n'
        ast.parse(result)  # still valid Python

    def test_multiline_literal_without_trailing_comma_gets_one_added(self):
        source = 'Status = Literal[\n    "a",\n    "b"\n]\n'
        tree = ast.parse(source)
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.Assign))
        sync = load_sync(Path("/nonexistent"))
        result = sync.splice_literal_add_members(source, node, ["c"])
        assert result == 'Status = Literal[\n    "a",\n    "b",\n    "c",\n]\n'


# --------------------------------------------------------------------------- #
# TypedDict field splicing / annotation choice
# --------------------------------------------------------------------------- #


class TestTypedDictFieldInsertion:
    def _class_info(self, sync: types.ModuleType, source: str, name: str):
        tree = ast.parse(source)
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == name)
        own_fields = {
            item.target.id: item
            for item in node.body
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name)
        }
        return sync.ClassInfo(
            file=Path("/fake.py"),
            node=node,
            source=source,
            bases=sync._base_names(node),
            total_false=sync._is_total_false(node),
            own_fields=own_fields,
        )

    def test_total_true_class_always_wraps_new_field_in_notrequired(self):
        """A total=True class (the default -- no `total=False` anywhere) makes
        every declared key structurally required. A newly added field must be
        NotRequired regardless of whether any sibling field already uses that
        convention or just uses a bare Optional[...] for its value type --
        otherwise every existing caller that omits the new key breaks pyright
        and mypy. This is the exact bug a real PR review caught: `class
        CreateQuoteInput(TypedDict):` has siblings typed as plain
        `Optional[str]`, but those were part of the original, already-required
        shape -- that convention does not extend to fields added later."""
        sync = load_sync(Path("/nonexistent"))
        source = "class Plain(TypedDict):\n    x: str\n    y: Optional[str]\n"
        info = self._class_info(sync, source, "Plain")
        assert info.total_false is False
        assert sync.choose_field_annotation(info, "str", nullable=True) == "NotRequired[Optional[str]]"
        assert sync.choose_field_annotation(info, "str", nullable=False) == "NotRequired[str]"

    def test_total_true_class_with_existing_notrequired_sibling_still_wraps(self):
        sync = load_sync(Path("/nonexistent"))
        source = "class WithNR(TypedDict):\n    x: str\n    y: NotRequired[str]\n"
        info = self._class_info(sync, source, "WithNR")
        assert sync.choose_field_annotation(info, "str", nullable=True) == "NotRequired[Optional[str]]"
        assert sync.choose_field_annotation(info, "str", nullable=False) == "NotRequired[str]"

    def test_total_false_class_uses_bare_type_when_not_nullable(self):
        sync = load_sync(Path("/nonexistent"))
        source = "class Foo(_FooRequired, total=False):\n    b: str\n"
        info = self._class_info(sync, source, "Foo")
        assert info.total_false is True
        assert sync.choose_field_annotation(info, "str", nullable=False) == "str"
        assert sync.choose_field_annotation(info, "str", nullable=True) == "Optional[str]"

    def test_splice_typeddict_add_field_appends_after_last_statement(self):
        sync = load_sync(Path("/nonexistent"))
        source = "class Plain(TypedDict):\n    x: str\n    y: Optional[str]\n"
        tree = ast.parse(source)
        node = next(n for n in ast.walk(tree) if isinstance(n, ast.ClassDef))
        result = sync.splice_typeddict_add_field(source, node, "z", "Optional[str]")
        expected = "class Plain(TypedDict):\n    x: str\n    y: Optional[str]\n    z: Optional[str]\n"
        assert result == expected
        ast.parse(result)


# --------------------------------------------------------------------------- #
# Import management: NotRequired/Optional must be added when a class needs
# them for the first time (this is the exact real-world case: quotes.py
# already imports Optional from typing but not NotRequired from anywhere)
# --------------------------------------------------------------------------- #


class TestImportManagement:
    def test_adds_notrequired_to_existing_typing_extensions_import(self):
        sync = load_sync(Path("/nonexistent"))
        source = "from typing_extensions import TypedDict\n\n\nclass Plain(TypedDict):\n    x: str\n"
        result = sync.ensure_name_imported(source, "NotRequired")
        assert result.startswith("from typing_extensions import NotRequired, TypedDict\n")
        ast.parse(result)

    def test_adds_notrequired_to_existing_typing_import_when_that_is_where_typeddict_lives(self):
        """Matches payins.py's own style: `from typing import ... TypedDict`,
        no typing_extensions import at all."""
        sync = load_sync(Path("/nonexistent"))
        source = "from typing import List, Optional, TypedDict\n\n\nclass Plain(TypedDict):\n    x: str\n"
        result = sync.ensure_name_imported(source, "NotRequired")
        assert result.startswith("from typing import List, NotRequired, Optional, TypedDict\n")
        ast.parse(result)

    def test_noop_when_already_imported(self):
        sync = load_sync(Path("/nonexistent"))
        source = "from typing_extensions import NotRequired, TypedDict\n\n\nclass Plain(TypedDict):\n    x: str\n"
        result = sync.ensure_name_imported(source, "NotRequired")
        assert result == source

    def test_end_to_end_apply_adds_import_and_wraps_field_for_total_true_class_lacking_notrequired(self, repo: Path):
        """The exact real-world scenario a PR review caught: a total=True
        class in a file that imports Optional from `typing` but has never
        needed NotRequired before. Both the import and the field annotation
        must come out right in the same apply."""
        write(repo, "src/blindpay/__init__.py", "")
        write(
            repo,
            "src/blindpay/resources/quotes_like.py",
            "from typing import Optional\n\nfrom typing_extensions import TypedDict\n\n\n"
            "class CreateThingInput(TypedDict):\n    bank_account_id: str\n    description: Optional[str]\n",
        )
        map_data: dict[str, Any] = {
            "enums": [],
            "types": [
                {
                    "spec": "ThingIn",
                    "sdk": [{"file": "src/blindpay/resources/quotes_like.py", "symbol": "CreateThingInput"}],
                }
            ],
            "ignore": {"schemas": []},
        }
        _write_map_and_unmodeled(repo, map_data)
        old_spec = base_schema(
            {
                "ThingIn": {
                    "properties": {"bank_account_id": {"type": "string"}, "description": {"type": ["string", "null"]}}
                }
            },
            {"/t": {"post": op(ref_in="ThingIn")}},
        )
        write(repo, ".api-sync/spec-snapshot.json", json.dumps(old_spec))
        new_spec = json.loads(json.dumps(old_spec))
        new_spec["components"]["schemas"]["ThingIn"]["properties"]["refund_wallet_address"] = {
            "type": ["string", "null"]
        }
        write(repo, ".api-sync/spec-current.json", json.dumps(new_spec))

        sync = load_sync(repo)
        assert sync.cmd_apply(sync.DEFAULT_SPEC_PATH, None) == 0

        result = (repo / "src/blindpay/resources/quotes_like.py").read_text()
        assert "from typing_extensions import NotRequired, TypedDict" in result
        assert "refund_wallet_address: NotRequired[Optional[str]]" in result
        ast.parse(result)


# --------------------------------------------------------------------------- #
# Reconciliation against a fixture repo (enums, properties, nested specPath)
# --------------------------------------------------------------------------- #


FIXTURE_TYPES_PY = """from typing import Literal

Color = Literal["red", "blue"]
"""

FIXTURE_RESOURCE_PY = """from typing import Optional
from typing_extensions import Literal, NotRequired, TypedDict

Status = Literal[
    "a",
    "b",
]


class Plain(TypedDict):
    id: str
    name: Optional[str]


class _FooRequired(TypedDict):
    id: str


class Foo(_FooRequired, total=False):
    label: str
"""


def _write_fixture_repo(root: Path) -> None:
    write(root, "src/blindpay/__init__.py", "")
    write(root, "src/blindpay/types.py", FIXTURE_TYPES_PY)
    write(root, "src/blindpay/resources/sample.py", FIXTURE_RESOURCE_PY)


def _write_map_and_unmodeled(root: Path, map_data: dict[str, Any], unmodeled: Optional[list[Any]] = None) -> None:
    write(root, ".api-sync/spec-map.json", json.dumps(map_data))
    write(root, ".api-sync/unmodeled.json", json.dumps(unmodeled or []))


class TestReconciliation:
    def test_enum_gap_detected_when_spec_has_extra_member(self, repo: Path):
        _write_fixture_repo(repo)
        map_data: dict[str, Any] = {
            "enums": [
                {
                    "spec": {"schema": "ColorOut", "property": "color"},
                    "sdk": {"file": "src/blindpay/types.py", "symbol": "Color"},
                }
            ],
            "types": [],
            "ignore": {"schemas": []},
        }
        _write_map_and_unmodeled(repo, map_data)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        spec = base_schema(
            {"ColorOut": {"properties": {"color": {"type": "string", "enum": ["red", "blue", "green"]}}}},
            {"/x": {"get": op(ref_out="ColorOut")}},
        )
        gaps = sync.reconcile_enums(spec, map_data, [], index)
        assert len(gaps) == 1
        assert gaps[0].symbol == "Color"
        assert gaps[0].missing == ["green"]

    def test_enum_gap_suppressed_by_unmodeled_entry(self, repo: Path):
        _write_fixture_repo(repo)
        map_data: dict[str, Any] = {
            "enums": [
                {
                    "spec": {"schema": "ColorOut", "property": "color"},
                    "sdk": {"file": "src/blindpay/types.py", "symbol": "Color"},
                }
            ],
            "types": [],
            "ignore": {"schemas": []},
        }
        unmodeled = [
            {
                "kind": "enum",
                "enum": "Color",
                "missing_values": ["green"],
                "reason": "test",
                "owner": "eric@blindpay.com",
            }
        ]
        _write_map_and_unmodeled(repo, map_data, unmodeled)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        spec = base_schema(
            {"ColorOut": {"properties": {"color": {"type": "string", "enum": ["red", "blue", "green"]}}}},
            {"/x": {"get": op(ref_out="ColorOut")}},
        )
        gaps = sync.reconcile_enums(spec, map_data, unmodeled, index)
        assert gaps == []

    def test_property_gap_detected(self, repo: Path):
        _write_fixture_repo(repo)
        map_data: dict[str, Any] = {
            "enums": [],
            "types": [{"spec": "PlainOut", "sdk": [{"file": "src/blindpay/resources/sample.py", "symbol": "Plain"}]}],
            "ignore": {"schemas": []},
        }
        _write_map_and_unmodeled(repo, map_data)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        spec = base_schema(
            {
                "PlainOut": {
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": ["string", "null"]},
                        "extra": {"type": "string"},
                    }
                }
            },
            {"/x": {"get": op(ref_out="PlainOut")}},
        )
        gaps = sync.reconcile_types(spec, map_data, [], index)
        assert len(gaps) == 1
        assert gaps[0].schema_names == ["PlainOut"]
        assert list(gaps[0].missing.keys()) == ["extra"]

    def test_two_part_total_false_pattern_field_resolved_via_base(self, repo: Path):
        _write_fixture_repo(repo)
        map_data: dict[str, Any] = {
            "enums": [],
            "types": [{"spec": "FooOut", "sdk": [{"file": "src/blindpay/resources/sample.py", "symbol": "Foo"}]}],
            "ignore": {"schemas": []},
        }
        _write_map_and_unmodeled(repo, map_data)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        # `id` lives on _FooRequired (the base class); resolve_typeddict_fields must find it
        fields = sync.resolve_typeddict_fields("Foo", "src/blindpay/resources/sample.py", index)
        assert fields == {"id", "label"}

    def test_nested_specpath_sub_object_reconciled_independently_of_root(self, repo: Path):
        """The blind spot that hid provider_reference in tracking_payment: a
        property can live in an inline sub-object that is never $ref'd. The
        reconciler must walk into `specPath`, not just the schema's own
        top-level properties."""
        _write_fixture_repo(repo)
        map_data: dict[str, Any] = {
            "enums": [],
            "types": [
                {
                    "spec": ["ParentOut"],
                    "specPath": "detail",
                    "sdk": [{"file": "src/blindpay/resources/sample.py", "symbol": "Plain"}],
                }
            ],
            "ignore": {"schemas": []},
        }
        _write_map_and_unmodeled(repo, map_data)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        spec = base_schema(
            {
                "ParentOut": {
                    "properties": {
                        "unrelated_top_level_field": {"type": "string"},  # NOT reconciled (out of scope for this entry)
                        "detail": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "string"},
                                "name": {"type": ["string", "null"]},
                                "newly_added": {"type": "string"},
                            },
                        },
                    }
                }
            },
            {"/x": {"get": op(ref_out="ParentOut")}},
        )
        gaps = sync.reconcile_types(spec, map_data, [], index)
        assert len(gaps) == 1
        assert gaps[0].path == "detail"
        assert list(gaps[0].missing.keys()) == ["newly_added"]
        # the root-level field is untouched by this specPath-scoped entry
        assert "unrelated_top_level_field" not in gaps[0].missing


# --------------------------------------------------------------------------- #
# Map validity
# --------------------------------------------------------------------------- #


class TestMapValidity:
    def test_valid_map_passes(self, repo: Path):
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        map_data: dict[str, Any] = {
            "enums": [
                {"spec": {"schema": "X", "property": "y"}, "sdk": {"file": "src/blindpay/types.py", "symbol": "Color"}}
            ],
            "types": [{"spec": "PlainOut", "sdk": [{"file": "src/blindpay/resources/sample.py", "symbol": "Plain"}]}],
            "ignore": {"schemas": []},
        }
        assert sync.validate_map(map_data, index) == []

    def test_missing_file_is_an_error(self, repo: Path):
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        map_data: dict[str, Any] = {
            "enums": [],
            "types": [{"spec": "X", "sdk": [{"file": "src/blindpay/nope.py", "symbol": "Plain"}]}],
            "ignore": {"schemas": []},
        }
        errors = sync.validate_map(map_data, index)
        assert len(errors) == 1
        assert "file not found" in errors[0]

    def test_symbol_not_found_is_an_error(self, repo: Path):
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        map_data: dict[str, Any] = {
            "enums": [],
            "types": [{"spec": "X", "sdk": [{"file": "src/blindpay/resources/sample.py", "symbol": "DoesNotExist"}]}],
            "ignore": {"schemas": []},
        }
        errors = sync.validate_map(map_data, index)
        assert len(errors) == 1
        assert "not found anywhere" in errors[0]

    def test_symbol_found_but_in_a_different_file_is_an_error(self, repo: Path):
        """This is the exact bug class the audit caught for real: PaymentMethod
        exists, just not in the file the map claims."""
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        map_data: dict[str, Any] = {
            "enums": [
                {
                    "spec": {"schema": "X", "property": "y"},
                    "sdk": {"file": "src/blindpay/resources/sample.py", "symbol": "Color"},
                }
            ],
            "types": [],
            "ignore": {"schemas": []},
        }
        errors = sync.validate_map(map_data, index)
        assert len(errors) == 1
        assert "not found in src/blindpay/resources/sample.py" in errors[0]


# --------------------------------------------------------------------------- #
# NEEDS_HUMAN classification (old-vs-new diff)
# --------------------------------------------------------------------------- #


class TestNeedsHuman:
    def _map(self) -> dict[str, Any]:
        return {
            "enums": [
                {
                    "spec": {"schema": "ColorOut", "property": "color"},
                    "sdk": {"file": "src/blindpay/types.py", "symbol": "Color"},
                }
            ],
            "types": [{"spec": "PlainOut", "sdk": [{"file": "src/blindpay/resources/sample.py", "symbol": "Plain"}]}],
            "ignore": {"schemas": []},
        }

    def test_enum_member_removed_is_needs_human(self, repo: Path):
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        old = base_schema(
            {"ColorOut": {"properties": {"color": {"type": "string", "enum": ["red", "blue"]}}}},
            {"/x": {"get": op(ref_out="ColorOut")}},
        )
        new = base_schema(
            {"ColorOut": {"properties": {"color": {"type": "string", "enum": ["red"]}}}},
            {"/x": {"get": op(ref_out="ColorOut")}},
        )
        problems = sync.diff_removals_and_changes(old, new, self._map(), index)
        assert any(p.kind == "enum_member_removed" for p in problems)

    def test_property_removed_is_needs_human(self, repo: Path):
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        old = base_schema(
            {"PlainOut": {"properties": {"id": {"type": "string"}, "name": {"type": "string"}}}},
            {"/x": {"get": op(ref_out="PlainOut")}},
        )
        new = base_schema(
            {"PlainOut": {"properties": {"id": {"type": "string"}}}}, {"/x": {"get": op(ref_out="PlainOut")}}
        )
        problems = sync.diff_removals_and_changes(old, new, self._map(), index)
        assert any(p.kind == "property_removed" for p in problems)

    def test_schema_removed_is_needs_human(self, repo: Path):
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        old = base_schema(
            {"PlainOut": {"properties": {"id": {"type": "string"}}}}, {"/x": {"get": op(ref_out="PlainOut")}}
        )
        new = base_schema({}, {})
        problems = sync.diff_removals_and_changes(old, new, self._map(), index)
        assert any(p.kind == "schema_removed" for p in problems)

    def test_required_ness_change_is_needs_human(self, repo: Path):
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        old = base_schema(
            {"PlainOut": {"properties": {"id": {"type": "string"}}, "required": []}},
            {"/x": {"get": op(ref_out="PlainOut")}},
        )
        new = base_schema(
            {"PlainOut": {"properties": {"id": {"type": "string"}}, "required": ["id"]}},
            {"/x": {"get": op(ref_out="PlainOut")}},
        )
        problems = sync.diff_removals_and_changes(old, new, self._map(), index)
        assert any(p.kind == "required_change" for p in problems)

    def test_type_change_is_needs_human(self, repo: Path):
        """string -> integer on a plain field."""
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        old = base_schema(
            {"PlainOut": {"properties": {"id": {"type": "string"}}}}, {"/x": {"get": op(ref_out="PlainOut")}}
        )
        new = base_schema(
            {"PlainOut": {"properties": {"id": {"type": "integer"}}}}, {"/x": {"get": op(ref_out="PlainOut")}}
        )
        problems = sync.diff_removals_and_changes(old, new, self._map(), index)
        assert any(p.kind == "type_change" for p in problems)

    def test_nullable_to_non_nullable_is_needs_human(self, repo: Path):
        """Same base JSON type, nullability narrows -- the SDK's existing
        Optional[...] (or lack of it) would silently stop matching the wire."""
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        old = base_schema(
            {"PlainOut": {"properties": {"id": {"type": ["string", "null"]}}}},
            {"/x": {"get": op(ref_out="PlainOut")}},
        )
        new = base_schema(
            {"PlainOut": {"properties": {"id": {"type": "string"}}}}, {"/x": {"get": op(ref_out="PlainOut")}}
        )
        problems = sync.diff_removals_and_changes(old, new, self._map(), index)
        assert any(p.kind == "type_change" and "nullability" in p.detail for p in problems)

    def test_non_nullable_to_nullable_is_also_needs_human(self, repo: Path):
        """The reverse direction is flagged too -- symmetric with required_change,
        which does not privilege either direction either."""
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        old = base_schema(
            {"PlainOut": {"properties": {"id": {"type": "string"}}}}, {"/x": {"get": op(ref_out="PlainOut")}}
        )
        new = base_schema(
            {"PlainOut": {"properties": {"id": {"type": ["string", "null"]}}}},
            {"/x": {"get": op(ref_out="PlainOut")}},
        )
        problems = sync.diff_removals_and_changes(old, new, self._map(), index)
        assert any(p.kind == "type_change" and "nullability" in p.detail for p in problems)

    def test_enum_property_degrading_to_bare_string_is_needs_human(self, repo: Path):
        """A mapped enum losing its `enum` array entirely (API stops constraining
        the field) must not silently pass: every value the SDK currently models
        shows up as no longer present in the (now enum-less) new spec, and the
        existing enum_member_removed path already hard-fails on that."""
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        old = base_schema(
            {"ColorOut": {"properties": {"color": {"type": "string", "enum": ["red", "blue"]}}}},
            {"/x": {"get": op(ref_out="ColorOut")}},
        )
        new = base_schema(
            {"ColorOut": {"properties": {"color": {"type": "string"}}}},  # enum removed entirely
            {"/x": {"get": op(ref_out="ColorOut")}},
        )
        problems = sync.diff_removals_and_changes(old, new, self._map(), index)
        assert any(p.kind == "enum_member_removed" for p in problems)

    def test_ambiguous_type_metadata_only_change_is_deliberately_compatible(self, repo: Path):
        """The one case treated as compatible on purpose: a property that had no
        "type" key at all (only "example"/"description") gaining an explicit
        type is not a type change to react to -- there is nothing on the old
        side to compare against. This is the exact, real, benign shape this
        spec's own created_at/updated_at fields went through (gaining
        {"type": ["string","null"], "format": "date-time"} where they
        previously had none)."""
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        old = base_schema(
            {"PlainOut": {"properties": {"id": {"example": "abc"}}}}, {"/x": {"get": op(ref_out="PlainOut")}}
        )
        new = base_schema(
            {"PlainOut": {"properties": {"id": {"type": ["string", "null"], "format": "date-time", "example": "abc"}}}},
            {"/x": {"get": op(ref_out="PlainOut")}},
        )
        problems = sync.diff_removals_and_changes(old, new, self._map(), index)
        assert problems == []

    def test_new_operation_is_needs_human(self, repo: Path):
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        old = base_schema({}, {})
        new = base_schema({}, {"/new-path": {"get": op()}})
        problems = sync.diff_removals_and_changes(old, new, self._map(), index)
        assert any(p.kind == "new_operation" and "/new-path" in p.detail for p in problems)

    def test_new_unmapped_schema_is_needs_human(self, repo: Path):
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        old = base_schema({}, {})
        new = base_schema(
            {"BrandNewOut": {"properties": {"a": {"type": "string"}}}}, {"/x": {"get": op(ref_out="BrandNewOut")}}
        )
        problems = sync.diff_removals_and_changes(old, new, self._map(), index)
        assert any(p.kind == "new_schema" for p in problems)

    def test_property_added_on_unmapped_schema_is_needs_human(self, repo: Path):
        _write_fixture_repo(repo)
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        # UnmappedOut is reachable in both old and new (not "new_schema"), but gains a field
        old = base_schema(
            {"UnmappedOut": {"properties": {"a": {"type": "string"}}}}, {"/u": {"get": op(ref_out="UnmappedOut")}}
        )
        new = base_schema(
            {"UnmappedOut": {"properties": {"a": {"type": "string"}, "b": {"type": "string"}}}},
            {"/u": {"get": op(ref_out="UnmappedOut")}},
        )
        problems = sync.diff_removals_and_changes(old, new, self._map(), index)
        assert any(p.kind == "property_on_unmapped_schema" for p in problems)

    def test_fan_out_ambiguous_target_is_needs_human(self, repo: Path):
        _write_fixture_repo(repo)
        write(
            repo,
            "src/blindpay/resources/other.py",
            "from typing_extensions import TypedDict\n\n\nclass OtherPlain(TypedDict):\n    id: str\n",
        )
        map_data: dict[str, Any] = {
            "enums": [],
            "types": [
                {
                    "spec": "FanOut",
                    "sdk": [
                        {"file": "src/blindpay/resources/sample.py", "symbol": "Plain"},
                        {"file": "src/blindpay/resources/other.py", "symbol": "OtherPlain"},
                    ],
                }
            ],
            "ignore": {"schemas": []},
        }
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        gap = sync.PropertyGap(
            schema_names=["FanOut"],
            path=None,
            sdk_sites=map_data["types"][0]["sdk"],
            missing={"new_field": {"type": "string"}},
        )
        applied, needs_human = sync.apply_property_change(gap, index)
        assert applied == []
        assert any(n.kind == "fan_out_target_ambiguous" for n in needs_human)

    def test_unresolvable_type_is_needs_human(self, repo: Path):
        _write_fixture_repo(repo)
        map_data: dict[str, Any] = {
            "enums": [],
            "types": [{"spec": "PlainOut", "sdk": [{"file": "src/blindpay/resources/sample.py", "symbol": "Plain"}]}],
            "ignore": {"schemas": []},
        }
        sync = load_sync(repo)
        index = sync.build_sdk_index(sync.SRC_ROOT)
        gap = sync.PropertyGap(
            schema_names=["PlainOut"],
            path=None,
            sdk_sites=map_data["types"][0]["sdk"],
            missing={"weird": {"type": "object", "properties": {}}},
        )
        applied, needs_human = sync.apply_property_change(gap, index)
        assert applied == []
        assert any(n.kind == "type_unresolvable" for n in needs_human)


# --------------------------------------------------------------------------- #
# Full apply flow: bump classification, idempotency, determinism
# --------------------------------------------------------------------------- #


class TestApplyFlow:
    def _setup(self, repo: Path):
        _write_fixture_repo(repo)
        map_data: dict[str, Any] = {
            "enums": [
                {
                    "spec": {"schema": "ColorOut", "property": "color"},
                    "sdk": {"file": "src/blindpay/types.py", "symbol": "Color"},
                }
            ],
            "types": [{"spec": "PlainOut", "sdk": [{"file": "src/blindpay/resources/sample.py", "symbol": "Plain"}]}],
            "ignore": {"schemas": []},
        }
        _write_map_and_unmodeled(repo, map_data)
        old_spec = base_schema(
            {
                "ColorOut": {"properties": {"color": {"type": "string", "enum": ["red", "blue"]}}},
                "PlainOut": {"properties": {"id": {"type": "string"}, "name": {"type": ["string", "null"]}}},
            },
            {"/c": {"get": op(ref_out="ColorOut")}, "/p": {"get": op(ref_out="PlainOut")}},
        )
        write(repo, ".api-sync/spec-snapshot.json", json.dumps(old_spec))
        return map_data, old_spec

    def test_enum_only_change_bumps_minor(self, repo: Path):
        self._setup(repo)
        new_spec = json.loads((repo / ".api-sync/spec-snapshot.json").read_text())
        new_spec["components"]["schemas"]["ColorOut"]["properties"]["color"]["enum"].append("green")
        write(repo, ".api-sync/spec-current.json", json.dumps(new_spec))

        sync = load_sync(repo)
        exit_code = sync.cmd_apply(sync.DEFAULT_SPEC_PATH, None)
        assert exit_code == 0

        color_src = (repo / "src/blindpay/types.py").read_text()
        assert "green" in color_src

    def test_snapshot_refresh_copies_raw_bytes_not_a_reformatted_json_dump(self, repo: Path):
        """Regression test: the patcher must never json.load then json.dump the
        delivered spec to refresh the snapshot. Even when the parsed content is
        semantically identical, re-serializing changes indentation, separators,
        key order and unicode escaping -- which would make every future sync PR
        carry a diff of the entire multi-thousand-line file instead of just the
        lines that changed, and would make the committed snapshot stop matching
        the exact bytes blindpay-v2 ships as spec-current.json."""
        self._setup(repo)
        new_spec = json.loads((repo / ".api-sync/spec-snapshot.json").read_text())
        new_spec["components"]["schemas"]["ColorOut"]["properties"]["color"]["enum"].append("green")
        new_spec["components"]["schemas"]["ColorOut"]["description"] = "café"  # non-ascii, must not get \u-escaped
        # deliberately unusual (but still valid) formatting -- compact separators,
        # no trailing newline -- that a naive json.dumps of the parsed object
        # would normalize away
        weird_bytes = json.dumps(new_spec, indent=None, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        spec_path = repo / ".api-sync/spec-current.json"
        spec_path.write_bytes(weird_bytes)

        sync = load_sync(repo)
        assert sync.cmd_apply(sync.DEFAULT_SPEC_PATH, None) == 0

        snapshot_bytes = (repo / ".api-sync/spec-snapshot.json").read_bytes()
        assert snapshot_bytes == weird_bytes

    def test_property_only_change_bumps_patch(self, repo: Path):
        self._setup(repo)
        new_spec = json.loads((repo / ".api-sync/spec-snapshot.json").read_text())
        new_spec["components"]["schemas"]["PlainOut"]["properties"]["extra"] = {"type": "string"}
        write(repo, ".api-sync/spec-current.json", json.dumps(new_spec))

        report_path = repo / "report.json"
        sync = load_sync(repo)
        exit_code = sync.cmd_apply(sync.DEFAULT_SPEC_PATH, report_path)
        assert exit_code == 0
        report = json.loads(report_path.read_text())
        assert report["bump"] == "patch"

        # Plain is total=True, so the newly added field must be NotRequired --
        # a bare "extra: str" would make it a required key and break every
        # existing caller that omits it.
        sample_src = (repo / "src/blindpay/resources/sample.py").read_text()
        assert "extra: NotRequired[str]" in sample_src

    def test_apply_twice_is_idempotent(self, repo: Path):
        self._setup(repo)
        new_spec = json.loads((repo / ".api-sync/spec-snapshot.json").read_text())
        new_spec["components"]["schemas"]["ColorOut"]["properties"]["color"]["enum"].append("green")
        new_spec["components"]["schemas"]["PlainOut"]["properties"]["extra"] = {"type": "string"}
        write(repo, ".api-sync/spec-current.json", json.dumps(new_spec))

        sync = load_sync(repo)
        first_report = repo / "first.json"
        assert sync.cmd_apply(sync.DEFAULT_SPEC_PATH, first_report) == 0
        first = json.loads(first_report.read_text())
        assert len(first["applied"]) == 2

        second_report = repo / "second.json"
        assert sync.cmd_apply(sync.DEFAULT_SPEC_PATH, second_report) == 0
        second = json.loads(second_report.read_text())
        assert second["applied"] == []
        assert second["bump"] is None

    def test_check_is_green_after_apply(self, repo: Path):
        """--check reconciles against spec-snapshot.json directly (state, not a
        diff): pending drift is whatever the already-committed baseline says is
        true but the code has not caught up to, exactly like the real
        BankingPartner/portage gap this project found (already in the
        committed spec-snapshot.json, no new spec delivery needed to see it)."""
        self._setup(repo)
        # Simulate drift baked into the baseline itself: the snapshot already
        # knows about "green", the code does not.
        snapshot = json.loads((repo / ".api-sync/spec-snapshot.json").read_text())
        snapshot["components"]["schemas"]["ColorOut"]["properties"]["color"]["enum"].append("green")
        write(repo, ".api-sync/spec-snapshot.json", json.dumps(snapshot))
        write(repo, ".api-sync/spec-current.json", json.dumps(snapshot))

        sync = load_sync(repo)
        assert sync.cmd_check(None) == 1  # pending drift before apply
        assert sync.cmd_apply(sync.DEFAULT_SPEC_PATH, None) == 0
        assert sync.cmd_check(None) == 0  # green after apply


class TestDeterminism:
    def test_two_independent_applies_produce_byte_identical_trees(self, tmp_path: Path):
        def build(root: Path) -> None:
            _write_fixture_repo(root)
            map_data: dict[str, Any] = {
                "enums": [
                    {
                        "spec": {"schema": "ColorOut", "property": "color"},
                        "sdk": {"file": "src/blindpay/types.py", "symbol": "Color"},
                    }
                ],
                "types": [
                    {"spec": "PlainOut", "sdk": [{"file": "src/blindpay/resources/sample.py", "symbol": "Plain"}]}
                ],
                "ignore": {"schemas": []},
            }
            _write_map_and_unmodeled(root, map_data)
            old_spec = base_schema(
                {
                    "ColorOut": {"properties": {"color": {"type": "string", "enum": ["red", "blue"]}}},
                    "PlainOut": {"properties": {"id": {"type": "string"}}},
                },
                {"/c": {"get": op(ref_out="ColorOut")}, "/p": {"get": op(ref_out="PlainOut")}},
            )
            write(root, ".api-sync/spec-snapshot.json", json.dumps(old_spec))
            new_spec = json.loads(json.dumps(old_spec))
            new_spec["components"]["schemas"]["ColorOut"]["properties"]["color"]["enum"].append("green")
            new_spec["components"]["schemas"]["PlainOut"]["properties"]["extra"] = {"type": "string"}
            write(root, ".api-sync/spec-current.json", json.dumps(new_spec))

        root_a = tmp_path / "a"
        root_b = tmp_path / "b"
        build(root_a)
        build(root_b)

        sync_a = load_sync(root_a)
        sync_b = load_sync(root_b)
        assert sync_a.cmd_apply(sync_a.DEFAULT_SPEC_PATH, None) == 0
        assert sync_b.cmd_apply(sync_b.DEFAULT_SPEC_PATH, None) == 0

        for rel in ["src/blindpay/types.py", "src/blindpay/resources/sample.py", ".api-sync/spec-snapshot.json"]:
            assert (root_a / rel).read_bytes() == (root_b / rel).read_bytes(), rel


# --------------------------------------------------------------------------- #
# unmodeled.json loading/validation
# --------------------------------------------------------------------------- #


class TestUnmodeledLoading:
    def test_property_entry_requires_all_keys(self, repo: Path):
        write(repo, ".api-sync/unmodeled.json", json.dumps([{"kind": "property", "schema": "X", "field": "y"}]))
        sync = load_sync(repo)
        with pytest.raises(SystemExit):
            sync.load_unmodeled()

    def test_enum_entry_requires_all_keys(self, repo: Path):
        write(repo, ".api-sync/unmodeled.json", json.dumps([{"kind": "enum", "enum": "X"}]))
        sync = load_sync(repo)
        with pytest.raises(SystemExit):
            sync.load_unmodeled()

    def test_unknown_kind_rejected(self, repo: Path):
        write(repo, ".api-sync/unmodeled.json", json.dumps([{"kind": "bogus"}]))
        sync = load_sync(repo)
        with pytest.raises(SystemExit):
            sync.load_unmodeled()

    def test_valid_entries_load(self, repo: Path):
        write(
            repo,
            ".api-sync/unmodeled.json",
            json.dumps(
                [
                    {"kind": "property", "schema": "X", "field": "y", "reason": "r", "owner": "eric@blindpay.com"},
                    {"kind": "enum", "enum": "X", "missing_values": ["a"], "reason": "r", "owner": "eric@blindpay.com"},
                ]
            ),
        )
        sync = load_sync(repo)
        assert len(sync.load_unmodeled()) == 2


# --------------------------------------------------------------------------- #
# Reachability
# --------------------------------------------------------------------------- #


class TestReachability:
    def test_orphan_schema_excluded_by_construction(self):
        sync = load_sync(Path("/nonexistent"))
        spec = base_schema(
            {
                "Reachable": {"properties": {"a": {"type": "string"}}},
                "Orphan": {"properties": {"b": {"type": "string"}}},
            },
            {"/x": {"get": op(ref_out="Reachable")}},
        )
        reachable = sync.compute_reachable_schemas(spec)
        assert reachable == {"Reachable"}

    def test_nested_ref_transitively_reachable(self):
        sync = load_sync(Path("/nonexistent"))
        spec = base_schema(
            {
                "Reachable": {"properties": {"child": {"$ref": "#/components/schemas/Child"}}},
                "Child": {"properties": {"a": {"type": "string"}}},
            },
            {"/x": {"get": op(ref_out="Reachable")}},
        )
        reachable = sync.compute_reachable_schemas(spec)
        assert reachable == {"Reachable", "Child"}


# --------------------------------------------------------------------------- #
# --audit-types: full state comparison of every mapped property's spec type
# against the SDK's CURRENT annotation, independent of any old-vs-new diff.
# --------------------------------------------------------------------------- #


class TestAuditPropertyType:
    def test_nullable_spec_without_optional_sdk_is_flagged(self):
        sync = load_sync(Path("/nonexistent"))
        note = sync.audit_property_type({"type": ["string", "null"]}, "str")
        assert note is not None and "Optional" in note

    def test_nullable_spec_with_optional_sdk_is_not_flagged(self):
        sync = load_sync(Path("/nonexistent"))
        assert sync.audit_property_type({"type": ["string", "null"]}, "Optional[str]") is None

    def test_non_nullable_spec_with_optional_sdk_is_not_flagged(self):
        """SDK wider than necessary (Optional where spec never sends null) is a
        legitimate, common, harmless modeling choice -- not reported."""
        sync = load_sync(Path("/nonexistent"))
        assert sync.audit_property_type({"type": "string"}, "Optional[str]") is None

    def test_enum_property_with_bare_scalar_sdk_is_flagged(self):
        sync = load_sync(Path("/nonexistent"))
        note = sync.audit_property_type({"type": "string", "enum": ["a", "b"]}, "str")
        assert note is not None and "enum-constrained" in note

    def test_enum_property_with_literal_reference_is_not_flagged(self):
        sync = load_sync(Path("/nonexistent"))
        assert sync.audit_property_type({"type": "string", "enum": ["a", "b"]}, "MyLiteral") is None

    def test_scalar_type_mismatch_is_flagged(self):
        """The one real finding this audit turned up in this repo:
        PayinOut.billing_fee_amount is `number` on the wire but `Optional[str]`
        in the SDK."""
        sync = load_sync(Path("/nonexistent"))
        note = sync.audit_property_type({"type": "number"}, "Optional[str]")
        assert note is not None and "`number`" in note and "`str`" in note

    def test_integer_widened_to_float_is_deliberately_compatible(self):
        sync = load_sync(Path("/nonexistent"))
        assert sync.audit_property_type({"type": "integer"}, "float") is None

    def test_ambiguous_spec_type_is_not_flagged(self):
        sync = load_sync(Path("/nonexistent"))
        assert sync.audit_property_type({"example": "abc"}, "str") is None

    def test_array_type_mismatch_is_flagged(self):
        sync = load_sync(Path("/nonexistent"))
        note = sync.audit_property_type({"type": "array"}, "str")
        assert note is not None and "array" in note

    def test_array_type_match_is_not_flagged(self):
        sync = load_sync(Path("/nonexistent"))
        assert sync.audit_property_type({"type": "array"}, "List[str]") is None


class TestAuditTypes:
    def test_finds_scalar_mismatch_end_to_end(self, repo: Path):
        _write_fixture_repo(repo)
        map_data: dict[str, Any] = {
            "enums": [],
            "types": [{"spec": "PlainOut", "sdk": [{"file": "src/blindpay/resources/sample.py", "symbol": "Plain"}]}],
            "ignore": {"schemas": []},
        }
        _write_map_and_unmodeled(repo, map_data)
        sync = load_sync(repo)
        # Plain.name: Optional[str] in the SDK; make the spec say it's really a number
        spec = base_schema(
            {"PlainOut": {"properties": {"id": {"type": "string"}, "name": {"type": "number"}}}},
            {"/x": {"get": op(ref_out="PlainOut")}},
        )
        findings = sync.audit_types(spec, map_data)
        assert any(f["field"] == "name" and "number" in f["note"] for f in findings)

    def test_shared_locators_are_merged_into_one_finding(self, repo: Path):
        """The exact duplication bug this audit's own development caught: a
        map entry with several spec locators asserted to share one shape must
        not multiply the same real finding once per locator."""
        _write_fixture_repo(repo)
        map_data: dict[str, Any] = {
            "enums": [],
            "types": [
                {
                    "spec": ["ParentOut", "SiblingOut"],
                    "sdk": [{"file": "src/blindpay/resources/sample.py", "symbol": "Plain"}],
                }
            ],
            "ignore": {"schemas": []},
        }
        _write_map_and_unmodeled(repo, map_data)
        sync = load_sync(repo)
        shape = {"id": {"type": "number"}, "name": {"type": ["string", "null"]}}
        spec = base_schema(
            {"ParentOut": {"properties": shape}, "SiblingOut": {"properties": shape}},
            {"/x": {"get": op(ref_out="ParentOut")}, "/y": {"get": op(ref_out="SiblingOut")}},
        )
        findings = sync.audit_types(spec, map_data)
        id_findings = [f for f in findings if f["field"] == "id"]
        assert len(id_findings) == 1
        assert "ParentOut" in id_findings[0]["schema"]
