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
        assert inspect.iscoroutinefunction(fn), f"{name}.{method} must be async"
        assert not inspect.iscoroutinefunction(getattr(sync_cls, method)), f"{name}Sync.{method} must be sync"
