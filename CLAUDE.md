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
    __init__.py                           # Public re-exports (types + clients + webhooks module)
    _version.py                           # __version__ (x-release-please-version marker; used in User-Agent)
    py.typed                              # PEP 561 marker (must stay inside the package)
    webhooks.py                           # Standalone Svix verifier: webhooks.verify / webhooks.construct_event
    webhook_events.py                     # GENERATED typed webhook payloads (.api-sync/gen_webhook_events.py)
    error_codes.py                        # GENERATED ErrorCode/RetryClass/ErrorCodeInfo (.api-sync/gen_error_codes.py)
    client.py                             # BlindPay (async) and BlindPaySync classes,
                                          #   ApiClientImpl / ApiClientImplSync (HTTP layer + retry loop),
                                          #   _*Namespace / _*NamespaceSync classes (sub-resources)
    types.py                              # Shared Literal types and TypedDicts used across resources
    _internal/
      api_client.py                       # Protocol interfaces: InternalApiClient, InternalApiClientSync,
                                          #   MultipartFile (get/post/put/patch/delete/post_multipart)
      http.py                             # RequestOptions, retry decision table, error mapping,
                                          #   path_param() and build_query() helpers, Redacted (a str whose
                                          #   repr hides the API key), strip_url_queries(). Pure, no I/O
      pagination.py                       # auto_paging_iter / async_auto_paging_iter (list_auto_paging)
      exceptions.py                       # BlindPayError, BlindPayApiError
    resources/
      __init__.py                         # Barrel re-exports of all create_*_resource factory functions
      <resource_name>/
        __init__.py                       # Barrel re-exports from the resource module(s)
        <resource_name>.py                # TypedDicts (input/output) + Resource classes (async+sync) + factory fns
  tests/
    conftest.py                           # Adds src/ to sys.path
    fixtures/spec/                        # Shared spec-shaped fixtures (all SDKs). Re-copy, never hand-edit
    fixtures/webhook-vectors.json         # Shared Svix verification vectors (14)
    fixtures/error-codes.json             # Shared error-code oracle (175 codes, status + retry class)
    spec_fixtures.py                      # Loads fixtures; assert_matches_spec(TypedDict, variants)
    http_mock.py                          # Wire-level seam: clients backed by httpx.MockTransport + Recorder
    test_webhooks.py                      # The 14 vectors through webhooks.verify and both client wrappers
    test_webhook_events.py                # construct_event + generated event types vs the webhook fixtures
    test_http.py                          # HTTP-layer behaviour shared by all resources
    test_retries.py                       # Retry table, idempotency keys, error shape (both clients)
    test_pagination.py                    # list envelopes and list_auto_paging (both clients)
    op_table.py                           # Every SDK method -> spec operation, minimal args, exact path
    test_operations.py                    # Options guard + op coverage, driven by op_table.py
    test_client_parity.py                 # Every resource method exists in both clients; namespaces are typed
    test_request_types.py                 # Request inputs' required keys vs the spec (via spec-map.json)
    test_packaging.py                     # py.typed placement, version single source, User-Agent
    test_error_codes.py                   # Generated ErrorCode/RetryClass vs fixtures/error-codes.json; generator
    test_review_reason.py                 # review_reason on the limit-increase GET and limitIncrease.* webhooks
    test_secret_hygiene.py                # No API key in client dumps, no query strings in transport errors
    test_union_arms.py                    # Every customer union arm vs CustomerOut (KNOWN_ARM_GAPS ledger)
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
- Docstrings on resource methods only where the signature can't say it: units, "exactly one of" inputs, a `None`
  result, the `/e/*` tracking endpoints' production 401, one-time settings.
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
from ..._internal.http import RequestOptions, path_param
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

    async def list(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[List{EntityName}Response]:
        return await self._client.get(f"/instances/{self._instance_id}/{api_path}", options=options)

    async def get(self, {id_param}: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[{EntityName}]:
        return await self._client.get(
            f"/instances/{self._instance_id}/{api_path}/{path_param({id_param})}", options=options
        )

    async def create(
        self, data: Create{EntityName}Input, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[Create{EntityName}Response]:
        return await self._client.post(f"/instances/{self._instance_id}/{api_path}", data, options=options)

    async def delete(self, {id_param}: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
        return await self._client.delete(
            f"/instances/{self._instance_id}/{api_path}/{path_param({id_param})}", options=options
        )


# --- Sync resource ---

class {EntityName}ResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def list(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[List{EntityName}Response]:
        return self._client.get(f"/instances/{self._instance_id}/{api_path}", options=options)

    def get(self, {id_param}: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[{EntityName}]:
        return self._client.get(
            f"/instances/{self._instance_id}/{api_path}/{path_param({id_param})}", options=options
        )

    def create(
        self, data: Create{EntityName}Input, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[Create{EntityName}Response]:
        return self._client.post(f"/instances/{self._instance_id}/{api_path}", data, options=options)

    def delete(self, {id_param}: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
        return self._client.delete(
            f"/instances/{self._instance_id}/{api_path}/{path_param({id_param})}", options=options
        )


# --- Factory functions ---

def create_{snake_name}_resource(instance_id: str, client: InternalApiClient) -> {EntityName}Resource:
    return {EntityName}Resource(instance_id, client)


def create_{snake_name}_resource_sync(instance_id: str, client: InternalApiClientSync) -> {EntityName}ResourceSync:
    return {EntityName}ResourceSync(instance_id, client)
```

Rules every method follows (enforced by `tests/test_operations.py` and `tests/test_client_parity.py`):
- Every method (GET included, and `post_multipart`) takes a trailing `options: Optional[RequestOptions] = None` and
  passes `options=options` to the client call. GETs use its `timeout` and `headers`; they never send an
  `Idempotency-Key`.
- Every caller-supplied path segment goes through `path_param(...)` inside the f-string (`a/b` -> `a%2Fb`).
  `self._instance_id` is client config and stays raw. Keep the path a literal f-string: api-sync reads it.
- Every query string comes from `build_query(params)` (drops `None`/`""`, booleans as `true`/`false`).
- Add the method to `tests/op_table.py` (operation, accessor, minimal call, exact path).

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

Export both the async and the sync factory (`create_{snake_name}_resource` and `create_{snake_name}_resource_sync`).

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
    field_a: str  # required by the spec
    field_b: NotRequired[Optional[str]]  # optional and nullable in the spec


class NewActionResponse(TypedDict):
    id: str
    status: Union[NewActionStatus, str]  # response enum: known values + str
```

### Step 2: Add the method to BOTH resource classes

**Async (in `{EntityName}Resource`):**
```python
async def new_action(
    self, entity_id: str, data: NewActionInput, options: Optional[RequestOptions] = None
) -> BlindpayApiResponse[NewActionResponse]:
    return await self._client.post(
        f"/instances/{self._instance_id}/{api_path}/{path_param(entity_id)}/action", data, options=options
    )
```

**Sync (in `{EntityName}ResourceSync`):**
```python
def new_action(
    self, entity_id: str, data: NewActionInput, options: Optional[RequestOptions] = None
) -> BlindpayApiResponse[NewActionResponse]:
    return self._client.post(
        f"/instances/{self._instance_id}/{api_path}/{path_param(entity_id)}/action", data, options=options
    )
```

### Step 3: Export from `__init__.py`

Add the new TypedDicts to both the import and `__all__` list in the resource's `__init__.py`.

### Step 4: Add tests for both async and sync

### Common method patterns

**GET with query params:**
```python
async def list(
    self, params: Optional[ListInput] = None, options: Optional[RequestOptions] = None
) -> BlindpayApiResponse[ListResponse]:
    query_string = build_query(params)
    return await self._client.get(f"/instances/{self._instance_id}/{path}{query_string}", options=options)
```

**Auto-pager** (for every list whose spec accepts `starting_after`). A plain `def` in BOTH classes, returning
`AsyncIterator[T]` (async class) or `Iterator[T]` (sync class), so bad params raise at the call:
```python
def list_auto_paging(self, params: Optional[ListInput] = None) -> AsyncIterator[Entity]:
    return async_auto_paging_iter(self.list, params)  # sync class: auto_paging_iter(self.list, params)
```

**POST with body:**
```python
async def create(self, data: CreateInput, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[CreateResponse]:
    return await self._client.post(f"/instances/{self._instance_id}/{path}", data, options=options)
```

**Method that extracts an ID from input to build the URL:**
```python
async def update(self, data: UpdateInput, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
    entity_id = data["entity_id"]
    payload = {k: v for k, v in data.items() if k != "entity_id"}
    return await self._client.put(
        f"/instances/{self._instance_id}/{path}/{path_param(entity_id)}", payload, options=options
    )
```

**GET with path param:**
```python
async def get(self, entity_id: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[Entity]:
    return await self._client.get(f"/instances/{self._instance_id}/{path}/{path_param(entity_id)}", options=options)
```

---

## 5. How to modify types

### Typing rules (checked against the spec)

`tests/test_operations.py::test_response_type_matches_every_fixture_variant` checks every method's response type
against every variant of its shared fixture, and `tests/test_request_types.py` checks inputs. The rules they enforce:

| Where | Spec says | Python annotation |
|---|---|---|
| Response field | not in `required` | `NotRequired[...]` |
| Response field | nullable | `Optional[...]` |
| Response field | string enum | `Union[<Literal alias>, str]` (known values, and new API values still type-check) |
| Request field | in `required` | required key (in a `total=False` class: `Required[...]`) |
| Request field | not in `required` | `NotRequired[...]` (or a `total=False` class) |
| Either | wire key is a Python keyword (`from`, `yield`) | declare it in a functional base: `_X = TypedDict("_X", {"from": ...})`, then `class X(_X)` |

Request enums stay closed Literals. Exception: the per-rail bank-account helpers and the two blockchain-wallet create
helpers require fields the merged spec schema marks optional, because the route validates each variant with its own
schema (`PER_VARIANT_HELPERS` in `tests/test_request_types.py`). Amount fields in cents are `int`; decimal fields
(quotations, whole-token amounts) are `float`. Input amount fields that were `float` before 4.1 are
`Union[int, float]` until the next major.

Every public name in a resource module must also be exported from `src/blindpay/__init__.py` (the "Resource types"
block) and from its package `__init__.py`; `tests/test_packaging.py` fails otherwise.

### Add a field to a TypedDict

Add the field following the typing rules above (`NotRequired`/`Optional`/`Union[Literal, str]` from the spec).

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

Sub-resources are accessed like `client.payins.quotes.create(...)`. The namespace class **subclasses** the parent
resource, so `client.payins.list()` keeps its real signature for type checkers (the old `__getattr__ -> Any`
delegation hid every method; `tests/test_client_parity.py` asserts the types with `assert_type`).

### Step 1: Create the sub-resource module

Add the sub-resource file inside the parent resource directory:
`src/blindpay/resources/{parent}/{sub_resource}.py`

Follow the same pattern as any resource file (types + async class + sync class + factory functions).

### Step 2: Update the parent `__init__.py`

Add imports from the new sub-resource module.

### Step 3: Create namespace classes in `client.py`

The parent resource classes are imported at module level in `client.py` (a subclass needs its base at runtime);
the sub-resources stay lazy:

```python
class _{ParentName}Namespace({ParentName}Resource):
    def __init__(self, instance_id: str, api_client: ApiClientImpl) -> None:
        super().__init__(instance_id, api_client)
        self._api = api_client

    @cached_property
    def {sub_resource}(self) -> "{SubResourceName}Resource":
        from blindpay.resources.{parent}.{sub_resource} import create_{sub_resource}_resource

        return create_{sub_resource}_resource(self._instance_id, self._api)
```

The sync twin is `_{ParentName}NamespaceSync({ParentName}ResourceSync)` with `ApiClientImplSync`.

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

The `_WalletsNamespace` has no base resource. It is purely a grouping:

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

Always pass `--python 3.13` to uv (otherwise uv may pick a newer interpreter and rewrite `uv.lock`):

```bash
uv run --python 3.13 pytest -q

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
- Response mocks come from the shared fixtures, never hand-written JSON: `response_variants("POST /v1/...")`
  from `tests/spec_fixtures.py`. Add `assert_matches_spec(ResponseType, variants)` for every response type you
  touch: it fails on fields the spec doesn't have, on required keys the spec makes optional, and on nullable
  fields not typed `Optional`. TypedDicts don't validate at runtime, so a round-tripped mock proves nothing.
- When the wire format matters (multipart, headers, query strings), use `tests/http_mock.py`
  (`async_client(recorder)` / `sync_client(recorder)`) and assert on the recorded `httpx.Request`.
- Mock return: `{"data": <expected_data>, "error": None}` for success.
- Assert: `response["error"] is None`, `response["data"] == expected`, `mock_request.assert_called_once_with(<METHOD>, <PATH>)`.
- For POST/PUT/PATCH methods, assert the body as well: `mock_request.assert_called_once_with("POST", "/path", {body_dict})`.

---

## 9. Versioning

The release runbook (what a merge triggers, secrets, re-running a stuck release, verifying PyPI) is
[RELEASING.md](RELEASING.md).

### release-please with conventional commits

The project uses [release-please](https://github.com/googleapis/release-please) for automated versioning.

**Config:** `release-please-config.json`
- Release type: `simple`, so release-please touches only the files listed in `extra-files` plus the changelog.
  The `python` type also rewrites `src/blindpay/__init__.py`, and in 4.0.0 it wrote back a stale copy that dropped
  every export.
- Tags are `vX.Y.Z` (`include-component-in-tag: false`). `publish.yaml` checks out that tag.
- Bumps `pyproject.toml` (toml updater, `$.project.version`), `uv.lock` (toml updater,
  `$.package[?(@.name.value=='blindpay')].version`: release-please's TOML parser wraps scalars, hence `.value`) and
  `src/blindpay/_version.py` (Generic updater)

**Auto-merge:** `publish.yaml` merges the release PR itself. It first waits for the PR's checks to pass, then
refuses if the PR changes any line outside `CHANGELOG.md` other than a version line.

**Manifest:** `.release-please-manifest.json`
- Tracks the current version at the root path `.`

**The release version lives in four files that release-please moves together.** Never edit them by hand:
- `.release-please-manifest.json` -> `"."`
- `pyproject.toml` -> `[project].version`
- `src/blindpay/_version.py` -> `__version__`. Keep the `# x-release-please-version` marker on that line:
  the Generic updater only rewrites marked lines. `client.py` imports it for the `User-Agent` header.

- `uv.lock` -> the `blindpay` package's `version`. The release PR's auto-merge guard accepts it (a `version = ` line).

`tests/test_packaging.py` fails if they drift. Regenerate `uv.lock` with `uv lock --python 3.13` only when
dependencies change.

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

### Schema to TypedDict mapping

| OpenAPI schema concept | Python representation |
|---|---|
| Object schema | `class MyType(TypedDict)` |
| String property | `field: str` |
| Number property | `field: float` |
| Integer property | `field: int` |
| Boolean property | `field: bool` |
| Nullable property | `field: Optional[str]` |
| Property not in `required` (response) | `field: NotRequired[...]` |
| String enum | `MyEnum = Literal["a", "b", "c"]`; response fields use `Union[MyEnum, str]` |
| Array of objects | `List[MyType]` |
| Nested object | Separate TypedDict, referenced by name |
| Optional input field | `NotRequired[X]` (or a `total=False` TypedDict); `Optional[X]` only if null is a valid value |
| Paginated list response | `List{Name}Response` (`data` + `pagination`); the method returns `Union[List{Name}Response, List[Entity]]` when the API sends a bare array without pagination params |
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

### Request bodies

- JSON bodies go through `post`/`put`/`patch`/`delete`. httpx sets `Content-Type: application/json`; the clients
  have no client-wide `Content-Type` (it would override the multipart boundary).
- Multipart bodies (`POST /upload`, `POST /upload/analyze`) go through `post_multipart(path, data, files)`.
  api-sync treats `post_multipart` as a POST when it scans resource methods (`CLIENT_VERB_ALIASES` in
  `.api-sync/sync.py`), so keep the path a literal (f-)string as the first argument.
- Exception to the factory signature rule: `create_upload_resource(instance_id, client)` (and `_sync`, and the
  `UploadResource(Sync)` constructors) still accept the legacy `(client)`-only call. Those calls emit a
  `DeprecationWarning` and send no `?instance_id=`. Remove the shim in the next major.

### Webhooks

`blindpay.webhooks.verify(payload, headers, secret, *, tolerance=300, now=None)` is the one verifier (native
Svix algorithm, `hmac` + `hashlib`, no `svix` dependency). It never raises. The clients'
`verify_webhook_signature` methods delegate to it; don't duplicate the algorithm.
`webhooks.construct_event(...)` (root alias `construct_webhook_event`) verifies, then returns the parsed body typed
as `WebhookEvent`.

`src/blindpay/webhook_events.py` is generated; never edit it by hand. Regenerate it from the spec and check it:

```bash
python3 .api-sync/gen_webhook_events.py --spec .api-sync/spec-snapshot.json          # write
python3 .api-sync/gen_webhook_events.py --spec .api-sync/spec-snapshot.json --check  # CI gate
```

Nested types are named `{Event}WebhookEvent{Property}`, enums are typed `str`, and provider-named fields
(`circle_*`, `checkbook_*`, `onemoney_*`, `aiprise_*`, `infinitus_*`, `jpm_*`) are skipped (provider names stay out of the public SDK surface).
`check_contract.py` skips this module (`GENERATED_FILES`).

### HTTP layer and retries

`_internal/http.py` holds every transport rule as pure functions shared by both clients: the retry decision table
(GETs retry on connection errors/408/429/5xx; mutations only without a response, on 429 and on
409 `idempotency_key_in_flight`, never on 5xx), auto idempotency keys (UUIDv4 before the first attempt for every
non-multipart mutation when `max_retries > 0`), and the `ErrorResponse` mapping. The clients only run the loop:
`time.sleep` in `ApiClientImplSync`, `asyncio.sleep` in `ApiClientImpl` (`_sleep` is the test seam). Never retry a
mutation on 5xx: the API releases the idempotency key, so a retry re-executes it.

### Deprecations

Mark methods that can't work (e.g. routes that don't exist) with `@typing_extensions.deprecated("...")` instead
of removing them outside a major release. Tests call them inside `pytest.warns(DeprecationWarning)`.

### api-sync ledgers

`.api-sync/allowlist.json` (SDK fields the spec snapshot doesn't know) and `.api-sync/unmodeled.json` (spec
fields/enums the SDK doesn't model) must stay true. When a fix makes an entry false, delete it in the same commit.
Provider-named spec fields (`checkbook_*`, `onemoney_*`, `circle_*`, `aiprise_*`, `jpm_*`, ...) are never modelled:
record them in `unmodeled.json` with reason "provider-named field; pending blindpay-v2 decision".

`.api-sync/spec-snapshot.json` is the public spec at `blindpay-v2@7e49addd9` (94 SDK operations). CI gates:

```bash
python3 .api-sync/sync.py --validate-map
python3 .api-sync/sync.py --check [--spec <openapi.json>]   # state reconciliation (default: the snapshot)
python3 .api-sync/sync.py --coverage --spec .api-sync/spec-snapshot.json   # METHOD+path: every x-sdk op has a method
python3 .api-sync/gen_webhook_events.py --spec .api-sync/spec-snapshot.json --check
python3 .api-sync/gen_error_codes.py --spec .api-sync/spec-snapshot.json --check
python3 .api-sync/check_contract.py
```

`src/blindpay/error_codes.py` is generated from the snapshot's `Errors` tag table (`| `CODE` | status | retry |
description |`); never edit it by hand. The generator fails on an empty table, any unparseable row (listing them all), a duplicate code or
an unknown retry class. `ErrorResponse["code"]` stays a plain `str` (unknown codes still arrive); `retry_class` is
informational and never feeds the transport retry table in `_internal/http.py`. `tests/fixtures/error-codes.json` is
the cross-SDK oracle `tests/test_error_codes.py` compares against.

`--apply` reports `bump=minor` for any applied change (each one adds an enum member, an optional field or an
operation). When it applies nothing but the delivered spec differs (an error-code row, a webhook-only field), it still
refreshes the snapshot, and `api-sync.yml` counts generator-only diffs (`webhook_events.py`, `error_codes.py`) as a
minor change, so they open a PR instead of being dropped.

Operations marked `x-sdk: false` (yield, card payment, ToS passthrough, upload/extract, deposit simulators) must never
get a method; `--coverage` fails if one does. `--apply` generates enum members, simple fields and standard operations
(with `options` and `path_param`); anything it can't infer is NEEDS_HUMAN and blocks the whole apply.

---

## Checklist for any change

- [ ] Types defined in the resource file (not `types.py`) unless shared across resources
- [ ] BOTH async and sync classes updated with identical logic
- [ ] Factory functions (async + sync) present at bottom of resource file
- [ ] Resource `__init__.py` re-exports all public names
- [ ] `resources/__init__.py` imports factory functions
- [ ] `client.py` has TYPE_CHECKING import + `@cached_property` in BOTH client classes
- [ ] Tests cover both async and sync variants
- [ ] Response types touched are checked with `assert_matches_spec` against the shared fixtures
- [ ] `ruff format src/` and `ruff check src/` pass
