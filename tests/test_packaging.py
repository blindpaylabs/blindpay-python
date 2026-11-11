"""Packaging regression guards: what ships in the wheel and what it reports about itself."""

import json
import tomllib
from pathlib import Path

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

    def test_version_file_carries_the_release_please_marker(self):
        assert "# x-release-please-version" in (PACKAGE_DIR / "_version.py").read_text()

    def test_user_agent_reports_the_package_version(self):
        async_client = BlindPay(api_key="test_key", instance_id="in_000000000000")
        sync_client = BlindPaySync(api_key="test_key", instance_id="in_000000000000")
        expected = f"blindpay-python/{blindpay.__version__}"
        assert async_client._headers["User-Agent"] == expected
        assert sync_client._headers["User-Agent"] == expected
        sync_client.close()
