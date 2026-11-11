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
from typing import Any, Dict, FrozenSet, List, Literal, Union, cast, get_args, get_origin, get_type_hints

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


UNKNOWN_ENUM = "zz_unknown_value_from_future_api"


def _union_args(hint: Any) -> List[Any]:
    return list(get_args(hint)) if get_origin(hint) in (Union, types.UnionType) else [hint]


def value_errors(hint: Any, value: Any, path: str = "$") -> List[str]:
    """Static "decode": every mismatch between a type hint and a JSON value, recursively.

    TypedDicts: required keys present, ``None`` only where the hint is ``Optional``. Strings: a closed ``Literal``
    must contain the value, and ``zz_unknown_value_from_future_api`` (the ``unknown_enum`` variant) needs a hint
    that admits ``str`` (response enums must accept values added later).
    Numbers: a non-integral value needs ``float``. Unions pass if any arm does.
    """
    if hint is Any:
        return []
    arms = _union_args(hint)
    if len(arms) > 1:
        if value is None:
            return [] if type(None) in arms else [f"{path}: null but the type doesn't allow None"]
        results = [value_errors(arm, value, path) for arm in arms if arm is not type(None)]
        return min(results, key=len) if all(results) else []
    if value is None:
        return [f"{path}: null but the type doesn't allow None"]
    origin = get_origin(hint)
    if origin is Literal:
        if value in get_args(hint):
            return []
        if value == UNKNOWN_ENUM:
            return [f"{path}: closed Literal can't hold an unknown enum value (C7: admit str)"]
        return [f"{path}: {value!r} is not in {get_args(hint)}"]
    if is_typeddict(hint):
        if not isinstance(value, dict):
            return [f"{path}: expected an object for {hint.__name__}"]
        obj = cast(Dict[str, Any], value)
        errors: List[str] = []
        required: FrozenSet[str] = getattr(hint, "__required_keys__", frozenset())
        for key, field_hint in get_type_hints(hint).items():
            if key not in obj:
                if key in required:
                    errors.append(f"{path}.{key}: required by {hint.__name__} but absent")
                continue
            errors.extend(value_errors(field_hint, obj[key], f"{path}.{key}"))
        return errors
    if origin in (list, List):
        if not isinstance(value, list):
            return [f"{path}: expected a list"]
        (item_hint,) = get_args(hint) or (Any,)
        return [
            e for i, item in enumerate(cast(List[Any], value)) for e in value_errors(item_hint, item, f"{path}[{i}]")
        ]
    if origin in (dict, Dict):
        return [] if isinstance(value, dict) else [f"{path}: expected an object"]
    if hint is str:
        return [] if isinstance(value, str) else [f"{path}: expected str, got {type(value).__name__}"]
    if hint is bool:
        return [] if isinstance(value, bool) else [f"{path}: expected bool, got {type(value).__name__}"]
    if hint is int:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return [f"{path}: expected int, got {type(value).__name__}"]
        return [] if float(value).is_integer() else [f"{path}: {value} is not an integer (decimal field typed int)"]
    if hint is float:
        ok = isinstance(value, (int, float)) and not isinstance(value, bool)
        return [] if ok else [f"{path}: expected float, got {type(value).__name__}"]
    return []


def declared_errors(typed_dict: Any, value: Any, path: str = "$") -> List[str]:
    """Keys a TypedDict declares that the spec's ``full`` variant doesn't have (misnamed or legacy fields)."""
    if not is_typeddict(typed_dict) or not isinstance(value, dict):
        return []
    return shape_errors(typed_dict, cast(Dict[str, Any], value), check_declared=True, check_required=False, path=path)


def variant_errors(hint: Any, variants: Dict[str, Any]) -> List[str]:
    """``value_errors`` for every variant, plus ``declared_errors`` on ``full``. List results pick the arm that
    matches each variant's shape (``{data, pagination}`` envelope or bare array)."""
    errors: List[str] = []
    for name, payload in sorted(variants.items()):
        errors.extend(f"[{name}] {e}" for e in value_errors(hint, payload))
        dict_arms = [arm for arm in _union_args(hint) if is_typeddict(arm)]
        if name.split(".")[0] == "full" and dict_arms and isinstance(payload, dict):
            best = min((declared_errors(arm, payload) for arm in dict_arms), key=len)
            errors.extend(f"[{name}] {e}" for e in best)
    return errors
