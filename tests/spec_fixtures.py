"""Helpers for the shared spec-shaped fixtures in ``tests/fixtures/spec``.

The fixtures are generated from the public OpenAPI spec (see ``tests/fixtures/spec/README.md``) and
are shared by every BlindPay SDK. Copy them again from the parity reference set instead of editing.

TypedDicts don't validate at runtime, so "decoding" a fixture proves nothing on its own. These
helpers check a TypedDict's annotations against the fixture variants instead:

- every key the SDK declares exists in the ``full`` variant (catches misnamed or legacy fields);
- every key the SDK marks required is present in ``required_only`` (catches over-required fields);
- every key that is ``null`` in ``nullables_null`` is annotated ``Optional`` (catches non-nullable types).
"""

import json
import types
from pathlib import Path
from typing import Any, Dict, FrozenSet, List, Union, cast, get_args, get_origin, get_type_hints

from typing_extensions import is_typeddict

FIXTURES_DIR = Path(__file__).parent / "fixtures"
SPEC_DIR = FIXTURES_DIR / "spec"


def load_index() -> Dict[str, Any]:
    return cast(Dict[str, Any], json.loads((SPEC_DIR / "index.json").read_text()))


def response_variants(operation: str, status: str = "200") -> Dict[str, Any]:
    """Variants for ``operation`` (e.g. ``"GET /v1/instances/{instance_id}/payouts"``)."""
    entry = load_index()["operations"][operation]
    file_name = entry if isinstance(entry, str) else entry["file"]
    document = json.loads((SPEC_DIR / file_name).read_text())
    return cast(Dict[str, Any], document["responses"][status]["variants"])


def load_webhook_vectors() -> List[Dict[str, Any]]:
    document = json.loads((FIXTURES_DIR / "webhook-vectors.json").read_text())
    return cast(List[Dict[str, Any]], document["vectors"])


def _is_optional(hint: Any) -> bool:
    return get_origin(hint) in (Union, types.UnionType) and type(None) in get_args(hint)


def _nested_typeddicts(hint: Any) -> List[Any]:
    if is_typeddict(hint):
        return [hint]
    found: List[Any] = []
    for arg in get_args(hint):
        found.extend(_nested_typeddicts(arg))
    return found


def _nested_values(value: Any) -> List[Dict[str, Any]]:
    if isinstance(value, dict):
        return [cast(Dict[str, Any], value)]
    if isinstance(value, list):
        items = cast(List[Any], value)
        return [cast(Dict[str, Any], item) for item in items if isinstance(item, dict)]
    return []


def shape_errors(
    typed_dict: Any,
    value: Dict[str, Any],
    *,
    check_declared: bool = False,
    check_required: bool = True,
    path: str = "$",
) -> List[str]:
    """Return every mismatch between ``typed_dict``'s annotations and ``value``, recursively."""
    errors: List[str] = []
    hints = get_type_hints(typed_dict)
    required: FrozenSet[str] = getattr(typed_dict, "__required_keys__", frozenset())
    for key, hint in hints.items():
        if key not in value:
            if check_declared:
                errors.append(f"{path}.{key}: declared by {typed_dict.__name__} but absent from the spec payload")
            elif check_required and key in required:
                errors.append(f"{path}.{key}: required by {typed_dict.__name__} but optional in the spec")
            continue
        item = value[key]
        if item is None:
            if not _is_optional(hint):
                errors.append(f"{path}.{key}: null in the spec but {typed_dict.__name__} doesn't allow None")
            continue
        for nested in _nested_typeddicts(hint):
            for nested_value in _nested_values(item):
                errors.extend(
                    shape_errors(
                        nested,
                        nested_value,
                        check_declared=check_declared,
                        check_required=check_required,
                        path=f"{path}.{key}",
                    )
                )
    return errors


def assert_matches_spec(typed_dict: Any, variants: Dict[str, Any], *, check_required: bool = True) -> None:
    """Check ``typed_dict`` against the ``full``, ``required_only`` and ``nullables_null`` variants."""
    errors = shape_errors(typed_dict, variants["full"], check_declared=True)
    errors += shape_errors(typed_dict, variants["required_only"], check_required=check_required)
    errors += shape_errors(typed_dict, variants["nullables_null"], check_required=check_required)
    assert not errors, "\n".join(errors)
