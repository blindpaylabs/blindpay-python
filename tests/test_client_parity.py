"""C12: every resource method exists in both clients with the same parameters."""

import inspect
from types import ModuleType
from typing import Dict, Iterator, List, Set, Tuple

import pytest

import blindpay.resources as resources_pkg
from blindpay.resources import (
    available,
    bank_accounts,
    custodial_wallets,
    customers,
    fees,
    instances,
    limits,
    ownership,
    partner_fees,
    payins,
    payouts,
    quotes,
    terms_of_service,
    transfers,
    upload,
    virtual_accounts,
    wallets,
    webhooks,
)

MODULES: List[ModuleType] = [
    available,
    bank_accounts,
    custodial_wallets,
    customers,
    fees,
    instances,
    limits,
    ownership,
    partner_fees,
    payins,
    payouts,
    quotes,
    terms_of_service,
    transfers,
    upload,
    virtual_accounts,
    wallets,
    webhooks,
]


Pair = Tuple[str, type, type]


def _resource_pairs() -> Iterator[Pair]:
    seen: Set[str] = set()
    for module in MODULES:
        for name, cls in vars(module).items():
            if not (inspect.isclass(cls) and name.endswith("Resource")) or name in seen:
                continue
            sync_cls = getattr(module, f"{name}Sync", None)
            assert sync_cls is not None, f"{name} has no {name}Sync twin"
            seen.add(name)
            yield name, cls, sync_cls


def _public_methods(cls: type) -> Dict[str, List[str]]:
    return {
        name: [p for p in inspect.signature(fn).parameters]
        for name, fn in inspect.getmembers(cls, inspect.isfunction)
        if not name.startswith("_")
    }


PAIRS: List[Pair] = list(_resource_pairs())


def test_every_resource_package_is_checked() -> None:
    assert {m.__name__.rsplit(".", 1)[-1] for m in MODULES} >= {
        n for n in dir(resources_pkg) if not n.startswith("_") and inspect.ismodule(getattr(resources_pkg, n))
    }


@pytest.mark.parametrize("name,async_cls,sync_cls", PAIRS, ids=[p[0] for p in PAIRS])
def test_sync_twin_has_the_same_methods_and_parameters(name: str, async_cls: type, sync_cls: type) -> None:
    assert name
    assert _public_methods(async_cls) == _public_methods(sync_cls)


@pytest.mark.parametrize("name,async_cls,sync_cls", PAIRS, ids=[p[0] for p in PAIRS])
def test_async_methods_are_coroutines(name: str, async_cls: type, sync_cls: type) -> None:
    for method, fn in inspect.getmembers(async_cls, inspect.isfunction):
        if method.startswith("_"):
            continue
        if method.endswith("auto_paging"):
            # Plain functions that validate params eagerly and return an (async) iterator.
            assert "AsyncIterator" in str(inspect.signature(fn).return_annotation)
            assert "AsyncIterator" not in str(inspect.signature(getattr(sync_cls, method)).return_annotation)
            continue
        # unwrap: older typing_extensions' @deprecated wrapper doesn't keep the coroutine-function marker
        assert inspect.iscoroutinefunction(inspect.unwrap(fn)), f"{name}.{method} must be async"
        sync_fn = inspect.unwrap(getattr(sync_cls, method))
        assert not inspect.iscoroutinefunction(sync_fn), f"{name}Sync.{method} must be sync"


def test_namespaces_expose_their_base_resource_with_types() -> None:
    from typing_extensions import assert_type

    from blindpay import BlindpayApiResponse
    from blindpay.resources.customers.customers import CustomersResource, GetCustomerResponse
    from blindpay.resources.instances.instances import GetInstanceMembersResponse
    from blindpay.resources.payins.payins import Payin, PayinsResourceSync
    from tests.http_mock import Recorder, async_client, sync_client

    client = sync_client(Recorder(body={}))

    # assert_type fails type checking if these resolve to Any (the old __getattr__ delegation).
    assert_type(client.payins.get("pa_000000000000"), BlindpayApiResponse[Payin])
    assert_type(client.customers.get("cu_000000000000"), BlindpayApiResponse[GetCustomerResponse])
    assert_type(client.instances.get_members(), BlindpayApiResponse[GetInstanceMembersResponse])
    assert isinstance(client.payins, PayinsResourceSync)
    assert isinstance(async_client(Recorder(body={})).customers, CustomersResource)
