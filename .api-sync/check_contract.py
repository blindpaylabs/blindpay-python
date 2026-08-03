#!/usr/bin/env python3
"""Wire-contract check: compares SDK-declared field/enum names against the API spec snapshot.

Run locally with:
    python3 .api-sync/check_contract.py

No third-party dependencies. Two checks:

Direction A (hard failure): every TypedDict field name declared anywhere under src/blindpay
must exist as a property name somewhere in the spec snapshot, unless the (ClassName, field)
pair is listed in allowlist.json.

Direction B (webhook events, hard failure): every event name in the spec's webhook event
enum must be present in the SDK's WebhookEvents literal. Fields in the spec the SDK simply
doesn't model are reported as a warning only (this direction is not exhaustive for other
enums -- webhook events is the one explicitly mapped).
"""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_PATH = Path(__file__).resolve().parent / "spec-snapshot.json"
ALLOWLIST_PATH = Path(__file__).resolve().parent / "allowlist.json"
SRC_ROOT = ROOT / "src" / "blindpay"
WEBHOOKS_FILE = SRC_ROOT / "resources" / "webhooks" / "webhooks.py"
WEBHOOKS_LITERAL_NAME = "WebhookEvents"

REQUIRED_ALLOWLIST_KEYS = {"schema", "field", "reason", "owner"}


def load_snapshot() -> dict:
    with SNAPSHOT_PATH.open() as f:
        return json.load(f)


def load_allowlist() -> list[dict]:
    if not ALLOWLIST_PATH.exists():
        return []
    with ALLOWLIST_PATH.open() as f:
        entries = json.load(f)
    if not isinstance(entries, list):
        raise SystemExit(f"{ALLOWLIST_PATH}: expected a JSON array of entries")
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise SystemExit(f"{ALLOWLIST_PATH}[{i}]: entry must be an object")
        missing = REQUIRED_ALLOWLIST_KEYS - entry.keys()
        if missing:
            raise SystemExit(f"{ALLOWLIST_PATH}[{i}]: missing required key(s) {sorted(missing)}")
        extra = entry.keys() - REQUIRED_ALLOWLIST_KEYS
        if extra:
            raise SystemExit(f"{ALLOWLIST_PATH}[{i}]: unexpected key(s) {sorted(extra)}")
        for key in REQUIRED_ALLOWLIST_KEYS:
            if not isinstance(entry[key], str) or not entry[key].strip():
                raise SystemExit(f"{ALLOWLIST_PATH}[{i}].{key}: must be a non-empty string")
    return entries


def collect_known_property_names(spec: dict) -> set[str]:
    """Every key that appears as an object schema's property name, anywhere in the
    document (components.schemas AND inline path request/response schemas)."""
    names: set[str] = set()

    def walk(node: object) -> None:
        if isinstance(node, dict):
            props = node.get("properties")
            if isinstance(props, dict):
                names.update(props.keys())
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(spec)
    return names


def collect_param_names(spec: dict) -> set[str]:
    """Every query/path parameter name declared on any operation."""
    names: set[str] = set()
    for path_item in spec.get("paths", {}).values():
        if not isinstance(path_item, dict):
            continue
        for op in path_item.values():
            if not isinstance(op, dict):
                continue
            for param in op.get("parameters", []):
                if isinstance(param, dict) and isinstance(param.get("name"), str):
                    names.add(param["name"])
    return names


def find_typeddict_fields(src_root: Path) -> dict[tuple[str, str], set[str]]:
    """Maps (relative_file, class_name) -> set of declared field names, for every
    class that is (transitively) a TypedDict subclass."""
    py_files = sorted(src_root.rglob("*.py"))
    trees: dict[Path, ast.Module] = {}
    for f in py_files:
        try:
            trees[f] = ast.parse(f.read_text(), filename=str(f))
        except SyntaxError as e:
            raise SystemExit(f"{f}: failed to parse: {e}") from e

    known_typeddict_classes = {"TypedDict"}
    # Fixed-point: a class based on a class we already know is a TypedDict is also one.
    for _ in range(5):
        changed = False
        for tree in trees.values():
            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue
                base_names = [b.id for b in node.bases if isinstance(b, ast.Name)]
                base_names += [b.attr for b in node.bases if isinstance(b, ast.Attribute)]
                if node.name in known_typeddict_classes:
                    continue
                if any(b in known_typeddict_classes for b in base_names):
                    known_typeddict_classes.add(node.name)
                    changed = True
        if not changed:
            break

    results: dict[tuple[str, str], set[str]] = {}
    for f, tree in trees.items():
        rel = str(f.relative_to(src_root))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name in known_typeddict_classes:
                fields = set()
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        fields.add(item.target.id)
                if fields:
                    results[(rel, node.name)] = fields
    return results


def find_literal_string_values(file_path: Path, literal_name: str) -> set[str]:
    tree = ast.parse(file_path.read_text(), filename=str(file_path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == literal_name for t in node.targets):
            values = set()
            for const in ast.walk(node.value):
                if isinstance(const, ast.Constant) and isinstance(const.value, str):
                    values.add(const.value)
            return values
    raise SystemExit(f"{file_path}: could not find `{literal_name} = Literal[...]`")


def find_spec_webhook_events(spec: dict) -> set[str]:
    schemas = spec.get("components", {}).get("schemas", {})
    for name in ("WebhookEndpointIn", "WebhookEndpoint", "WebhookEndpointOut"):
        schema = schemas.get(name)
        if not schema:
            continue
        events = schema.get("properties", {}).get("events")
        if not events:
            continue
        enum = events.get("items", {}).get("enum")
        if enum:
            return set(enum)
    raise SystemExit("could not locate the webhook events enum in the spec snapshot")


def main() -> int:
    spec = load_snapshot()
    allowlist = load_allowlist()
    allowset = {(e["schema"], e["field"]) for e in allowlist}

    known = collect_known_property_names(spec) | collect_param_names(spec)
    typeddict_fields = find_typeddict_fields(SRC_ROOT)

    failures: list[str] = []
    for (rel_file, class_name), fields in typeddict_fields.items():
        for field in sorted(fields):
            if field in known:
                continue
            if (class_name, field) in allowset:
                continue
            failures.append(f"  {rel_file}:{class_name}.{field}")

    unused_allowlist = sorted(allowset - {(c, f) for (_, c), fields in typeddict_fields.items() for f in fields})

    sdk_events = find_literal_string_values(WEBHOOKS_FILE, WEBHOOKS_LITERAL_NAME)
    spec_events = find_spec_webhook_events(spec)
    missing_events = sorted(spec_events - sdk_events)

    ok = True

    print(
        f"Checked {sum(len(f) for f in typeddict_fields.values())} declared TypedDict fields "
        f"across {len(typeddict_fields)} classes against {len(known)} known wire keys."
    )

    if failures:
        ok = False
        print(
            f"\nDirection A -- FAILED: {len(failures)} field(s) declared by the SDK do not "
            f"exist anywhere in the spec snapshot:"
        )
        print("\n".join(failures))
        print(
            "\nEach must be renamed to match the wire, or added to .api-sync/allowlist.json "
            "with a reason and owner if it is a genuine, pre-existing divergence unrelated "
            "to the change you're making."
        )

    if missing_events:
        ok = False
        print(
            f"\nDirection B (webhook events) -- FAILED: the spec defines event(s) the SDK's "
            f"WebhookEvents literal is missing: {missing_events}"
        )

    extra_sdk_events = sorted(sdk_events - spec_events)
    if extra_sdk_events:
        print(
            f"\nNote: SDK's WebhookEvents literal has event(s) not present in the spec's enum "
            f"(likely deprecated events that stopped firing): {extra_sdk_events}"
        )

    if unused_allowlist:
        print(
            f"\nWarning: allowlist.json has {len(unused_allowlist)} entrie(s) that don't match "
            f"any current SDK field -- consider pruning: {unused_allowlist}"
        )

    sdk_declared_fields = {f for fields in typeddict_fields.values() for f in fields}
    schema_only_known = collect_known_property_names(spec)
    unmodeled = schema_only_known - sdk_declared_fields
    if unmodeled:
        print(
            f"\nDirection B (fields) -- warning only: {len(unmodeled)} spec property name(s) "
            f"are not declared by any SDK TypedDict. Not a failure; the SDK is allowed to "
            f"model a subset of the API."
        )

    if ok:
        print("\nDirection A and B: PASSED.")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
