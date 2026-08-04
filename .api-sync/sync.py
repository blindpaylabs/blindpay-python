#!/usr/bin/env python3
"""Deterministic spec -> SDK patcher.

Run locally with:
    python3 .api-sync/sync.py --check
    python3 .api-sync/sync.py --apply [--spec PATH] [--report PATH]
    python3 .api-sync/sync.py --validate-map
    python3 .api-sync/sync.py --coverage [--spec PATH]
    python3 .api-sync/sync.py --audit-types [--spec PATH]

No third-party dependencies. Mirrors check_contract.py's style: ast for reading,
precise text splicing for writing.

Design summary (see .api-sync/spec-map.json and .api-sync/unmodeled.json):

- .api-sync/spec-map.json is the curated, hand-verified mapping from spec
  constructs (enums, schemas, and named nested sub-objects via `specPath`) to
  SDK symbols. Schemas outside the transitive $ref closure of paths/webhooks
  are unreachable and are skipped by construction (never considered "unmapped"
  or "coverage gaps" -- they simply do not exist for this tool's purposes).
- .api-sync/unmodeled.json is the honest ledger of currently-absent spec
  properties and enum-member/value divergences on schemas/enums this SDK DOES
  map, each with a reason and an owner. Entries there suppress both --check
  failures and --apply auto-additions for that exact (schema[, path], field)
  or (enum, missing value) -- they are a deliberate "not yet, and here is why"
  record, not a silent skip.

--check reconciles the current SDK source against .api-sync/spec-snapshot.json
(the last-synced baseline) and fails loudly on anything unaccounted for. It
never reads --spec.

--apply reconciles against --spec (default .api-sync/spec-current.json, the
newly delivered spec), computes an old(snapshot)-vs-new(--spec) diff purely to
detect removals / required-ness changes / type changes / new operations / new
schemas (state alone cannot tell you these), applies whatever is APPLICABLE,
hard-fails on anything NEEDS_HUMAN, and on success refreshes spec-snapshot.json
to equal --spec.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Union

ROOT = Path(__file__).resolve().parent.parent
API_SYNC = Path(__file__).resolve().parent
SRC_ROOT = ROOT / "src" / "blindpay"

SNAPSHOT_PATH = API_SYNC / "spec-snapshot.json"
DEFAULT_SPEC_PATH = API_SYNC / "spec-current.json"
MAP_PATH = API_SYNC / "spec-map.json"
UNMODELED_PATH = API_SYNC / "unmodeled.json"

SCALAR_TYPE_MAP = {"string": "str", "integer": "int", "number": "float", "boolean": "bool"}
HTTP_VERBS = ("get", "post", "put", "patch", "delete")


# --------------------------------------------------------------------------- #
# JSON loading
# --------------------------------------------------------------------------- #


def load_json(path: Path) -> Any:
    with path.open() as f:
        return json.load(f)


def load_map() -> dict:
    return load_json(MAP_PATH)


def load_unmodeled() -> list[dict]:
    if not UNMODELED_PATH.exists():
        return []
    data = load_json(UNMODELED_PATH)
    if not isinstance(data, list):
        raise SystemExit(f"{UNMODELED_PATH}: expected a JSON array")
    for i, e in enumerate(data):
        kind = e.get("kind")
        if kind == "property":
            required = {"schema", "field", "reason", "owner"}
        elif kind == "enum":
            required = {"enum", "missing_values", "reason", "owner"}
        elif kind == "enum_coverage":
            required = {"schema", "property", "reason", "owner"}
        elif kind == "nested_object":
            required = {"schema", "path", "reason", "owner"}
        elif kind == "operation":
            required = {"method", "path", "reason", "owner"}
        else:
            raise SystemExit(
                f"{UNMODELED_PATH}[{i}]: unknown or missing 'kind' "
                f"(expected 'property', 'enum', 'enum_coverage', 'nested_object', or 'operation')"
            )
        missing = required - e.keys()
        if missing:
            raise SystemExit(f"{UNMODELED_PATH}[{i}]: missing required key(s) {sorted(missing)}")
    return data


# --------------------------------------------------------------------------- #
# Spec introspection
# --------------------------------------------------------------------------- #


def find_refs(node: object, out: set[str]) -> None:
    if isinstance(node, dict):
        r = node.get("$ref")
        if isinstance(r, str) and r.startswith("#/components/schemas/"):
            out.add(r.split("/")[-1])
        for v in node.values():
            find_refs(v, out)
    elif isinstance(node, list):
        for v in node:
            find_refs(v, out)


def compute_reachable_schemas(spec: dict) -> set[str]:
    """Transitive $ref closure from paths + webhooks. Anything outside this
    set does not exist for this tool: not mappable, not a coverage gap, not
    reconciled -- skipped by construction, never by a hand-maintained list."""
    schemas = spec.get("components", {}).get("schemas", {})
    roots = {"paths": spec.get("paths", {}), "webhooks": spec.get("webhooks", {})}
    reachable: set[str] = set()
    find_refs(roots, reachable)
    changed = True
    while changed:
        changed = False
        for name in list(reachable):
            s = schemas.get(name)
            if s is None:
                continue
            found: set[str] = set()
            find_refs(s, found)
            for n in found:
                if n not in reachable:
                    reachable.add(n)
                    changed = True
    return reachable


def get_schema(spec: dict, name: str) -> Optional[dict]:
    return spec.get("components", {}).get("schemas", {}).get(name)


def resolve_path(schema_obj: dict, path: Optional[str]) -> Optional[dict]:
    node = schema_obj
    if not path:
        return node
    for part in path.split("."):
        props = node.get("properties", {}) if isinstance(node, dict) else {}
        node = props.get(part)
        if node is None:
            return None
    return node


def get_properties(node: Optional[dict]) -> dict[str, dict]:
    if not node:
        return {}
    return node.get("properties", {})


def get_required(node: Optional[dict]) -> set[str]:
    if not node:
        return set()
    return set(node.get("required", []))


def get_enum_values(spec: dict, locator: dict) -> Optional[set[str]]:
    schema_obj = get_schema(spec, locator["schema"])
    if schema_obj is None:
        return None
    prop = resolve_path(schema_obj, None)
    prop = get_properties(prop).get(locator["property"])
    if prop is None:
        return None
    if locator.get("items"):
        prop = prop.get("items", {})
    enum = prop.get("enum")
    if enum is None:
        return None
    return set(enum)


def find_enum_locator(prop_schema: dict) -> Optional[tuple[bool, list]]:
    """Detects an enum constraint in any of the shapes the public spec uses:
    a bare `enum`, an array's `items.enum`, or either wrapped in `anyOf`/`oneOf`
    (the usual nullable-enum pattern). Returns (is_items_form, enum_values) or
    None if the property carries no enum constraint at all."""
    if not isinstance(prop_schema, dict):
        return None
    if "enum" in prop_schema:
        return False, prop_schema["enum"]
    items = prop_schema.get("items")
    if isinstance(items, dict) and "enum" in items:
        return True, items["enum"]
    for key in ("anyOf", "oneOf"):
        variants = prop_schema.get(key)
        if not isinstance(variants, list):
            continue
        for variant in variants:
            if not isinstance(variant, dict):
                continue
            if "enum" in variant:
                return False, variant["enum"]
            v_items = variant.get("items")
            if isinstance(v_items, dict) and "enum" in v_items:
                return True, v_items["enum"]
    return None


def inline_object_shapes(prop_schema: dict) -> list[tuple[str, dict]]:
    """Returns (path_suffix, shape) for every inline (non-$ref) object shape
    implied directly by this property: the property itself if it is an inline
    object, and/or its array items if those are an inline object. A $ref'd
    object is a named schema and out of scope here -- it is reachable (or not)
    and mappable (or ignored) on its own terms via the normal schema machinery."""
    shapes: list[tuple[str, dict]] = []
    if not isinstance(prop_schema, dict):
        return shapes
    if prop_schema.get("type") == "object" and "$ref" not in prop_schema and "properties" in prop_schema:
        shapes.append(("", prop_schema))
    items = prop_schema.get("items")
    if isinstance(items, dict) and "$ref" not in items and items.get("type") == "object" and "properties" in items:
        shapes.append((".items", items))
    return shapes


def coarse_type(prop_schema: dict) -> tuple[Optional[str], bool]:
    """Returns (single non-null JSON type or None if ambiguous/multi-type, nullable)."""
    t = prop_schema.get("type")
    if isinstance(t, list):
        types = [x for x in t if x != "null"]
        nullable = "null" in t
    elif isinstance(t, str):
        types = [t]
        nullable = False
    else:
        types = []
        nullable = False
    if len(types) != 1:
        return None, nullable
    return types[0], nullable


# --------------------------------------------------------------------------- #
# SDK (Python source) introspection via ast
# --------------------------------------------------------------------------- #


@dataclass
class ClassInfo:
    file: Path
    node: ast.ClassDef
    source: str
    bases: list[str] = field(default_factory=list)
    total_false: bool = False
    own_fields: dict[str, ast.AnnAssign] = field(default_factory=dict)


@dataclass
class SdkIndex:
    # every symbol name may legitimately have more than one definition across files
    # (e.g. OfframpWallet is intentionally duplicated, PaymentMethod is shadowed
    # locally in payins/quotes.py) -- always disambiguate by file, never by
    # "first one found".
    all_classes: dict[str, list[ClassInfo]]
    all_literals: dict[str, list[tuple[Path, ast.Assign, str]]]
    sources: dict[Path, str]

    def find_class(self, symbol: str, file_rel: str) -> Optional[ClassInfo]:
        for info in self.all_classes.get(symbol, []):
            if str(info.file.relative_to(ROOT)) == file_rel:
                return info
        return None

    def find_literal(self, symbol: str, file_rel: str) -> Optional[tuple[Path, ast.Assign, str]]:
        for entry in self.all_literals.get(symbol, []):
            if str(entry[0].relative_to(ROOT)) == file_rel:
                return entry
        return None


def _base_names(node: ast.ClassDef) -> list[str]:
    names = [b.id for b in node.bases if isinstance(b, ast.Name)]
    names += [b.attr for b in node.bases if isinstance(b, ast.Attribute)]
    return names


def _is_total_false(node: ast.ClassDef) -> bool:
    for kw in node.keywords:
        if kw.arg == "total" and isinstance(kw.value, ast.Constant) and kw.value.value is False:
            return True
    return False


def build_sdk_index(src_root: Path = SRC_ROOT) -> SdkIndex:
    py_files = sorted(src_root.rglob("*.py"))
    trees: dict[Path, ast.Module] = {}
    sources: dict[Path, str] = {}
    for f in py_files:
        text = f.read_text()
        sources[f] = text
        trees[f] = ast.parse(text, filename=str(f))

    known_typeddict = {"TypedDict"}
    for _ in range(5):
        changed = False
        for tree in trees.values():
            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef) or node.name in known_typeddict:
                    continue
                if any(b in known_typeddict for b in _base_names(node)):
                    known_typeddict.add(node.name)
                    changed = True
        if not changed:
            break

    all_classes: dict[str, list[ClassInfo]] = {}
    for f, tree in trees.items():
        for node in ast.walk(tree):
            if not (isinstance(node, ast.ClassDef) and node.name in known_typeddict):
                continue
            own_fields = {}
            for item in node.body:
                if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                    own_fields[item.target.id] = item
            info = ClassInfo(
                file=f,
                node=node,
                source=sources[f],
                bases=_base_names(node),
                total_false=_is_total_false(node),
                own_fields=own_fields,
            )
            all_classes.setdefault(node.name, []).append(info)

    all_literals: dict[str, list[tuple[Path, ast.Assign, str]]] = {}
    for f, tree in trees.items():
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
                continue
            if not isinstance(node.value, ast.Subscript):
                continue
            base = node.value.value
            base_name = (
                base.id if isinstance(base, ast.Name) else (base.attr if isinstance(base, ast.Attribute) else None)
            )
            if base_name != "Literal":
                continue
            name = node.targets[0].id
            all_literals.setdefault(name, []).append((f, node, sources[f]))

    return SdkIndex(all_classes=all_classes, all_literals=all_literals, sources=sources)


def _pick_unambiguous(file_rel: Optional[str], candidates: list) -> Optional[Any]:
    if file_rel is not None:
        for c in candidates:
            if str(c[0].relative_to(ROOT) if isinstance(c, tuple) else c.file.relative_to(ROOT)) == file_rel:
                return c
        return None
    return candidates[0] if len(candidates) == 1 else None


def resolve_typeddict_fields(
    symbol: str, file_rel: Optional[str], index: SdkIndex, seen: Optional[set[str]] = None
) -> set[str]:
    """Full field set, transitively resolving locally-defined TypedDict base classes
    (the `_XRequired` / total=False two-part pattern). `file_rel` disambiguates
    symbols legitimately defined in more than one file (e.g. OfframpWallet)."""
    seen = seen or set()
    key = f"{file_rel}::{symbol}"
    if key in seen:
        return set()
    seen.add(key)
    info = _pick_unambiguous(file_rel, index.all_classes.get(symbol, []))
    if info is None:
        return set()
    fields = set(info.own_fields.keys())
    for base in info.bases:
        # base classes are always local to the same file
        fields |= resolve_typeddict_fields(base, str(info.file.relative_to(ROOT)), index, seen)
    return fields


def literal_values(symbol: str, file_rel: str, index: SdkIndex) -> set[str]:
    entry = index.find_literal(symbol, file_rel)
    if entry is None:
        return set()
    _, node, _ = entry
    values: set[str] = set()
    for const in ast.walk(node.value):
        if isinstance(const, ast.Constant) and isinstance(const.value, str):
            values.add(const.value)
    return values


# --------------------------------------------------------------------------- #
# Map validity
# --------------------------------------------------------------------------- #


def validate_map(map_data: dict, index: SdkIndex) -> list[str]:
    errors: list[str] = []

    def check_sdk_site(site: dict, ctx: str) -> None:
        rel = site["file"]
        symbol = site["symbol"]
        f = ROOT / rel
        if not f.exists():
            errors.append(f"{ctx}: file not found: {rel}")
            return
        class_candidates = index.all_classes.get(symbol, [])
        literal_candidates = index.all_literals.get(symbol, [])
        if not class_candidates and not literal_candidates:
            errors.append(f"{ctx}: symbol `{symbol}` not found anywhere under src/blindpay")
            return
        if index.find_class(symbol, rel) is None and index.find_literal(symbol, rel) is None:
            found_in = sorted(
                {str(c.file.relative_to(ROOT)) for c in class_candidates}
                | {str(c[0].relative_to(ROOT)) for c in literal_candidates}
            )
            errors.append(f"{ctx}: symbol `{symbol}` not found in {rel} (found in {found_in})")

    for i, e in enumerate(map_data.get("enums", [])):
        ctx = f"enums[{i}] ({e['spec']['schema']}.{e['spec']['property']})"
        check_sdk_site(e["sdk"], ctx)

    for i, e in enumerate(map_data.get("types", [])):
        spec = e["spec"]
        names = spec if isinstance(spec, list) else [spec]
        ctx_base = "/".join(names) + (f"#{e['specPath']}" if e.get("specPath") else "")
        for j, site in enumerate(e["sdk"]):
            check_sdk_site(site, f"types[{i}] ({ctx_base})[{j}]")

    return errors


# --------------------------------------------------------------------------- #
# Reconciliation (state-based, against a single spec)
# --------------------------------------------------------------------------- #


@dataclass
class EnumGap:
    symbol: str
    file: str
    locators: list[dict]
    missing: list[str]  # unaccounted (not in unmodeled.json)


@dataclass
class PropertyGap:
    schema_names: list[str]
    path: Optional[str]
    sdk_sites: list[dict]
    missing: dict[str, dict]  # field name -> its spec property schema


def unmodeled_enum_allowed(unmodeled: list[dict], enum_symbol: str) -> set[str]:
    allowed: set[str] = set()
    for e in unmodeled:
        if e["kind"] == "enum" and e["enum"] == enum_symbol:
            allowed.update(e["missing_values"])
    return allowed


def unmodeled_property_allowed(unmodeled: list[dict], schema_names: list[str], path: Optional[str]) -> set[str]:
    allowed: set[str] = set()
    for e in unmodeled:
        if e["kind"] != "property":
            continue
        if e["schema"] not in schema_names:
            continue
        if e.get("path") != path:
            continue
        allowed.add(e["field"])
    return allowed


def reconcile_enums(spec: dict, map_data: dict, unmodeled: list[dict], index: SdkIndex) -> list[EnumGap]:
    gaps: list[EnumGap] = []
    # group by (file, symbol): the same symbol name can legitimately denote two
    # different Literals in two different files (e.g. PaymentMethod), and must
    # never be merged.
    by_site: dict[tuple[str, str], list[dict]] = {}
    for e in map_data.get("enums", []):
        key = (e["sdk"]["file"], e["sdk"]["symbol"])
        by_site.setdefault(key, []).append(e)

    for (file_rel, symbol), entries in sorted(by_site.items()):
        spec_members: set[str] = set()
        for e in entries:
            vals = get_enum_values(spec, e["spec"])
            if vals:
                spec_members |= vals
        sdk_members = literal_values(symbol, file_rel, index)
        missing = spec_members - sdk_members
        allowed = unmodeled_enum_allowed(unmodeled, symbol)
        unaccounted = sorted(missing - allowed)
        if unaccounted:
            gaps.append(
                EnumGap(symbol=symbol, file=file_rel, locators=[e["spec"] for e in entries], missing=unaccounted)
            )
    return gaps


def reconcile_types(spec: dict, map_data: dict, unmodeled: list[dict], index: SdkIndex) -> list[PropertyGap]:
    gaps: list[PropertyGap] = []
    reachable = compute_reachable_schemas(spec)

    for e in map_data.get("types", []):
        spec_names = e["spec"] if isinstance(e["spec"], list) else [e["spec"]]
        path = e.get("specPath")
        spec_props: dict[str, dict] = {}
        any_reachable = False
        for name in spec_names:
            schema_obj = get_schema(spec, name)
            if schema_obj is None:
                continue
            if name not in reachable:
                continue
            any_reachable = True
            node = resolve_path(schema_obj, path)
            spec_props.update(get_properties(node))
        if not any_reachable:
            continue

        sdk_fields: set[str] = set()
        for site in e["sdk"]:
            sdk_fields |= resolve_typeddict_fields(site["symbol"], site["file"], index)

        missing_names = set(spec_props.keys()) - sdk_fields
        allowed = unmodeled_property_allowed(unmodeled, spec_names, path)
        unaccounted = sorted(missing_names - allowed)
        if unaccounted:
            gaps.append(
                PropertyGap(
                    schema_names=spec_names,
                    path=path,
                    sdk_sites=e["sdk"],
                    missing={n: spec_props[n] for n in unaccounted},
                )
            )
    return gaps


def unmodeled_enum_coverage_allowed(unmodeled: list[dict], schema: str, path: Optional[str], prop: str) -> bool:
    return any(
        e.get("kind") == "enum_coverage" and e["schema"] == schema and e.get("path") == path and e["property"] == prop
        for e in unmodeled
    )


def unmodeled_nested_object_allowed(unmodeled: list[dict], schema: str, path: str) -> bool:
    return any(e.get("kind") == "nested_object" and e["schema"] == schema and e["path"] == path for e in unmodeled)


@dataclass
class EnumCoverageGap:
    schema: str
    path: Optional[str]
    property: str


def reconcile_enum_coverage(
    spec: dict, map_data: dict, unmodeled: list[dict], index: SdkIndex
) -> list[EnumCoverageGap]:
    """Every enum-constrained property on a schema this SDK actually models
    the field for must resolve to a mapped Literal (via spec-map.json's
    `enums` list) or a recorded (kind=enum_coverage) exclusion. Unlike
    reconcile_enums, which only checks the *members* of enums someone already
    chose to map, this walks every mapped schema and flags enum-constrained
    properties nobody mapped at all."""
    reachable = compute_reachable_schemas(spec)
    covered = {
        (e["spec"]["schema"], e["spec"].get("path"), e["spec"]["property"], bool(e["spec"].get("items")))
        for e in map_data.get("enums", [])
    }

    gaps: list[EnumCoverageGap] = []
    seen: set[tuple[str, Optional[str], str]] = set()
    for e in map_data.get("types", []):
        spec_names = e["spec"] if isinstance(e["spec"], list) else [e["spec"]]
        path = e.get("specPath")
        sdk_fields: set[str] = set()
        for site in e["sdk"]:
            sdk_fields |= resolve_typeddict_fields(site["symbol"], site["file"], index)

        for name in spec_names:
            if name not in reachable:
                continue
            schema_obj = get_schema(spec, name)
            if schema_obj is None:
                continue
            node = resolve_path(schema_obj, path)
            for prop_name, prop_schema in get_properties(node).items():
                if prop_name not in sdk_fields:
                    continue  # unmapped field entirely -- reconcile_types's concern, not this check's
                locator = find_enum_locator(prop_schema)
                if locator is None:
                    continue
                is_items, _values = locator
                key = (name, path, prop_name)
                if key in seen:
                    continue
                if (name, path, prop_name, is_items) in covered:
                    continue
                if unmodeled_enum_coverage_allowed(unmodeled, name, path, prop_name):
                    continue
                seen.add(key)
                gaps.append(EnumCoverageGap(schema=name, path=path, property=prop_name))

    gaps.sort(key=lambda g: (g.schema, g.path or "", g.property))
    return gaps


@dataclass
class NestedObjectGap:
    schema: str
    path: str


def reconcile_nested_coverage(spec: dict, map_data: dict, unmodeled: list[dict]) -> list[NestedObjectGap]:
    """Recursively enumerates inline object and array-item-object shapes
    reachable under every mapped schema's mapped path. Each such shape must
    itself have a map entry (specPath pointing at it) or a recorded
    (kind=nested_object) omission -- otherwise its own properties (which may
    include further enums, or fields drifting out from under it) are
    invisible to every other check in this file."""
    reachable = compute_reachable_schemas(spec)
    mapped_paths: set[tuple[str, Optional[str]]] = set()
    for e in map_data.get("types", []):
        spec_names = e["spec"] if isinstance(e["spec"], list) else [e["spec"]]
        path = e.get("specPath")
        for name in spec_names:
            mapped_paths.add((name, path))

    gaps: list[NestedObjectGap] = []
    seen: set[tuple[str, str]] = set()

    def walk(schema_name: str, base_path: Optional[str], node: Optional[dict]) -> None:
        for prop_name, prop_schema in get_properties(node).items():
            child_path = f"{base_path}.{prop_name}" if base_path else prop_name
            for suffix, shape in inline_object_shapes(prop_schema):
                full_path = child_path + suffix
                key = (schema_name, full_path)
                if key in seen:
                    continue
                if (schema_name, full_path) in mapped_paths:
                    walk(schema_name, full_path, shape)
                    continue
                if unmodeled_nested_object_allowed(unmodeled, schema_name, full_path):
                    continue
                seen.add(key)
                gaps.append(NestedObjectGap(schema=schema_name, path=full_path))
                # do not recurse into an unresolved shape -- its own nested
                # shapes are not in scope until this one is mapped or excused

    for name, path in sorted(mapped_paths, key=lambda t: (t[0], t[1] or "")):
        if name not in reachable:
            continue
        schema_obj = get_schema(spec, name)
        if schema_obj is None:
            continue
        node = resolve_path(schema_obj, path)
        walk(name, path, node)

    gaps.sort(key=lambda g: (g.schema, g.path))
    return gaps


# --------------------------------------------------------------------------- #
# Old-vs-new diff (apply-only): removals, required/type changes, new operations/schemas
# --------------------------------------------------------------------------- #


@dataclass
class NeedsHuman:
    kind: str
    detail: str


def diff_removals_and_changes(old_spec: dict, new_spec: dict, map_data: dict, index: SdkIndex) -> list[NeedsHuman]:
    problems: list[NeedsHuman] = []

    # enums: sdk-modeled member disappearing from the new spec
    by_site: dict[tuple[str, str], list[dict]] = {}
    for e in map_data.get("enums", []):
        by_site.setdefault((e["sdk"]["file"], e["sdk"]["symbol"]), []).append(e)
    for (file_rel, symbol), entries in sorted(by_site.items()):
        sdk_members = literal_values(symbol, file_rel, index)
        new_members: set[str] = set()
        for e in entries:
            vals = get_enum_values(new_spec, e["spec"])
            if vals:
                new_members |= vals
        old_members: set[str] = set()
        for e in entries:
            vals = get_enum_values(old_spec, e["spec"])
            if vals:
                old_members |= vals
        removed = (sdk_members & old_members) - new_members
        if removed:
            problems.append(NeedsHuman("enum_member_removed", f"{symbol}: {sorted(removed)} no longer in the spec"))

    old_reachable = compute_reachable_schemas(old_spec)
    new_reachable = compute_reachable_schemas(new_spec)

    for e in map_data.get("types", []):
        spec_names = e["spec"] if isinstance(e["spec"], list) else [e["spec"]]
        path = e.get("specPath")
        sdk_fields: set[str] = set()
        for site in e["sdk"]:
            sdk_fields |= resolve_typeddict_fields(site["symbol"], site["file"], index)

        for name in spec_names:
            if name in old_reachable and name not in new_reachable:
                problems.append(NeedsHuman("schema_removed", f"{name} no longer reachable in the new spec"))
                continue
            old_obj = get_schema(old_spec, name)
            new_obj = get_schema(new_spec, name)
            if old_obj is None or new_obj is None:
                continue
            old_node = resolve_path(old_obj, path)
            new_node = resolve_path(new_obj, path)
            old_props = get_properties(old_node)
            new_props = get_properties(new_node)
            old_required = get_required(old_node)
            new_required = get_required(new_node)

            removed_fields = (sdk_fields & set(old_props.keys())) - set(new_props.keys())
            for f in sorted(removed_fields):
                problems.append(
                    NeedsHuman(
                        "property_removed",
                        f"{name}{'/' + path if path else ''}.{f} modeled by the SDK, no longer in the spec",
                    )
                )

            for f in sorted(sdk_fields & set(old_props.keys()) & set(new_props.keys())):
                was_required = f in old_required
                is_required = f in new_required
                if was_required != is_required:
                    problems.append(
                        NeedsHuman(
                            "required_change",
                            f"{name}{'/' + path if path else ''}.{f} required-ness changed "
                            f"({was_required} -> {is_required})",
                        )
                    )
                    continue
                old_type, old_nullable = coarse_type(old_props[f])
                new_type, new_nullable = coarse_type(new_props[f])
                # Ambiguous on either side (multi-type, or no "type" key at all --
                # e.g. a property that only ever had "example"/"description") is
                # deliberately treated as compatible, not needs-human: this is the
                # real, observed, benign shape of this spec's own evolution
                # (created_at/updated_at gaining an explicit
                # {"type": ["string","null"], "format": "date-time"} where they
                # previously had no "type" key at all). There is nothing to
                # meaningfully compare when one side never declared a concrete type.
                if old_type is not None and new_type is not None:
                    if old_type != new_type:
                        problems.append(
                            NeedsHuman(
                                "type_change",
                                f"{name}{'/' + path if path else ''}.{f} type changed ({old_type} -> {new_type})",
                            )
                        )
                    elif old_nullable != new_nullable:
                        problems.append(
                            NeedsHuman(
                                "type_change",
                                f"{name}{'/' + path if path else ''}.{f} nullability changed "
                                f"(nullable={old_nullable} -> nullable={new_nullable})",
                            )
                        )

    # New/uncovered operations are handled by reconcile_operations (state-based:
    # it checks whether the CURRENT spec's operations have a matching SDK call
    # site, not whether the path key is new relative to the old snapshot -- an
    # operation can be "new" to the SDK without its path being new to the spec,
    # e.g. right after a human deletes a method by hand).

    # new reachable schemas not present before
    mapped_or_ignored: set[str] = set()
    for e in map_data.get("types", []):
        spec_names = e["spec"] if isinstance(e["spec"], list) else [e["spec"]]
        mapped_or_ignored.update(spec_names)
    mapped_or_ignored.update(x["schema"] for x in map_data.get("ignore", {}).get("schemas", []))
    for name in sorted(new_reachable - old_reachable):
        if name not in mapped_or_ignored:
            problems.append(NeedsHuman("new_schema", f"new reachable schema: {name}"))

    # properties added on an entirely unmapped (and not ignored) reachable schema
    schemas = new_spec.get("components", {}).get("schemas", {})
    for name in sorted(new_reachable):
        if name in mapped_or_ignored:
            continue
        old_obj = get_schema(old_spec, name)
        new_obj = schemas.get(name)
        old_props = set(get_properties(old_obj).keys()) if old_obj else set()
        new_props = set(get_properties(new_obj).keys())
        added = new_props - old_props
        if added:
            problems.append(
                NeedsHuman("property_on_unmapped_schema", f"{name}: {sorted(added)} (schema has no spec-map entry)")
            )

    return problems


# --------------------------------------------------------------------------- #
# Operation coverage (state-based): does every spec operation have a matching
# SDK call site? Coverage is derived, never hand-maintained: an operation is
# "covered" iff some resource module already issues that exact (HTTP verb,
# path template) request. Uncovered operations are then classified as either
# STANDARD (deterministically generatable: plain JSON in/out, maps cleanly to
# an existing resource module by path prefix) or NON-STANDARD (needs-human,
# with a precise reason).
# --------------------------------------------------------------------------- #


def normalize_spec_path(path: str) -> str:
    """Strips the "/v1" prefix (the SDK's base_url already carries it, so no
    call-site f-string ever repeats it) and collapses every `{param}` segment
    to a bare `{}`, matching the shape produced by `_fstring_template`."""
    if path.startswith("/v1/"):
        path = path[3:]
    elif path == "/v1":
        path = ""
    return re.sub(r"\{[^}]*\}", "{}", path)


def path_param_names(path: str) -> list[str]:
    return re.findall(r"\{([^}]+)\}", path)


def _fstring_template(node: ast.expr) -> Optional[str]:
    """Reduces a call-site path argument to a template with every interpolation
    collapsed to `{}`, or None if it isn't a plain string/f-string literal (in
    which case it cannot be reconciled against the spec and is simply not
    counted as covering anything -- never mistaken for a match)."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for v in node.values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                parts.append(v.value)
            elif isinstance(v, ast.FormattedValue):
                parts.append("{}")
            else:
                return None
        return "".join(parts)
    return None


def _client_call_verb(call: ast.Call) -> Optional[str]:
    f = call.func
    if not isinstance(f, ast.Attribute) or f.attr not in HTTP_VERBS:
        return None
    obj = f.value
    if isinstance(obj, ast.Attribute) and obj.attr == "_client" and isinstance(obj.value, ast.Name):
        return f.attr if obj.value.id == "self" else None
    return None


def _singularize(name: str) -> str:
    return name[:-1] if name.endswith("s") and not name.endswith("ss") else name


@dataclass
class ResourceMethod:
    name: str
    verb: str
    template: str  # no "/v1" prefix, params collapsed to "{}"


@dataclass
class ResourceModule:
    file: Path
    async_class_name: str
    sync_class_name: Optional[str]
    factory_name: Optional[str]
    factory_sync_name: Optional[str]
    uses_instance_id: bool
    methods: list[ResourceMethod]
    prefix: str  # singularized PascalCase, e.g. "PartnerFeesResource" -> "PartnerFee"


def discover_resource_modules(src_root: Path = SRC_ROOT) -> list[ResourceModule]:
    """Derives, from the SDK source itself, which (verb, path template) each
    resource module already implements. Deliberately not a hand-maintained
    map (unlike spec-map.json's schema/enum entries, which need curation
    because names diverge): call-site f-strings are a direct, mechanical
    record of what a resource module actually does."""
    modules: list[ResourceModule] = []
    resources_dir = src_root / "resources"
    if not resources_dir.exists():
        return modules
    for f in sorted(resources_dir.rglob("*.py")):
        if f.name == "__init__.py":
            continue
        tree = ast.parse(f.read_text(), filename=str(f))
        classes = {n.name: n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)}
        for name, async_cls in sorted(classes.items()):
            if not name.endswith("Resource") or name.endswith("ResourceSync"):
                continue
            uses_instance_id = False
            for stmt in async_cls.body:
                if isinstance(stmt, ast.FunctionDef) and stmt.name == "__init__":
                    uses_instance_id = any(a.arg == "instance_id" for a in stmt.args.args)
            methods: list[ResourceMethod] = []
            for stmt in async_cls.body:
                if not isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)) or stmt.name == "__init__":
                    continue
                for node in ast.walk(stmt):
                    if not isinstance(node, ast.Call):
                        continue
                    verb = _client_call_verb(node)
                    if verb is None or not node.args:
                        continue
                    tmpl = _fstring_template(node.args[0])
                    if tmpl is None:
                        continue
                    tmpl = tmpl.split("?")[0]  # literal query strings (e.g. ?rail=...) aren't part of the route
                    tmpl = re.sub(r"\{[^}]*\}", "{}", tmpl)
                    # A `{}` glued directly onto the previous character (no "/" before it) is an
                    # interpolated query-string suffix built at runtime (e.g. f"...{query_string}"),
                    # never a path segment -- drop it so it isn't mistaken for a trailing path param.
                    tmpl = re.sub(r"(?<!/)\{\}$", "", tmpl)
                    methods.append(ResourceMethod(name=stmt.name, verb=verb, template=tmpl))
                    break  # the first client call in the method body is the operative one
            factory_name = None
            factory_sync_name = None
            for stmt in tree.body:
                if isinstance(stmt, ast.FunctionDef) and stmt.name.startswith("create_"):
                    if stmt.name.endswith("_resource_sync"):
                        factory_sync_name = stmt.name
                    elif stmt.name.endswith("_resource"):
                        factory_name = stmt.name
            sync_name = f"{name}Sync"
            modules.append(
                ResourceModule(
                    file=f,
                    async_class_name=name,
                    sync_class_name=sync_name if sync_name in classes else None,
                    factory_name=factory_name,
                    factory_sync_name=factory_sync_name,
                    uses_instance_id=uses_instance_id,
                    methods=methods,
                    prefix=_singularize(name[: -len("Resource")]),
                )
            )
    return modules


def covered_operations(modules: list[ResourceModule]) -> set[tuple[str, str]]:
    return {(m.verb, m.template) for mod in modules for m in mod.methods}


def _collection_prefix(template: str) -> str:
    """Strips trailing `/{}` path-param segments, e.g. "/x/{}/y/{}" -> "/x/{}/y"."""
    while template.endswith("/{}"):
        template = template[: -len("/{}")]
    return template


def _item_prefix(template: str) -> Optional[str]:
    """Everything up to and including the LAST path param, e.g.
    "/x/{}/y/{}/secret" -> "/x/{}/y/{}" -- this is what lets a GET whose path
    is "item param, then a literal sub-action" (".../{id}/secret") match a
    sibling method on the same item (".../{id}" DELETE). Only meaningful with
    2+ params: with exactly one (just the resource's own instance-id), this
    would collapse to a generic "/instances/{}" shared by nearly every
    resource and defeat the whole point of prefix matching."""
    if template.count("{}") < 2:
        return None
    idx = template.rfind("{}")
    return template[: idx + 2]


def find_matching_module(template: str, modules: list[ResourceModule]) -> Union[ResourceModule, str, None]:
    """The resource module whose own call templates already share this
    operation's collection prefix (or, failing that, its item prefix --
    see `_item_prefix`), `"ambiguous"` if more than one module qualifies,
    or None if none do."""
    target_collection = _collection_prefix(template)
    target_item = _item_prefix(template)
    matches = []
    for mod in modules:
        collections = {_collection_prefix(m.template) for m in mod.methods}
        items = {_item_prefix(m.template) for m in mod.methods} - {None}
        if target_collection in collections or (target_item is not None and target_item in items):
            matches.append(mod)
    if not matches:
        return None
    if len(matches) > 1:
        return "ambiguous"
    return matches[0]


class SynthesisError(Exception):
    def __init__(self, reason: str):
        self.reason = reason
        super().__init__(reason)


def _lookup_type_map(map_data: dict, spec_schema: str) -> Optional[dict]:
    """A named (`$ref`'d) schema is reusable only if spec-map.json already maps
    it 1:1 to a single SDK symbol (no specPath, no fan-out) -- anything else
    (a sub-object path, or a fan-out across several SDK variants) is a
    judgment call this function refuses to make silently."""
    for e in map_data.get("types", []):
        spec = e["spec"] if isinstance(e["spec"], list) else [e["spec"]]
        if spec == [spec_schema] and not e.get("specPath") and len(e["sdk"]) == 1:
            return e["sdk"][0]
    return None


def _lookup_enum_map(map_data: dict, schema: str, prop: str, is_items: bool) -> Optional[dict]:
    for e in map_data.get("enums", []):
        loc = e["spec"]
        if loc["schema"] == schema and loc["property"] == prop and bool(loc.get("items")) == is_items:
            return e["sdk"]
    return None


@dataclass
class FieldSpec:
    name: str
    annotation: str
    reused_symbol: Optional[dict] = None  # {"file": ..., "symbol": ...} if importing an existing type


def synth_field(
    field_name: str, prop_schema: dict, required: bool, named_schema: Optional[str], map_data: dict
) -> FieldSpec:
    """Synthesizes one TypedDict field from a spec property, reusing an
    existing mapped SDK symbol for any `$ref` or enum-constrained property
    (never inventing a new nested type or Literal -- that naming/placement
    call stays with a human) and SCALAR_TYPE_MAP for everything else. Raises
    SynthesisError with a precise, human-readable reason on anything it
    cannot express."""
    _, nullable = coarse_type(prop_schema)
    reused: Optional[dict] = None

    ref = prop_schema.get("$ref")
    if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
        ref_name = ref.split("/")[-1]
        site = _lookup_type_map(map_data, ref_name)
        if site is None:
            raise SynthesisError(f"property `{field_name}` references schema `{ref_name}` with no spec-map entry")
        py_type = site["symbol"]
        reused = site
    elif find_enum_locator(prop_schema) is not None:
        if named_schema is None:
            raise SynthesisError(f"property `{field_name}` is enum-constrained on an inline (unnamed) schema")
        is_items, _ = find_enum_locator(prop_schema)
        site = _lookup_enum_map(map_data, named_schema, field_name, is_items)
        if site is None:
            raise SynthesisError(f"property `{field_name}` is enum-constrained with no mapped Literal in spec-map.json")
        py_type = f"List[{site['symbol']}]" if is_items else site["symbol"]
        reused = site
    elif prop_schema.get("type") == "array" or (
        isinstance(prop_schema.get("type"), list) and "array" in prop_schema["type"]
    ):
        items = prop_schema.get("items", {}) if isinstance(prop_schema.get("items"), dict) else {}
        item_ref = items.get("$ref")
        if isinstance(item_ref, str) and item_ref.startswith("#/components/schemas/"):
            ref_name = item_ref.split("/")[-1]
            site = _lookup_type_map(map_data, ref_name)
            if site is None:
                raise SynthesisError(f"property `{field_name}` is an array of `{ref_name}` with no spec-map entry")
            py_type = f"List[{site['symbol']}]"
            reused = site
        else:
            t0, _ = coarse_type(items)
            scalar = SCALAR_TYPE_MAP.get(t0) if t0 else None
            if scalar is None:
                raise SynthesisError(f"property `{field_name}` is an array of a type the synthesizer cannot express")
            py_type = f"List[{scalar}]"
    else:
        t0, _ = coarse_type(prop_schema)
        if t0 is None:
            raise SynthesisError(f"property `{field_name}` has an ambiguous or multi-type spec shape")
        py_type = SCALAR_TYPE_MAP.get(t0)
        if py_type is None:
            raise SynthesisError(f"property `{field_name}` has spec type `{t0}`, which the synthesizer cannot express")

    if nullable:
        py_type = f"Optional[{py_type}]"
    if not required:
        py_type = f"NotRequired[{py_type}]"
    return FieldSpec(name=field_name, annotation=py_type, reused_symbol=reused)


@dataclass
class BodySpec:
    type_name: str
    fields: list[FieldSpec]
    named_schema: Optional[str]  # the $ref'd schema name, so a spec-map entry can be added for it


def resolve_json_content(container: dict, ctx: str) -> Optional[dict]:
    """Returns the `application/json` schema dict for a requestBody/response
    object, or None if there is no content at all. Raises SynthesisError if
    any *other* content type is present (multipart, binary, streaming, ...)."""
    content = container.get("content")
    if not content:
        return None
    other = sorted(set(content.keys()) - {"application/json"})
    if other:
        raise SynthesisError(f"{ctx} uses unsupported content type(s): {other}")
    return content.get("application/json", {}).get("schema")


def resolve_body_spec(
    schema: Optional[dict], spec: dict, map_data: dict, type_name: str, ctx: str
) -> Optional[BodySpec]:
    """Resolves a requestBody/response JSON schema (inline object, `$ref` to a
    named object schema, or None) into the fields for a brand-new TypedDict
    named `type_name`. Anything else a plain object -- oneOf/anyOf, a
    top-level array, a bare scalar -- is out of scope for STANDARD generation
    and raises SynthesisError with the exact shape that defeated it."""
    if schema is None:
        return None
    named_schema: Optional[str] = None
    node = schema
    if "$ref" in schema:
        ref = schema["$ref"]
        if not ref.startswith("#/components/schemas/"):
            raise SynthesisError(f"{ctx}: unsupported $ref `{ref}`")
        named_schema = ref.split("/")[-1]
        node = get_schema(spec, named_schema)
        if node is None:
            raise SynthesisError(f"{ctx}: $ref `{named_schema}` does not resolve to a component schema")
    if "oneOf" in node or "anyOf" in node:
        kind = "oneOf" if "oneOf" in node else "anyOf"
        raise SynthesisError(f"{ctx}: schema uses {kind}, which is unsupported")
    if node.get("type") not in (None, "object") or "properties" not in node:
        raise SynthesisError(f"{ctx}: schema is not a plain JSON object")
    required = get_required(node)
    fields = [
        synth_field(name, prop, name in required, named_schema, map_data) for name, prop in get_properties(node).items()
    ]
    return BodySpec(type_name=type_name, fields=fields, named_schema=named_schema)


@dataclass
class OperationInsertPlan:
    path: str
    verb: str
    module: ResourceModule
    method_name: str
    path_args: list[str]  # extra path params (instance_id already excluded), in call order
    input_type_name: Optional[str]  # None if this operation has no request body
    input_spec: Optional[BodySpec]  # non-None iff a brand-new TypedDict must be generated for it
    output_type_name: str  # "None" (as a literal type, for BlindpayApiResponse[None]) if no response body
    output_spec: Optional[BodySpec]


def derive_method_and_output_name(
    verb: str, template: str, prefix: str, drop_leading_param: bool
) -> tuple[str, bool, Optional[str]]:
    """Returns (method_name, is_list, output_type_base_name). output_type_base
    already has the "Get"/"List" prefix and "Response" suffix applied where
    the verb implies a response type name; None means "no synthesized name
    needed yet" (POST/PUT/PATCH/DELETE decide their own below).

    `drop_leading_param` discards the resource's own instance-id placeholder
    (e.g. the `{}` in "/instances/{}/transfers") before reading off the last
    segment(s) -- otherwise a plain collection GET right under the instance
    (".../transfers") is misread as a single-item fetch, because the
    instance-id placeholder immediately precedes it."""
    if verb == "get":
        segments = [s for s in template.split("/") if s]
        if drop_leading_param:
            for i, s in enumerate(segments):
                if s == "{}":
                    del segments[i]
                    break
        if not segments or segments[-1] != "{}":
            if len(segments) >= 2 and segments[-2] == "{}":
                suffix = "".join(p.capitalize() for p in re.split(r"[-_]", segments[-1]))
                return f"get_{segments[-1].replace('-', '_')}", False, f"Get{prefix}{suffix}Response"
            return "list", True, f"List{prefix}sResponse"
        return "get", False, f"Get{prefix}Response"
    if verb == "post":
        return "create", False, f"Create{prefix}Response"
    if verb in ("put", "patch"):
        return "update", False, f"Update{prefix}Response"
    if verb == "delete":
        return "delete", False, None
    raise AssertionError(verb)


def classify_operation(
    path: str, verb: str, op: dict, spec: dict, modules: list[ResourceModule], map_data: dict
) -> Union[OperationInsertPlan, NeedsHuman]:
    norm = normalize_spec_path(path)
    ctx = f"{verb.upper()} {path}"
    match = find_matching_module(norm, modules)
    if match is None:
        return NeedsHuman("needs_human_operation", f"{ctx}: no existing resource matches this path's prefix")
    if match == "ambiguous":
        return NeedsHuman("needs_human_operation", f"{ctx}: more than one resource module matches this path's prefix")
    module = match
    assert isinstance(module, ResourceModule)

    all_params = path_param_names(path)
    path_args = all_params[1:] if module.uses_instance_id and all_params else all_params

    method_name, is_list, output_name = derive_method_and_output_name(
        verb, norm, module.prefix, drop_leading_param=module.uses_instance_id
    )
    if any(m.name == method_name for m in module.methods):
        return NeedsHuman(
            "needs_human_operation",
            f"{ctx}: derived method name `{method_name}` already exists on {module.async_class_name}",
        )

    try:
        response_schema = None
        for status, resp in sorted(op.get("responses", {}).items()):
            if status.startswith("2") and isinstance(resp, dict):
                response_schema = resolve_json_content(resp, f"{ctx} response {status}")
                break

        output_spec: Optional[BodySpec] = None
        if response_schema is None:
            output_type_name = "None"
        elif response_schema.get("type") == "array":
            items = response_schema.get("items", {}) if isinstance(response_schema.get("items"), dict) else {}
            item_ref = items.get("$ref")
            if isinstance(item_ref, str) and item_ref.startswith("#/components/schemas/"):
                ref_name = item_ref.split("/")[-1]
                site = _lookup_type_map(map_data, ref_name)
                if site is None:
                    raise SynthesisError(f"response is an array of `{ref_name}` with no spec-map entry")
                output_type_name = f"List[{site['symbol']}]"
            else:
                t0, _ = coarse_type(items)
                scalar = SCALAR_TYPE_MAP.get(t0) if t0 else None
                if scalar is None:
                    raise SynthesisError("response is a top-level array of a type the synthesizer cannot express")
                output_type_name = f"List[{scalar}]"
        else:
            output_type_name = output_name or f"{module.prefix}Response"
            output_spec = resolve_body_spec(response_schema, spec, map_data, output_type_name, f"{ctx} response")

        input_type_name: Optional[str] = None
        input_spec: Optional[BodySpec] = None
        request_body = op.get("requestBody")
        if request_body:
            req_schema = resolve_json_content(request_body, f"{ctx} request body")
            input_type_name = f"{'Create' if verb == 'post' else 'Update'}{module.prefix}Input"
            input_spec = resolve_body_spec(req_schema, spec, map_data, input_type_name, f"{ctx} request body")
    except SynthesisError as e:
        return NeedsHuman("needs_human_operation", f"{ctx}: {e.reason}")

    return OperationInsertPlan(
        path=path,
        verb=verb,
        module=module,
        method_name=method_name,
        path_args=path_args,
        input_type_name=input_type_name,
        input_spec=input_spec,
        output_type_name=output_type_name,
        output_spec=output_spec,
    )


def unmodeled_operation_allowed(unmodeled: list[dict], verb: str, path: str) -> bool:
    return any(e.get("kind") == "operation" and e["method"].lower() == verb and e["path"] == path for e in unmodeled)


def reconcile_operations(
    spec: dict,
    map_data: dict,
    unmodeled: Optional[list[dict]] = None,
    modules: Optional[list[ResourceModule]] = None,
) -> tuple[list[OperationInsertPlan], list[NeedsHuman]]:
    if modules is None:
        modules = discover_resource_modules()
    unmodeled = unmodeled or []
    covered = covered_operations(modules)
    plans: list[OperationInsertPlan] = []
    problems: list[NeedsHuman] = []
    for path, item in sorted(spec.get("paths", {}).items()):
        if not isinstance(item, dict):
            continue
        for verb, op in sorted(item.items()):
            if verb not in HTTP_VERBS or not isinstance(op, dict):
                continue
            if (verb, normalize_spec_path(path)) in covered:
                continue
            if unmodeled_operation_allowed(unmodeled, verb, path):
                continue
            result = classify_operation(path, verb, op, spec, modules, map_data)
            if isinstance(result, OperationInsertPlan):
                plans.append(result)
            else:
                problems.append(result)
    return plans, problems


# --------------------------------------------------------------------------- #
# Applying changes (text splicing)
# --------------------------------------------------------------------------- #


@dataclass
class AppliedChange:
    kind: str  # "enum" | "property"
    file: str
    symbol: str
    detail: str


def splice_literal_add_members(source: str, node: ast.Assign, new_values: list[str]) -> str:
    lines = source.splitlines(keepends=True)
    subscript = node.value
    assert isinstance(subscript, ast.Subscript)
    sl = subscript.slice
    elts = sl.elts if isinstance(sl, ast.Tuple) else [sl]
    last = elts[-1]

    close_lineno = subscript.end_lineno
    last_end_line = last.end_lineno
    last_end_col = last.end_col_offset

    if close_lineno == last_end_line:
        line = lines[last_end_line - 1]
        insertion = "".join(f', "{v}"' for v in new_values)
        lines[last_end_line - 1] = line[:last_end_col] + insertion + line[last_end_col:]
    else:
        last_line = lines[last_end_line - 1]
        stripped_no_nl = last_line[:-1] if last_line.endswith("\n") else last_line
        indent = last_line[: len(last_line) - len(last_line.lstrip())]
        if not stripped_no_nl.rstrip().endswith(","):
            nl = "\n" if last_line.endswith("\n") else ""
            lines[last_end_line - 1] = stripped_no_nl + "," + nl
        insert_lines = [f'{indent}"{v}",\n' for v in new_values]
        lines[last_end_line:last_end_line] = insert_lines
    return "".join(lines)


def apply_enum_change(gap: EnumGap, index: SdkIndex) -> AppliedChange:
    entry = index.find_literal(gap.symbol, gap.file)
    if entry is None:
        raise SystemExit(f"internal error: lost track of literal {gap.symbol} in {gap.file}")
    file_path, node, source = entry
    new_source = splice_literal_add_members(source, node, sorted(gap.missing))
    file_path.write_text(new_source)
    return AppliedChange(
        kind="enum",
        file=str(file_path.relative_to(ROOT)),
        symbol=gap.symbol,
        detail=f"added member(s) {sorted(gap.missing)}",
    )


def infer_annotation(prop_schema: dict) -> Optional[str]:
    if "enum" in prop_schema:
        return None  # would need a Literal/mapped enum symbol; not auto-resolved
    if prop_schema.get("type") == "array" or (
        isinstance(prop_schema.get("type"), list) and "array" in prop_schema["type"]
    ):
        return None
    t0, _nullable = coarse_type(prop_schema)
    if t0 is None:
        return None
    return SCALAR_TYPE_MAP.get(t0)


def choose_field_annotation(info: ClassInfo, python_type: str, nullable: bool) -> str:
    """A newly ADDED optional spec property must never turn into a required
    dict key. Whether that needs an explicit NotRequired[...] wrapper depends
    entirely on the target class's totality, not on sibling style:
    - total=False (a class declared `total=False`, or the non-required half
      of the `_XRequired` two-part pattern -- `info` is always the class we
      insert into, which for that pattern already IS the total=False side):
      every key is already optional, so a bare `T` / `Optional[T]` is correct
      and sufficient.
    - total=True (the default, e.g. `class CreateQuoteInput(TypedDict):`):
      every key is structurally REQUIRED regardless of whether its value type
      happens to be Optional[...]. Adding a bare `Optional[T]` field here
      would make every existing caller that omits the new key fail pyright
      and mypy -- a breaking change to an already-published TypedDict. This
      always needs `NotRequired[...]`, independent of whether any sibling
      field already uses that convention.
    """
    inner = f"Optional[{python_type}]" if nullable else python_type
    if info.total_false:
        return inner
    return f"NotRequired[{inner}]"


def splice_typeddict_add_field(source: str, class_node: ast.ClassDef, field_name: str, annotation_text: str) -> str:
    lines = source.splitlines(keepends=True)
    last_stmt = class_node.body[-1]
    last_line_no = last_stmt.end_lineno
    last_line = lines[last_line_no - 1]
    indent = last_line[: len(last_line) - len(last_line.lstrip())]
    new_line = f"{indent}{field_name}: {annotation_text}\n"
    lines.insert(last_line_no, new_line)
    return "".join(lines)


def ensure_name_imported(
    source: str, name: str, candidate_modules: tuple[str, ...] = ("typing", "typing_extensions")
) -> str:
    """Add `name` to whichever of `candidate_modules` this file already imports
    TypedDict from (matching that file's own typing vs typing_extensions
    convention), if it is not already imported from either. A no-op if `name`
    is already present. Assumes a single-line, non-aliased import statement,
    which is what every TypedDict-bearing file in this repo currently uses."""
    tree = ast.parse(source)
    target: Optional[ast.ImportFrom] = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in candidate_modules:
            names = [a.name for a in node.names]
            if name in names:
                return source
            if "TypedDict" in names:
                target = node
    if target is None:
        return source

    names = sorted({a.name for a in target.names} | {name})
    new_line = f"from {target.module} import {', '.join(names)}"
    lines = source.splitlines(keepends=True)
    start, end = target.lineno, target.end_lineno
    assert end is not None
    trailing = "\n" if lines[end - 1].endswith("\n") else ""
    lines[start - 1 : end] = [new_line + trailing]
    return "".join(lines)


def apply_property_change(gap: PropertyGap, index: SdkIndex) -> tuple[list[AppliedChange], list[NeedsHuman]]:
    applied: list[AppliedChange] = []
    needs_human: list[NeedsHuman] = []

    if len(gap.sdk_sites) > 1:
        ctx = "/".join(gap.schema_names) + (f"#{gap.path}" if gap.path else "")
        needs_human.append(
            NeedsHuman(
                "fan_out_target_ambiguous",
                f"{ctx}: new propert{'y' if len(gap.missing) == 1 else 'ies'} {sorted(gap.missing)} on a "
                f"{len(gap.sdk_sites)}-variant fan-out; a human must decide which variant(s) legitimately "
                f"carry it (or opt the map entry into uniform fan-out application).",
            )
        )
        return applied, needs_human

    site = gap.sdk_sites[0]
    symbol = site["symbol"]
    info = index.find_class(symbol, site["file"])
    if info is None:
        needs_human.append(NeedsHuman("unresolved_anchor", f"{symbol} not found in {site['file']}"))
        return applied, needs_human

    for name in sorted(gap.missing):
        prop_schema = gap.missing[name]
        python_type = infer_annotation(prop_schema)
        if python_type is None:
            ctx = "/".join(gap.schema_names) + (f"#{gap.path}" if gap.path else "")
            needs_human.append(
                NeedsHuman(
                    "type_unresolvable",
                    f"{ctx}.{name}: cannot safely infer a Python type from the spec schema for {symbol}",
                )
            )
            continue
        _, nullable = coarse_type(prop_schema)
        annotation = choose_field_annotation(info, python_type, nullable)
        source = info.source
        for required_name in ("NotRequired", "Optional"):
            if f"{required_name}[" in annotation:
                updated = ensure_name_imported(source, required_name)
                if updated != source:
                    source = updated
                    info.file.write_text(source)
                    info.node = _reparse_class(info.file, symbol)
        new_source = splice_typeddict_add_field(source, info.node, name, annotation)
        info.file.write_text(new_source)
        # re-read so subsequent insertions into the same class see updated positions
        info.source = new_source
        info.node = _reparse_class(info.file, symbol)
        applied.append(
            AppliedChange(
                kind="property",
                file=str(info.file.relative_to(ROOT)),
                symbol=symbol,
                detail=f"added field `{name}: {annotation}`",
            )
        )
    return applied, needs_human


def _reparse_class(file_path: Path, symbol: str) -> ast.ClassDef:
    tree = ast.parse(file_path.read_text(), filename=str(file_path))
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == symbol:
            return node
    raise SystemExit(f"internal error: lost track of class {symbol} in {file_path} after edit")


# --------------------------------------------------------------------------- #
# Applying operation-insert changes
# --------------------------------------------------------------------------- #


def render_typeddict(body: BodySpec) -> str:
    lines = [f"class {body.type_name}(TypedDict):"]
    for f in body.fields:
        lines.append(f"    {f.name}: {f.annotation}")
    if not body.fields:
        lines.append("    pass")
    return "\n".join(lines) + "\n"


def _find_class(source: str, name: str) -> ast.ClassDef:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    raise SystemExit(f"internal error: class {name} not found while applying an operation-insert")


def insert_typeddicts_before_class(source: str, class_name: str, blocks: list[str]) -> str:
    if not blocks:
        return source
    class_node = _find_class(source, class_name)
    lines = source.splitlines(keepends=True)
    text = "\n\n".join(b.rstrip("\n") for b in blocks) + "\n\n\n"
    lines[class_node.lineno - 1 : class_node.lineno - 1] = [text]
    return "".join(lines)


def append_method(source: str, class_name: str, method_source: str) -> str:
    class_node = _find_class(source, class_name)
    last_stmt = class_node.body[-1]
    last_line_no = last_stmt.end_lineno
    assert last_line_no is not None
    lines = source.splitlines(keepends=True)
    indented = "\n".join(f"    {ln}" if ln else ln for ln in method_source.rstrip("\n").split("\n"))
    lines.insert(last_line_no, "\n" + indented + "\n")
    return "".join(lines)


def build_path_fstring(path: str, module: ResourceModule) -> str:
    path_wo_v1 = path[3:] if path.startswith("/v1/") else path
    names = path_param_names(path)
    if module.uses_instance_id and names:
        path_wo_v1 = path_wo_v1.replace("{" + names[0] + "}", "{self._instance_id}", 1)
    return path_wo_v1


def render_method(plan: OperationInsertPlan, is_sync: bool) -> str:
    args = [f"{a}: str" for a in plan.path_args]
    if plan.input_type_name:
        args.append(f"data: {plan.input_type_name}")
    arg_str = ", ".join(["self", *args])
    fstring = build_path_fstring(plan.path, plan.module)
    call_args = f'f"{fstring}"' + (", data" if plan.input_type_name else "")
    awaited = "" if is_sync else "await "
    async_kw = "" if is_sync else "async "
    client_call = f"self._client.{plan.verb}({call_args})"
    return (
        f"{async_kw}def {plan.method_name}({arg_str}) -> BlindpayApiResponse[{plan.output_type_name}]:\n"
        f"    return {awaited}{client_call}\n"
    )


def apply_operation_insert(plan: OperationInsertPlan, map_data: dict) -> AppliedChange:
    module = plan.module
    file_path = module.file
    source = file_path.read_text()

    new_blocks = [render_typeddict(spec) for spec in (plan.input_spec, plan.output_spec) if spec is not None]
    source = insert_typeddicts_before_class(source, module.async_class_name, new_blocks)

    source = append_method(source, module.async_class_name, render_method(plan, is_sync=False))
    if module.sync_class_name:
        source = append_method(source, module.sync_class_name, render_method(plan, is_sync=True))

    needed_wrappers = {
        kw
        for spec in (plan.input_spec, plan.output_spec)
        if spec
        for f in spec.fields
        for kw in ("NotRequired", "Optional")
        if f"{kw}[" in f.annotation
    }
    for kw in sorted(needed_wrappers):
        source = ensure_name_imported(source, kw)

    for spec in (plan.input_spec, plan.output_spec):
        if spec and spec.named_schema:
            map_data.setdefault("types", []).append(
                {
                    "spec": spec.named_schema,
                    "sdk": [{"file": str(file_path.relative_to(ROOT)), "symbol": spec.type_name}],
                }
            )

    file_path.write_text(source)
    try:
        subprocess.run([sys.executable, "-m", "ruff", "format", "--quiet", str(file_path)], check=False)
        subprocess.run(
            [sys.executable, "-m", "ruff", "check", "--fix", "--quiet", "--select=I", str(file_path)], check=False
        )
    except FileNotFoundError:
        pass  # ruff not available in this environment; the generated source is still valid Python

    return AppliedChange(
        kind="operation-insert",
        file=str(file_path.relative_to(ROOT)),
        symbol=f"{module.async_class_name}.{plan.method_name}",
        detail=f"added {plan.verb.upper()} {plan.path} as {module.async_class_name}.{plan.method_name}()",
    )


# --------------------------------------------------------------------------- #
# Coverage report (non-blocking)
# --------------------------------------------------------------------------- #


def coverage_report(spec: dict, map_data: dict) -> list[dict]:
    reachable = compute_reachable_schemas(spec)
    ignore_reasons = {e["schema"]: e["reason"] for e in map_data.get("ignore", {}).get("schemas", [])}
    mapped_names: set[str] = set()
    for e in map_data.get("types", []):
        spec_names = e["spec"] if isinstance(e["spec"], list) else [e["spec"]]
        mapped_names.update(spec_names)

    gaps = []
    for p, item in sorted(spec.get("paths", {}).items()):
        if not isinstance(item, dict):
            continue
        for method, op in sorted(item.items()):
            if method not in ("get", "post", "put", "patch", "delete") or not isinstance(op, dict):
                continue
            # only the request body and SUCCESS (2xx) responses are relevant here;
            # 4xx/5xx responses almost all reference the shared Error schema and
            # would otherwise drown every operation in a false "gap".
            names: set[str] = set()
            rb = op.get("requestBody", {}).get("content", {})
            for c in rb.values():
                r = c.get("schema", {}).get("$ref")
                if r:
                    names.add(r.split("/")[-1])
            responses = op.get("responses", {})
            for status, resp in responses.items():
                if not isinstance(resp, dict) or not status.startswith("2"):
                    continue
                r = resp.get("content", {}).get("application/json", {}).get("schema", {}).get("$ref")
                if r:
                    names.add(r.split("/")[-1])
            names &= reachable
            ignored = sorted(n for n in names if n in ignore_reasons)
            if ignored and not (names - set(ignore_reasons)):
                gaps.append(
                    {
                        "method": method.upper(),
                        "path": p,
                        "schemas": ignored,
                        "reason": ignore_reasons[ignored[0]],
                    }
                )
    return gaps


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #


def cmd_validate_map() -> int:
    index = build_sdk_index(SRC_ROOT)
    map_data = load_map()
    errors = validate_map(map_data, index)
    if errors:
        print("Map validity -- FAILED:")
        for e in sorted(errors):
            print(f"  {e}")
        return 1
    print("Map validity: OK")
    return 0


def cmd_check(report_path: Optional[Path]) -> int:
    index = build_sdk_index(SRC_ROOT)
    map_data = load_map()
    unmodeled = load_unmodeled()

    map_errors = validate_map(map_data, index)
    spec = load_json(SNAPSHOT_PATH)
    enum_gaps = reconcile_enums(spec, map_data, unmodeled, index) if not map_errors else []
    prop_gaps = reconcile_types(spec, map_data, unmodeled, index) if not map_errors else []
    enum_coverage_gaps = reconcile_enum_coverage(spec, map_data, unmodeled, index) if not map_errors else []
    nested_gaps = reconcile_nested_coverage(spec, map_data, unmodeled) if not map_errors else []
    op_plans, op_needs_human = (
        reconcile_operations(spec, map_data, unmodeled, discover_resource_modules(SRC_ROOT))
        if not map_errors
        else ([], [])
    )

    report = {
        "mode": "check",
        "map_errors": sorted(map_errors),
        "enum_gaps": [{"symbol": g.symbol, "file": g.file, "missing": g.missing} for g in enum_gaps],
        "property_gaps": [
            {"schema": g.schema_names, "path": g.path, "missing": sorted(g.missing.keys())} for g in prop_gaps
        ],
        "enum_coverage_gaps": [
            {"schema": g.schema, "path": g.path, "property": g.property} for g in enum_coverage_gaps
        ],
        "nested_object_gaps": [{"schema": g.schema, "path": g.path} for g in nested_gaps],
        "operation_gaps": [f"{p.verb.upper()} {p.path}" for p in op_plans],
        "operation_needs_human": [{"kind": n.kind, "detail": n.detail} for n in op_needs_human],
    }
    if report_path:
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    if not (map_errors or enum_gaps or prop_gaps or enum_coverage_gaps or nested_gaps or op_plans or op_needs_human):
        return 0

    if map_errors:
        print("spec-map.json validity -- FAILED:")
        for e in sorted(map_errors):
            print(f"  {e}")
    for p in op_plans:
        print(
            f"PENDING DRIFT (operation-insert): {p.verb.upper()} {p.path} has no SDK method yet and is "
            f"auto-generatable; run --apply to add {p.module.async_class_name}.{p.method_name}()."
        )
    for n in op_needs_human:
        print(f"NEEDS_HUMAN (operation): {n.detail}")
    for g in enum_gaps:
        print(
            f"PENDING DRIFT (enum): {g.symbol} in {g.file} is missing {g.missing}; add to the Literal "
            f"or record in .api-sync/unmodeled.json (kind=enum) with a reason and owner."
        )
    for g in prop_gaps:
        ctx = "/".join(g.schema_names) + (f"#{g.path}" if g.path else "")
        print(
            f"PENDING DRIFT (property): {ctx} is missing {sorted(g.missing.keys())} on "
            f"{[s['symbol'] for s in g.sdk_sites]}; add the field(s) or record in "
            f".api-sync/unmodeled.json (kind=property) with a reason and owner."
        )
    for g in enum_coverage_gaps:
        ctx = g.schema + (f"#{g.path}" if g.path else "")
        print(
            f"ENUM COVERAGE GAP: {ctx}.{g.property} is enum-constrained in the spec but is not mapped "
            f"to an SDK Literal via spec-map.json's `enums` list; map it or record it in "
            f".api-sync/unmodeled.json (kind=enum_coverage) with a reason and owner."
        )
    for g in nested_gaps:
        print(
            f"NESTED OBJECT COVERAGE GAP: {g.schema}#{g.path} is an inline object/array-item shape with no "
            f"map entry; add a specPath map entry for it or record it in .api-sync/unmodeled.json "
            f"(kind=nested_object) with a reason and owner."
        )
    return 1


def cmd_apply(spec_path: Path, report_path: Optional[Path]) -> int:
    index = build_sdk_index(SRC_ROOT)
    map_data = load_map()
    unmodeled = load_unmodeled()

    map_errors = validate_map(map_data, index)
    if map_errors:
        print("spec-map.json validity -- FAILED, refusing to apply:")
        for e in sorted(map_errors):
            print(f"  {e}")
        return 1

    old_spec = load_json(SNAPSHOT_PATH)
    new_spec = load_json(spec_path)

    needs_human = diff_removals_and_changes(old_spec, new_spec, map_data, index)

    enum_gaps = reconcile_enums(new_spec, map_data, unmodeled, index)
    prop_gaps = reconcile_types(new_spec, map_data, unmodeled, index)
    op_plans, op_needs_human = reconcile_operations(new_spec, map_data, unmodeled, discover_resource_modules(SRC_ROOT))
    needs_human.extend(op_needs_human)

    applied: list[AppliedChange] = []

    if not needs_human:
        for g in sorted(enum_gaps, key=lambda g: g.symbol):
            applied.append(apply_enum_change(g, index))
        # re-check property gaps against a fresh index is unnecessary: enum edits never touch TypedDicts
        for g in sorted(prop_gaps, key=lambda g: ("/".join(g.schema_names), g.path or "")):
            a, nh = apply_property_change(g, index)
            applied.extend(a)
            needs_human.extend(nh)
        for p in sorted(op_plans, key=lambda p: (p.verb, p.path)):
            applied.append(apply_operation_insert(p, map_data))
        if op_plans:
            MAP_PATH.write_text(json.dumps(map_data, indent=2) + "\n")

    bump: Optional[str] = None
    if not needs_human:
        if any(a.kind in ("enum", "operation-insert") for a in applied):
            bump = "minor"
        elif applied:
            bump = "patch"

    report = {
        "mode": "apply",
        "spec": str(spec_path),
        "applied": [{"kind": a.kind, "file": a.file, "symbol": a.symbol, "detail": a.detail} for a in applied],
        "needs_human": [
            {"kind": n.kind, "detail": n.detail} for n in sorted(needs_human, key=lambda n: (n.kind, n.detail))
        ],
        "bump": bump,
        "coverage_gaps": coverage_report(new_spec, map_data),
    }
    if report_path:
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    if needs_human:
        print("NEEDS_HUMAN -- refusing to apply:")
        for n in report["needs_human"]:
            print(f"  [{n['kind']}] {n['detail']}")
        return 1

    if applied:
        # Copy the delivered spec's exact bytes rather than round-tripping through
        # json.dumps: re-serializing would reformat/reorder the *entire* file on
        # every apply (noise unrelated to the actual drift) and is not needed for
        # determinism -- the upstream filter already produces stable formatting.
        SNAPSHOT_PATH.write_bytes(spec_path.read_bytes())
        print(f"Applied {len(applied)} change(s); bump={bump}")
        for a in applied:
            print(f"  [{a.kind}] {a.file}: {a.detail}")
    else:
        print("No changes.")
    return 0


def cmd_coverage(spec_path: Path) -> int:
    map_data = load_map()
    spec = load_json(spec_path) if spec_path.exists() else load_json(SNAPSHOT_PATH)
    gaps = coverage_report(spec, map_data)
    if not gaps:
        print("Coverage: no known gaps.")
        return 0
    print(f"Coverage report ({len(gaps)} known gap(s), non-blocking):")
    for g in gaps:
        print(f"  {g['method']} {g['path']}  ({', '.join(g['schemas'])}): {g['reason']}")
    return 0


# --------------------------------------------------------------------------- #
# Type audit (non-blocking, informational): does the SDK's CURRENT annotation
# for every mapped property still match the spec's CURRENT declared type,
# independent of any old-vs-new diff? diff_removals_and_changes only ever
# catches drift going forward from a synced baseline; it cannot see a
# pre-existing latent mismatch that was already there when a field was first
# modeled. This reuses the same primitives (coarse_type, SCALAR_TYPE_MAP) in a
# state comparison instead of a diff, mirroring how reconcile_* replaced
# event-diffing with state reconciliation for presence.
# --------------------------------------------------------------------------- #


def collect_annotations(
    symbol: str, file_rel: str, index: SdkIndex, seen: Optional[set[str]] = None
) -> dict[str, tuple[ast.expr, str]]:
    """field name -> (annotation node, source text) across the class and any
    locally-defined base (the `_XRequired` two-part pattern)."""
    seen = seen or set()
    key = f"{file_rel}::{symbol}"
    if key in seen:
        return {}
    seen.add(key)
    info = index.find_class(symbol, file_rel)
    if info is None:
        return {}
    result: dict[str, tuple[ast.expr, str]] = {}
    for base in info.bases:
        result.update(collect_annotations(base, str(info.file.relative_to(ROOT)), index, seen))
    for name, node in info.own_fields.items():
        result[name] = (node.annotation, info.source)
    return result


def _strip_wrappers(ann_text: str) -> tuple[str, bool]:
    """Returns (innermost type text, was_optional)."""
    text = ann_text.strip()
    if text.startswith("NotRequired[") and text.endswith("]"):
        text = text[len("NotRequired[") : -1].strip()
    is_optional = False
    if text.startswith("Optional[") and text.endswith("]"):
        is_optional = True
        text = text[len("Optional[") : -1].strip()
    return text, is_optional


def audit_property_type(prop_schema: dict, ann_text: str) -> Optional[str]:
    """A property with no direct SDK counterpart is not this function's
    concern (that's reconcile_types'). Only flags cases where the SDK
    annotation is NARROWER or otherwise structurally wrong versus the spec --
    a SDK type that is deliberately wider than necessary (e.g. Optional[str]
    for a non-nullable property, or float for a spec integer) is a legitimate,
    common modeling choice, not a bug, and is not reported."""
    inner, is_optional = _strip_wrappers(ann_text)
    base_type, nullable = coarse_type(prop_schema)

    if nullable and not is_optional:
        return f"spec is nullable but SDK annotation `{ann_text}` has no Optional[...]"

    if "enum" in prop_schema:
        if inner in SCALAR_TYPE_MAP.values():
            return f"spec property is enum-constrained but SDK annotation is a bare `{inner}` (no Literal)"
        return None  # trust some Literal/mapped-symbol reference; membership is reconcile_enums's job

    if base_type is None:
        return None  # ambiguous on the spec side (multi-type, or no "type" key) -- nothing to compare
    if base_type == "array":
        return None if inner.startswith(("List[", "list[")) else f"spec type is array but SDK annotation is `{inner}`"
    if base_type == "object":
        if inner in SCALAR_TYPE_MAP.values():
            return f"spec type is object but SDK annotation is a bare scalar `{inner}`"
        return None  # assume a nested TypedDict reference; not verifying its own shape here

    expected = SCALAR_TYPE_MAP.get(base_type)
    if expected is None or inner == expected:
        return None
    if base_type == "integer" and inner == "float":
        return None  # deliberately compatible widening
    return f"spec type `{base_type}` (expected `{expected}`) but SDK annotation is `{inner}`"


def audit_types(spec: dict, map_data: dict) -> list[dict[str, str]]:
    """One map entry can list several spec locators that are asserted to share
    the same shape (e.g. tracking_payment duplicated inline across 6 payout
    schemas) -- audit against a single representative locator, not once per
    duplicate, or the same real finding is reported N times over."""
    index = build_sdk_index(SRC_ROOT)
    reachable = compute_reachable_schemas(spec)
    findings: list[dict[str, str]] = []

    for e in map_data.get("types", []):
        spec_names = e["spec"] if isinstance(e["spec"], list) else [e["spec"]]
        path = e.get("specPath")
        reachable_names = sorted(n for n in spec_names if n in reachable)
        if not reachable_names:
            continue
        representative = reachable_names[0]
        schema_obj = get_schema(spec, representative)
        if schema_obj is None:
            continue
        schema_label = (
            representative
            if len(reachable_names) == 1
            else f"{representative} (+{len(reachable_names) - 1} shared locator(s))"
        )
        props = get_properties(resolve_path(schema_obj, path))
        for site in e["sdk"]:
            annotations = collect_annotations(site["symbol"], site["file"], index)
            for field_name in sorted(props.keys()):
                if field_name not in annotations:
                    continue
                ann_node, source = annotations[field_name]
                ann_text = ast.get_source_segment(source, ann_node) or ""
                note = audit_property_type(props[field_name], ann_text)
                if note:
                    findings.append(
                        {
                            "schema": schema_label,
                            "path": path or "",
                            "field": field_name,
                            "sdk_file": site["file"],
                            "sdk_symbol": site["symbol"],
                            "sdk_annotation": ann_text,
                            "note": note,
                        }
                    )

    # a single SDK field (same file+symbol+field+annotation) can legitimately
    # get evaluated from more than one map entry -- e.g. TrackingPayment is
    # the target of both a payout-side and a payin-side entry. Collapse those
    # into one finding that names every schema it was seen from, rather than
    # reporting what is really the same annotation issue multiple times.
    merged: dict[tuple[str, str, str, str], dict[str, str]] = {}
    for f in findings:
        key = (f["sdk_file"], f["sdk_symbol"], f["field"], f["note"])
        if key in merged:
            if f["schema"] not in merged[key]["schema"]:
                merged[key]["schema"] += f", {f['schema']}"
        else:
            merged[key] = dict(f)
    result = list(merged.values())
    result.sort(key=lambda f: (f["sdk_file"], f["sdk_symbol"], f["field"]))
    return result


def cmd_audit_types(spec_path: Path) -> int:
    map_data = load_map()
    spec = load_json(spec_path) if spec_path.exists() else load_json(SNAPSHOT_PATH)
    findings = audit_types(spec, map_data)
    if not findings:
        print("Type audit: no mismatches found.")
        return 0
    print(f"Type audit ({len(findings)} finding(s), non-blocking, informational only):")
    for f in findings:
        ctx = f["schema"] + (f"/{f['path']}" if f["path"] else "")
        site = f"{f['sdk_symbol']} in {f['sdk_file']}"
        print(f"  {ctx}.{f['field']} ({site}): {f['note']} [annotation: {f['sdk_annotation']}]")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--validate-map", action="store_true")
    mode.add_argument("--coverage", action="store_true")
    mode.add_argument("--audit-types", action="store_true")
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC_PATH)
    parser.add_argument("--report", type=Path, default=None)
    args = parser.parse_args()

    if args.validate_map:
        return cmd_validate_map()
    if args.check:
        return cmd_check(args.report)
    if args.apply:
        return cmd_apply(args.spec, args.report)
    if args.coverage:
        return cmd_coverage(args.spec)
    if args.audit_types:
        return cmd_audit_types(args.spec)
    return 1


if __name__ == "__main__":
    sys.exit(main())
