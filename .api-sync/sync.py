#!/usr/bin/env python3
"""Deterministic spec -> SDK patcher.

Run locally with:
    python3 .api-sync/sync.py --check
    python3 .api-sync/sync.py --apply [--spec PATH] [--report PATH]
    python3 .api-sync/sync.py --validate-map
    python3 .api-sync/sync.py --coverage [--spec PATH]

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
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parent.parent
API_SYNC = Path(__file__).resolve().parent
SRC_ROOT = ROOT / "src" / "blindpay"

SNAPSHOT_PATH = API_SYNC / "spec-snapshot.json"
DEFAULT_SPEC_PATH = API_SYNC / "spec-current.json"
MAP_PATH = API_SYNC / "spec-map.json"
UNMODELED_PATH = API_SYNC / "unmodeled.json"

SCALAR_TYPE_MAP = {"string": "str", "integer": "int", "number": "float", "boolean": "bool"}


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
        else:
            raise SystemExit(f"{UNMODELED_PATH}[{i}]: unknown or missing 'kind' (expected 'property' or 'enum')")
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
                old_type, _ = coarse_type(old_props[f])
                new_type, _ = coarse_type(new_props[f])
                if old_type is not None and new_type is not None and old_type != new_type:
                    problems.append(
                        NeedsHuman(
                            "type_change",
                            f"{name}{'/' + path if path else ''}.{f} type changed ({old_type} -> {new_type})",
                        )
                    )

    # new operations (paths present in new, absent from old)
    old_paths = set(old_spec.get("paths", {}).keys())
    new_paths = set(new_spec.get("paths", {}).keys())
    for p in sorted(new_paths - old_paths):
        problems.append(NeedsHuman("new_operation", f"new path: {p}"))

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


def class_uses_notrequired(info: ClassInfo) -> bool:
    for item in info.own_fields.values():
        seg = ast.get_source_segment(info.source, item.annotation) or ""
        if seg.startswith("NotRequired["):
            return True
    return False


def choose_field_annotation(info: ClassInfo, python_type: str, nullable: bool) -> str:
    if info.total_false:
        return f"Optional[{python_type}]" if nullable else python_type
    if class_uses_notrequired(info):
        inner = f"Optional[{python_type}]" if nullable else python_type
        return f"NotRequired[{inner}]"
    return f"Optional[{python_type}]"


def splice_typeddict_add_field(source: str, class_node: ast.ClassDef, field_name: str, annotation_text: str) -> str:
    lines = source.splitlines(keepends=True)
    last_stmt = class_node.body[-1]
    last_line_no = last_stmt.end_lineno
    last_line = lines[last_line_no - 1]
    indent = last_line[: len(last_line) - len(last_line.lstrip())]
    new_line = f"{indent}{field_name}: {annotation_text}\n"
    lines.insert(last_line_no, new_line)
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
        new_source = splice_typeddict_add_field(info.source, info.node, name, annotation)
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

    report = {
        "mode": "check",
        "map_errors": sorted(map_errors),
        "enum_gaps": [{"symbol": g.symbol, "file": g.file, "missing": g.missing} for g in enum_gaps],
        "property_gaps": [
            {"schema": g.schema_names, "path": g.path, "missing": sorted(g.missing.keys())} for g in prop_gaps
        ],
    }
    if report_path:
        report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    if not (map_errors or enum_gaps or prop_gaps):
        return 0

    if map_errors:
        print("spec-map.json validity -- FAILED:")
        for e in sorted(map_errors):
            print(f"  {e}")
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

    applied: list[AppliedChange] = []

    if not needs_human:
        for g in sorted(enum_gaps, key=lambda g: g.symbol):
            applied.append(apply_enum_change(g, index))
        # re-check property gaps against a fresh index is unnecessary: enum edits never touch TypedDicts
        for g in sorted(prop_gaps, key=lambda g: ("/".join(g.schema_names), g.path or "")):
            a, nh = apply_property_change(g, index)
            applied.extend(a)
            needs_human.extend(nh)

    bump: Optional[str] = None
    if not needs_human:
        if any(a.kind == "enum" for a in applied):
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--validate-map", action="store_true")
    mode.add_argument("--coverage", action="store_true")
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
    return 1


if __name__ == "__main__":
    sys.exit(main())
