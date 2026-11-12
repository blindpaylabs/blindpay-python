"""Packaging regression guards: what ships in the wheel and what it reports about itself."""

import json
import tomllib
from pathlib import Path
from typing import List

import blindpay
from blindpay import BlindPay, BlindPaySync

PACKAGE_DIR = Path(blindpay.__file__).parent
REPO_ROOT = Path(__file__).parent.parent


class TestPackaging:
    def test_py_typed_marker_lives_inside_the_package(self):
        # The wheel packages only src/blindpay, so a marker at the repo root never reaches users (PEP 561).
        assert (PACKAGE_DIR / "py.typed").is_file()

    def test_runtime_version_matches_the_released_version(self):
        # release-please bumps pyproject.toml and the manifest, and rewrites _version.py through the
        # x-release-please-version marker. If they drift, the User-Agent reports the wrong version.
        pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())
        manifest = json.loads((REPO_ROOT / ".release-please-manifest.json").read_text())
        assert blindpay.__version__ == pyproject["project"]["version"] == manifest["."]

    def test_lockfile_pins_the_released_version(self):
        # release-please bumps uv.lock too (extra-files), so `uv sync --locked` keeps working after a release.
        lock = tomllib.loads((REPO_ROOT / "uv.lock").read_text())
        (own,) = [package for package in lock["package"] if package["name"] == "blindpay"]
        assert own["version"] == blindpay.__version__

    def test_version_file_carries_the_release_please_marker(self):
        assert "# x-release-please-version" in (PACKAGE_DIR / "_version.py").read_text()

    def test_user_agent_reports_the_package_version(self):
        async_client = BlindPay(api_key="test_key", instance_id="in_000000000000")
        sync_client = BlindPaySync(api_key="test_key", instance_id="in_000000000000")
        expected = f"blindpay-python/{blindpay.__version__}"
        assert async_client._headers["User-Agent"] == expected
        assert sync_client._headers["User-Agent"] == expected
        sync_client.close()


# Names defined in more than one resource module: the root exports the other module's copy.
_ROOT_EXPORTS_ANOTHER_COPY = {
    ("ArgentinaTransfers", "payouts/payouts.py"),
    ("OfframpWallet", "bank_accounts/bank_accounts.py"),
    ("PayinLimit", "limits/limits.py"),
    ("PayoutLimit", "limits/limits.py"),
    ("GetCustomerLimitsResponse", "limits/limits.py"),
    ("MigrateInstanceOwnershipInput", "ownership/ownership.py"),
    ("MigrateInstanceOwnershipResponse", "ownership/ownership.py"),
    ("PaymentMethod", "payins/quotes.py"),
}


def test_every_public_resource_type_is_importable_from_the_package_root():
    """Inputs, outputs, enums and resource classes are all importable as ``from blindpay import X``."""
    import ast

    resources = Path(blindpay.__file__).parent / "resources"
    missing: List[str] = []
    for module in sorted(resources.rglob("*.py")):
        if module.name == "__init__.py":
            continue
        rel = str(module.relative_to(resources))
        for node in ast.parse(module.read_text()).body:
            if isinstance(node, ast.ClassDef):
                name = node.name
            elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
                name = node.targets[0].id
            else:
                continue
            if name.startswith("_") or (name, rel) in _ROOT_EXPORTS_ANOTHER_COPY:
                continue
            if name not in blindpay.__all__ or not hasattr(blindpay, name):
                missing.append(f"{rel}:{name}")

    assert not missing, missing
    assert len(blindpay.__all__) == len(set(blindpay.__all__))
