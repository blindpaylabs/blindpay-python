# CLAUDE.md -- blindpay-python SDK

This document is the authoritative reference for an AI agent modifying this codebase.
Read it fully before making any change.

---

## 1. Project structure

```
blindpay-python/
  pyproject.toml                          # Package metadata, deps, ruff/mypy config
  release-please-config.json              # release-please settings (Python type, v-tag)
  .release-please-manifest.json           # Current release-please version tracker
  src/blindpay/
    __init__.py                           # SDK version, public re-exports (types + clients)
    client.py                             # BlindPay (async) and BlindPaySync classes,
                                          #   ApiClientImpl / ApiClientImplSync (HTTP layer),
                                          #   _*Namespace / _*NamespaceSync classes (sub-resources)
    types.py                              # Shared Literal types and TypedDicts used across resources
    _internal/
      api_client.py                       # Protocol interfaces: InternalApiClient, InternalApiClientSync
      exceptions.py                       # BlindPayError exception class
    resources/
      __init__.py                         # Barrel re-exports of all create_*_resource factory functions
      <resource_name>/
        __init__.py                       # Barrel re-exports from the resource module(s)
        <resource_name>.py                # TypedDicts (input/output) + Resource classes (async+sync) + factory fns
  tests/
    conftest.py                           # Adds src/ to sys.path
    test_client.py                        # Tests for BlindPay / BlindPaySync (webhook verification)
    resources/
      test_<resource_name>.py             # Per-resource test files (async + sync test classes)
```

### Resource directory examples

Standard resource (no sub-resources):
```
resources/payouts/
  __init__.py       # re-exports from payouts.py
  payouts.py        # types + PayoutsResource + PayoutsResourceSync + factory fns
```

Resource with sub-resources (e.g. payins has quotes):
```
resources/payins/
  __init__.py       # re-exports from BOTH payins.py and quotes.py
  payins.py         # types + PayinsResource + PayinsResourceSync + factory fns
  quotes.py         # types + PayinQuotesResource + PayinQuotesResourceSync + factory fns
```

Multi-module namespace (wallets -- no _base, purely a grouping):
```
resources/wallets/
  __init__.py       # re-exports from blockchain.py and offramp.py
  blockchain.py     # BlockchainWalletsResource + BlockchainWalletsResourceSync + factory fns
  offramp.py        # OfframpWalletsResource + OfframpWalletsResourceSync + factory fns
resources/custodial_wallets/
  __init__.py
  custodial_wallets.py  # CustodialWalletsResource + CustodialWalletsResourceSync + factory fns
```

---

## 2. Conventions

### Naming

| Concept | Convention | Example |
|---|---|---|
| Resource class (async) | `{Name}Resource` | `PayinsResource` |
| Resource class (sync) | `{Name}ResourceSync` | `PayinsResourceSync` |
| Factory function (async) | `create_{snake_name}_resource` | `create_payins_resource` |
| Factory function (sync) | `create_{snake_name}_resource_sync` | `create_payins_resource_sync` |
| Input TypedDict | `{ActionName}Input` | `CreatePayinQuoteInput` |
| Output TypedDict | `{ActionName}Response` | `CreatePayinQuoteResponse` |
| Entity TypedDict | `{EntityName}` (no suffix) | `Payout`, `Payin`, `BlockchainWallet` |
| List response | `List{Name}Response` (TypedDict with `data` + `pagination`) | `ListPayoutsResponse` |
| Literal type | `PascalCase` | `TransactionStatus`, `Network` |
| Client namespace (async) | `_{Name}Namespace` | `_PayinsNamespace` |
| Client namespace (sync) | `_{Name}NamespaceSync` | `_PayinsNamespaceSync` |

### Code style

- Line length: 120 (ruff config).
- Formatter: ruff format. Linter: ruff lint. Type checker: mypy (strict) + pyright.
- Ruff lint rules: `["I","B","E","F","ARG","T201","T203"]`, ignore `["B006"]`.
- All TypedDicts come from `typing_extensions.TypedDict` (NOT `typing.TypedDict`). Exception: some resource files use `typing.TypedDict` -- follow whichever the file already uses, but prefer `typing_extensions`.
- Use `Optional[X]` from `typing`, not `X | None`.
- Use `List[X]` from `typing`, not `list[X]`.
- Use `Literal[...]` from `typing_extensions` for resource-local literals, or from `typing` if already imported.
- No docstrings on resource methods (the verify_webhook_signature method is an exception).
- All methods return `BlindpayApiResponse[T]` where T is the response TypedDict.
- Double quotes for strings.
- Imports: standard library first, then third-party, then relative. Sorted by ruff isort.
- No trailing commas after the last parameter in function signatures that fit on one line.
- Factory functions are always at the bottom of the resource file.

### Imports inside resource files

```python
from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse, <other shared types>
```

Resource-specific Literal types and TypedDicts are defined in the same file as the resource class, NOT in `types.py`. Only truly shared types (used across multiple resources) go in `types.py`.

### Imports in client.py

- Resource types are imported inside `TYPE_CHECKING` blocks only (lazy imports).
- Actual imports happen inside `@cached_property` methods using inline `from` statements.
- The `TYPE_CHECKING` import uses absolute paths: `from blindpay.resources.<name>.<name> import ...`.

---

## 3. How to add a new resource

### Step 1: Create the resource directory and files

Create `src/blindpay/resources/{resource_name}/` with two files:

**`__init__.py`**:
```python
from .{resource_name} import (
    {EntityName},
    {EntityName}Resource,
    {EntityName}ResourceSync,
    # ... all TypedDicts ...
    create_{snake_name}_resource,
    create_{snake_name}_resource_sync,
)

__all__ = [
    "create_{snake_name}_resource",
    "create_{snake_name}_resource_sync",
    "{EntityName}Resource",
    "{EntityName}ResourceSync",
    # ... all TypedDicts ...
]
```

**`{resource_name}.py`** (example for an instance-scoped resource):
```python
from typing import List, Optional

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse


class {EntityName}(TypedDict):
    id: str
    instance_id: str
    # ... fields ...
    created_at: str
    updated_at: str


class Create{EntityName}Input(TypedDict):
    # ... fields ...
    pass


class Create{EntityName}Response(TypedDict):
    id: str


class List{EntityName}Response(TypedDict):
    data: List[{EntityName}]


# --- Async resource ---

class {EntityName}Resource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def list(self) -> BlindpayApiResponse[List{EntityName}Response]:
        return await self._client.get(f"/instances/{self._instance_id}/{api_path}")

    async def get(self, {id_param}: str) -> BlindpayApiResponse[{EntityName}]:
        return await self._client.get(f"/instances/{self._instance_id}/{api_path}/{{{id_param}}}")

    async def create(self, data: Create{EntityName}Input) -> BlindpayApiResponse[Create{EntityName}Response]:
        return await self._client.post(f"/instances/{self._instance_id}/{api_path}", data)

    async def delete(self, {id_param}: str) -> BlindpayApiResponse[None]:
        return await self._client.delete(f"/instances/{self._instance_id}/{api_path}/{{{id_param}}}")


# --- Sync resource ---

class {EntityName}ResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self) -> BlindpayApiResponse[List{EntityName}Response]:
        return self._client.get(f"/instances/{self._instance_id}/{api_path}")

    def get(self, {id_param}: str) -> BlindpayApiResponse[{EntityName}]:
        return self._client.get(f"/instances/{self._instance_id}/{api_path}/{{{id_param}}}")

    def create(self, data: Create{EntityName}Input) -> BlindpayApiResponse[Create{EntityName}Response]:
        return self._client.post(f"/instances/{self._instance_id}/{api_path}", data)

    def delete(self, {id_param}: str) -> BlindpayApiResponse[None]:
        return self._client.delete(f"/instances/{self._instance_id}/{api_path}/{{{id_param}}}")


# --- Factory functions ---

def create_{snake_name}_resource(instance_id: str, client: InternalApiClient) -> {EntityName}Resource:
    return {EntityName}Resource(instance_id, client)


def create_{snake_name}_resource_sync(instance_id: str, client: InternalApiClientSync) -> {EntityName}ResourceSync:
    return {EntityName}ResourceSync(instance_id, client)
```

CRITICAL: The sync class is identical to the async class except:
- Methods are NOT `async def`, they are plain `def`.
- Method bodies do NOT use `await`.
- Constructor takes `InternalApiClientSync` instead of `InternalApiClient`.

For a resource that does NOT require `instance_id` (like `available`), omit `instance_id` from constructor and factory function, and do not prefix paths with `/instances/{self._instance_id}`.

### Step 2: Register in `resources/__init__.py`

Add the import and `__all__` entry:
```python
from .{resource_name} import create_{snake_name}_resource
```

Also add the sync factory if not already following the pattern (note: the barrel `__init__` only exports async factories currently; check existing pattern).

### Step 3: Wire into `client.py`

Add TYPE_CHECKING import at the top of client.py:
```python
if TYPE_CHECKING:
    from blindpay.resources.{resource_name}.{resource_name} import {EntityName}Resource, {EntityName}ResourceSync
```

Add `@cached_property` to BOTH `BlindPay` (async) and `BlindPaySync` classes:

**In `BlindPay`:**
```python
@cached_property
def {resource_name}(self) -> "{EntityName}Resource":
    from blindpay.resources.{resource_name} import create_{snake_name}_resource

    return create_{snake_name}_resource(self._instance_id, self._api)
```

**In `BlindPaySync`:**
```python
@cached_property
def {resource_name}(self) -> "{EntityName}ResourceSync":
    from blindpay.resources.{resource_name} import create_{snake_name}_resource_sync

    return create_{snake_name}_resource_sync(self._instance_id, self._api)
```

### Step 4: Add tests

Create `tests/resources/test_{resource_name}.py`:
```python
from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class Test{EntityName}:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_list(self):
        mocked_data = [{"id": "xxx_000000000000"}]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_data, "error": None}

            response = await self.blindpay.{resource_name}.list()

            assert response["error"] is None
            assert response["data"] == mocked_data
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/{api_path}")


class Test{EntityName}Sync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_list(self):
        mocked_data = [{"id": "xxx_000000000000"}]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_data, "error": None}

            response = self.blindpay.{resource_name}.list()

            assert response["error"] is None
            assert response["data"] == mocked_data
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/{api_path}")
```

Testing pattern:
- Async tests: class `Test{Name}`, use `@pytest.mark.asyncio` + `async def`, mock `self.blindpay._api._request`.
- Sync tests: class `Test{Name}Sync`, plain `def`, mock `self.blindpay._api._request`.
- Both patch `_request` on the `_api` object and assert the HTTP method + path.

---

## 4. How to add a method to an existing resource

### Step 1: Define input/output types in the resource file

Add TypedDicts above the resource classes in the same file:
```python
class NewActionInput(TypedDict):
    field_a: str
    field_b: Optional[str]


class NewActionResponse(TypedDict):
    id: str
    status: str
```

### Step 2: Add the method to BOTH resource classes

**Async (in `{EntityName}Resource`):**
```python
async def new_action(self, data: NewActionInput) -> BlindpayApiResponse[NewActionResponse]:
    return await self._client.post(f"/instances/{self._instance_id}/{api_path}/action", data)
```

**Sync (in `{EntityName}ResourceSync`):**
```python
def new_action(self, data: NewActionInput) -> BlindpayApiResponse[NewActionResponse]:
    return self._client.post(f"/instances/{self._instance_id}/{api_path}/action", data)
```

### Step 3: Export from `__init__.py`

Add the new TypedDicts to both the import and `__all__` list in the resource's `__init__.py`.

### Step 4: Add tests for both async and sync

### Common method patterns

**GET with query params:**
```python
async def list(self, params: Optional[ListInput] = None) -> BlindpayApiResponse[ListResponse]:
    query_string = ""
    if params:
        filtered_params = {k: v for k, v in params.items() if v is not None}
        if filtered_params:
            query_string = f"?{urlencode(filtered_params)}"
    return await self._client.get(f"/instances/{self._instance_id}/{path}{query_string}")
```

**POST with body:**
```python
async def create(self, data: CreateInput) -> BlindpayApiResponse[CreateResponse]:
    return await self._client.post(f"/instances/{self._instance_id}/{path}", data)
```

**Method that extracts an ID from input to build the URL:**
```python
async def update(self, data: UpdateInput) -> BlindpayApiResponse[None]:
    entity_id = data["entity_id"]
    payload = {k: v for k, v in data.items() if k != "entity_id"}
    return await self._client.put(f"/instances/{self._instance_id}/{path}/{entity_id}", payload)
```

**GET with path param:**
```python
async def get(self, entity_id: str) -> BlindpayApiResponse[Entity]:
    return await self._client.get(f"/instances/{self._instance_id}/{path}/{entity_id}")
```

---

## 5. How to modify types

### Add a field to a TypedDict

Simply add the new field. Use `Optional[X]` if the field can be null in API responses.

```python
class Payout(TypedDict):
    # ... existing fields ...
    new_field: str                # required, always present
    another_field: Optional[str]  # nullable
```

### Remove a field from a TypedDict

Delete the line. Search the codebase for any code that references the removed field (e.g., `data["removed_field"]`).

### Rename a field

1. Change the field name in the TypedDict.
2. Search for all references to the old name across the codebase.
3. If the API uses a different name than the Python field (e.g., `from` is reserved), use a renamed field and convert in the method body. See `quotes.py` for the `from_currency` -> `from` pattern.

### Add a new shared Literal type

Add to `src/blindpay/types.py`:
```python
NewType = Literal["value_a", "value_b", "value_c"]
```

Then export from `src/blindpay/__init__.py`: add to both the import block and the `__all__` list.

### Add a resource-local Literal type

Define it at the top of the resource file, after imports:
```python
LocalType = Literal["option_a", "option_b"]
```

---

## 6. How to remove a resource

1. Delete the `src/blindpay/resources/{resource_name}/` directory.
2. Remove the import and `__all__` entry from `src/blindpay/resources/__init__.py`.
3. Remove the `TYPE_CHECKING` import from `client.py`.
4. Remove the `@cached_property` from BOTH `BlindPay` and `BlindPaySync` in `client.py`.
5. If the resource was part of a namespace, also remove the `@cached_property` from the corresponding `_*Namespace` and `_*NamespaceSync` classes.
6. Remove any re-exports from `src/blindpay/__init__.py` if applicable.
7. Delete `tests/resources/test_{resource_name}.py`.

---

## 7. How to add a sub-resource (namespace pattern)

Sub-resources are accessed like `client.payins.quotes.create(...)`. This uses a namespace class with `__getattr__` delegation.

### Step 1: Create the sub-resource module

Add the sub-resource file inside the parent resource directory:
`src/blindpay/resources/{parent}/{sub_resource}.py`

Follow the same pattern as any resource file (types + async class + sync class + factory functions).

### Step 2: Update the parent `__init__.py`

Add imports from the new sub-resource module.

### Step 3: Create namespace classes in `client.py`

**Async namespace:**
```python
class _{ParentName}Namespace:
    def __init__(self, instance_id: str, api_client: ApiClientImpl) -> None:
        self._instance_id = instance_id
        self._api = api_client

    @cached_property
    def _base(self) -> "{ParentName}Resource":
        from blindpay.resources.{parent}.{parent} import create_{parent}_resource

        return create_{parent}_resource(self._instance_id, self._api)

    @cached_property
    def {sub_resource}(self) -> "{SubResourceName}Resource":
        from blindpay.resources.{parent}.{sub_resource} import create_{sub_resource}_resource

        return create_{sub_resource}_resource(self._instance_id, self._api)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base, name)
```

**Sync namespace:**
```python
class _{ParentName}NamespaceSync:
    def __init__(self, instance_id: str, api_client: ApiClientImplSync) -> None:
        self._instance_id = instance_id
        self._api = api_client

    @cached_property
    def _base(self) -> "{ParentName}ResourceSync":
        from blindpay.resources.{parent}.{parent} import create_{parent}_resource_sync

        return create_{parent}_resource_sync(self._instance_id, self._api)

    @cached_property
    def {sub_resource}(self) -> "{SubResourceName}ResourceSync":
        from blindpay.resources.{parent}.{sub_resource} import create_{sub_resource}_resource_sync

        return create_{sub_resource}_resource_sync(self._instance_id, self._api)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base, name)
```

The `__getattr__` method delegates unknown attribute access to `_base`, so `client.payins.list()` works -- it forwards to `PayinsResource.list()`. Meanwhile `client.payins.quotes.create()` hits the explicit `quotes` cached_property.

### Step 4: Update the client class

Change the `@cached_property` return type from the resource to the namespace:

```python
@cached_property
def {parent}(self) -> _{ParentName}Namespace:
    return _{ParentName}Namespace(self._instance_id, self._api)
```

Do the same in the sync client with `_{ParentName}NamespaceSync`.

### Step 5: Add TYPE_CHECKING imports

Add the sub-resource types to the `TYPE_CHECKING` block in `client.py`.

### Namespace without a base resource (wallets pattern)

The `_WalletsNamespace` has no `_base` and no `__getattr__`. It is purely a grouping:

```python
class _WalletsNamespace:
    def __init__(self, instance_id: str, api_client: ApiClientImpl) -> None:
        self._instance_id = instance_id
        self._api = api_client

    @cached_property
    def blockchain(self) -> "BlockchainWalletsResource":
        from blindpay.resources.wallets.blockchain import create_blockchain_wallets_resource

        return create_blockchain_wallets_resource(self._instance_id, self._api)

    @cached_property
    def offramp(self) -> "OfframpWalletsResource":
        from blindpay.resources.wallets.offramp import create_offramp_wallets_resource

        return create_offramp_wallets_resource(self._instance_id, self._api)

    @cached_property
    def custodial(self) -> "CustodialWalletsResource":
        from blindpay.resources.custodial_wallets.custodial_wallets import create_custodial_wallets_resource

        return create_custodial_wallets_resource(self._instance_id, self._api)
```

Note: `custodial` imports from `custodial_wallets` package (not from `wallets/`). Use this pattern when the parent is not itself an API resource, only a namespace.

---

## 8. Testing

### Run tests

```bash
# All tests
pytest tests/ -v

# Specific resource
pytest tests/resources/test_payins.py -v

# Only async tests
pytest tests/ -v -k "not Sync"

# Only sync tests
pytest tests/ -v -k "Sync"
```

### Linting and type checking

```bash
# Format
ruff format src/

# Lint
ruff check src/

# Lint with auto-fix
ruff check src/ --fix

# Type check
mypy src/blindpay/
pyright src/blindpay/
```

### Test file pattern

- One test file per resource: `tests/resources/test_{resource_name}.py`.
- Two classes per file: `Test{Name}` (async) and `Test{Name}Sync` (sync).
- Each class has `@pytest.fixture(autouse=True) def setup(self)` that creates the client.
- Async class uses `BlindPay`, sync class uses `BlindPaySync`.
- Mock target: `patch.object(self.blindpay._api, "_request")`.
- Mock return: `{"data": <expected_data>, "error": None}` for success.
- Assert: `response["error"] is None`, `response["data"] == expected`, `mock_request.assert_called_once_with(<METHOD>, <PATH>)`.
- For POST/PUT/PATCH methods, assert the body as well: `mock_request.assert_called_once_with("POST", "/path", {body_dict})`.

---

## 9. Versioning

### release-please with conventional commits

The project uses [release-please](https://github.com/googleapis/release-please) for automated versioning.

**Config:** `release-please-config.json`
- Release type: `python`
- Tags include `v` prefix (e.g., `v1.3.0`)
- Bumps version in `src/blindpay/__init__.py` (via `extra-files`)

**Manifest:** `.release-please-manifest.json`
- Tracks the current version at the root path `.`

**Version is stored in TWO places** (keep them in sync for local dev, release-please handles it in CI):
- `pyproject.toml` -> `[project].version`
- `src/blindpay/__init__.py` -> `__version__`
- `src/blindpay/client.py` -> `__version__` (duplicated, used in User-Agent header)

### Commit message format

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add invoices resource
feat(payouts): add submit_documents method
fix(types): correct Currency literal values
chore: update dependencies
docs: update README examples
refactor(client): simplify namespace initialization
```

- `feat:` triggers a MINOR version bump.
- `fix:` triggers a PATCH version bump.
- `feat!:` or `BREAKING CHANGE:` in the footer triggers a MAJOR bump.

---

## 10. OpenAPI to SDK mapping rules

### Path to resource mapping

| API path pattern | SDK access pattern | Resource location |
|---|---|---|
| `/available/*` | `client.available.method()` | `resources/available/available.py` |
| `/instances/{id}/{resource}` | `client.{resource}.method()` | `resources/{resource}/{resource}.py` |
| `/instances/{id}/{resource}/{rid}/sub` | `client.{resource}.method(data)` where data contains `{rid}` | Same resource file, ID extracted from input |
| `/instances/{id}/payin-quotes` | `client.payins.quotes.method()` | `resources/payins/quotes.py` (sub-resource) |
| `/e/{resource}/{id}` | `client.{resource}.get_track(id)` | Same resource file (external tracking endpoint) |

### HTTP method to class method mapping

| HTTP method | SDK method name | Notes |
|---|---|---|
| `GET /resources` | `list()` | Optional params TypedDict, builds query string |
| `GET /resources/{id}` | `get(id)` | Takes ID as string param |
| `POST /resources` | `create(data)` | Takes input TypedDict |
| `PUT /resources/{id}` | `update(data)` | ID extracted from TypedDict, excluded from payload |
| `PATCH /resources/{id}` | `update(data)` | Same as PUT |
| `DELETE /resources/{id}` | `delete(id)` | Takes ID as string param |
| `POST /resources/{id}/action` | `action_name(data)` | Descriptive method name |
| `GET /export/resources` | `export(params)` | Query string params |

### Schema to TypedDict mapping

| OpenAPI schema concept | Python representation |
|---|---|
| Object schema | `class MyType(TypedDict)` |
| String property | `field: str` |
| Number property | `field: float` |
| Integer property | `field: int` |
| Boolean property | `field: bool` |
| Nullable property | `field: Optional[str]` |
| String enum | `MyEnum = Literal["a", "b", "c"]` |
| Array of objects | `List[MyType]` |
| Nested object | Separate TypedDict, referenced by name |
| Optional input field | Use `total=False` on the TypedDict or `Optional[X]` per field |
| Paginated list response | TypedDict with `data: List[Entity]` + `pagination: PaginationMetadata` |
| Request body | `{Action}Input(TypedDict)` |
| Response body | `{Action}Response(TypedDict)` |

### API path parameter handling in methods

When a method needs to extract an ID from the input to build a URL path:
```python
async def action(self, data: ActionInput) -> BlindpayApiResponse[ActionResponse]:
    entity_id = data["entity_id"]
    payload = {k: v for k, v in data.items() if k != "entity_id"}
    return await self._client.post(f"/instances/{self._instance_id}/path/{entity_id}/action", payload)
```

When multiple IDs need extraction:
```python
async def action(self, data: ActionInput) -> BlindpayApiResponse[ActionResponse]:
    parent_id = data["parent_id"]
    child_id = data["child_id"]
    payload = {k: v for k, v in data.items() if k not in ["parent_id", "child_id"]}
    return await self._client.post(f"/instances/{self._instance_id}/parents/{parent_id}/children/{child_id}", payload)
```

### Python reserved word handling

If an API field name clashes with a Python keyword, rename the field and convert in the method body:
```python
# In TypedDict: use suffixed name
class MyInput(TypedDict):
    from_currency: Currency  # API field is "from"

# In method: convert back
async def method(self, data: MyInput) -> BlindpayApiResponse[MyResponse]:
    payload = {
        "from": data["from_currency"],
        "to": data["to"],
    }
    return await self._client.post(f"/path", payload)
```

---

## Checklist for any change

- [ ] Types defined in the resource file (not `types.py`) unless shared across resources
- [ ] BOTH async and sync classes updated with identical logic
- [ ] Factory functions (async + sync) present at bottom of resource file
- [ ] Resource `__init__.py` re-exports all public names
- [ ] `resources/__init__.py` imports factory functions
- [ ] `client.py` has TYPE_CHECKING import + `@cached_property` in BOTH client classes
- [ ] Tests cover both async and sync variants
- [ ] `ruff format src/` and `ruff check src/` pass
