"""Golden self-test for the operation-insert generator in .api-sync/sync.py.

Unlike test_api_sync.py (which never touches the real src/blindpay tree, only
synthetic fixture repos), this test deliberately operates on a scratch COPY of
the real repo: it deletes two real, currently-existing SDK methods (one GET,
one POST-with-body) along with their TypedDicts and spec-map entries, runs the
patcher with --apply against the repo's own committed spec snapshot, and
asserts the regenerated method's route, HTTP verb, and types match what was
deleted. It also runs pyright/mypy/pytest against the regenerated tree, and
checks that a second --apply is a no-op (idempotent).

This is slow (spins up a second uv-managed virtualenv) and is skipped unless
`uv` is on PATH.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import types
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SYNC_PATH = REPO_ROOT / ".api-sync" / "sync.py"

pytestmark = pytest.mark.skipif(shutil.which("uv") is None, reason="uv is required to build the golden scratch repo")

_load_counter = 0


def load_sync(root: Path) -> types.ModuleType:
    global _load_counter
    _load_counter += 1
    module_name = f"sync_golden_under_test_{_load_counter}"
    spec = importlib.util.spec_from_file_location(module_name, SYNC_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    module.ROOT = root  # type: ignore[attr-defined]
    module.API_SYNC = root / ".api-sync"  # type: ignore[attr-defined]
    module.SRC_ROOT = root / "src" / "blindpay"  # type: ignore[attr-defined]
    module.SNAPSHOT_PATH = module.API_SYNC / "spec-snapshot.json"  # type: ignore[attr-defined]
    module.DEFAULT_SPEC_PATH = module.API_SYNC / "spec-current.json"  # type: ignore[attr-defined]
    module.MAP_PATH = module.API_SYNC / "spec-map.json"  # type: ignore[attr-defined]
    module.UNMODELED_PATH = module.API_SYNC / "unmodeled.json"  # type: ignore[attr-defined]
    return module


def build_scratch_repo(dest: Path) -> None:
    """Copies just enough of the real repo to run the patcher and its gauntlet
    against: source, tests, and the packaging/tooling config the gauntlet
    needs (pyproject.toml for pyright/ruff config, uv.lock for a fast,
    reproducible `uv sync`)."""
    for rel in (
        "src",
        "tests",
        ".api-sync",
        "pyproject.toml",
        "uv.lock",
        "pyrightconfig.json",
        "pytest.ini",
        "py.typed",
        "README.md",
        "LICENSE",
    ):
        src = REPO_ROOT / rel
        dst = dest / rel
        if src.is_dir():
            # This file itself must never be copied in: the golden repo's own
            # `uv run pytest` (invoked below by test_regenerated_tree_passes_pytest)
            # would otherwise discover and re-run it, rebuilding another golden
            # repo inside itself, recursively, forever.
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("test_api_sync_golden.py"))
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    # --apply reads --spec, never spec-current.json's *default* unless told to;
    # give it a spec identical to the committed snapshot so the two real
    # deletions below are the only drift it needs to reconcile.
    shutil.copy2(dest / ".api-sync" / "spec-snapshot.json", dest / ".api-sync" / "spec-current.json")


def delete_get_secret(webhooks_py: Path) -> None:
    """Deletes WebhookEndpointsResource(Sync).get_secret() -- a GET with a
    single path param and an inline (unnamed) response schema -- and its
    TypedDict."""
    src = webhooks_py.read_text()
    for pattern in (
        "\n    async def get_secret(self, id: str) -> BlindpayApiResponse[GetWebhookEndpointSecretResponse]:\n"
        '        return await self._client.get(f"/instances/{self._instance_id}/webhook-endpoints/{id}/secret")\n',
        "\n    def get_secret(self, id: str) -> BlindpayApiResponse[GetWebhookEndpointSecretResponse]:\n"
        '        return self._client.get(f"/instances/{self._instance_id}/webhook-endpoints/{id}/secret")\n',
        "\n\nclass GetWebhookEndpointSecretResponse(TypedDict):\n    key: str\n",
    ):
        assert pattern in src, f"fixture assumption broken, pattern not found:\n{pattern}"
        src = src.replace(pattern, "\n" if pattern.startswith("\n    ") else "")
    webhooks_py.write_text(src)


def delete_create(webhooks_py: Path) -> None:
    """Deletes WebhookEndpointsResource(Sync).create() -- a POST with a
    request body and response, both $ref'd to named, spec-mapped schemas --
    and its TypedDicts."""
    src = webhooks_py.read_text()
    for pattern in (
        "\n    async def create(self, data: CreateWebhookEndpointInput) -> "
        "BlindpayApiResponse[CreateWebhookEndpointResponse]:\n"
        '        return await self._client.post(f"/instances/{self._instance_id}/webhook-endpoints", data)\n',
        "\n    def create(self, data: CreateWebhookEndpointInput) -> "
        "BlindpayApiResponse[CreateWebhookEndpointResponse]:\n"
        '        return self._client.post(f"/instances/{self._instance_id}/webhook-endpoints", data)\n',
        "\n\nclass CreateWebhookEndpointInput(TypedDict):\n    url: str\n    events: List[WebhookEvents]\n",
        "\n\nclass CreateWebhookEndpointResponse(TypedDict):\n    id: str\n",
    ):
        assert pattern in src, f"fixture assumption broken, pattern not found:\n{pattern}"
        src = src.replace(pattern, "\n" if pattern.startswith("\n    ") else "")
    webhooks_py.write_text(src)


def remove_spec_map_entries(map_path: Path, *spec_schemas: str) -> None:
    data = json.loads(map_path.read_text())
    data["types"] = [e for e in data["types"] if e["spec"] not in spec_schemas]
    map_path.write_text(json.dumps(data, indent=2) + "\n")


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


@pytest.fixture(scope="module")
def golden_repo(tmp_path_factory: pytest.TempPathFactory) -> Path:
    root = tmp_path_factory.mktemp("api-sync-golden")
    build_scratch_repo(root)

    webhooks_py = root / "src/blindpay/resources/webhooks/webhooks.py"
    delete_get_secret(webhooks_py)
    delete_create(webhooks_py)
    remove_spec_map_entries(root / ".api-sync/spec-map.json", "WebhookEndpointIn", "WebhookEndpointOut")

    sync_up_front = load_sync(root)
    # Sanity: with both methods gone, --check must now report drift (point 5
    # of the brief: a pending, un-applied operation-insert fails --check).
    assert sync_up_front.cmd_check(None) == 1

    sync_setup = load_sync(root)
    apply_result = sync_setup.cmd_apply(sync_setup.DEFAULT_SPEC_PATH, root / "apply-report.json")
    assert apply_result == 0, "the patcher refused to regenerate the two deleted methods"

    sync_env = run(["uv", "sync", "--group", "dev", "--group", "test"], cwd=root)
    assert sync_env.returncode == 0, sync_env.stderr

    return root


class TestGoldenRegeneration:
    def test_apply_regenerated_both_deleted_methods(self, golden_repo: Path) -> None:
        report = json.loads((golden_repo / "apply-report.json").read_text())
        assert report["bump"] == "minor"
        symbols = {a["symbol"] for a in report["applied"]}
        assert "WebhookEndpointsResource.get_secret" in symbols
        assert "WebhookEndpointsResource.create" in symbols

    def test_regenerated_get_secret_matches_original_route_verb_and_types(self, golden_repo: Path) -> None:
        src = (golden_repo / "src/blindpay/resources/webhooks/webhooks.py").read_text()
        assert "async def get_secret(self, id: str) -> BlindpayApiResponse[GetWebhookEndpointSecretResponse]:" in src
        assert 'self._client.get(f"/instances/{self._instance_id}/webhook-endpoints/{id}/secret")' in src
        assert "class GetWebhookEndpointSecretResponse(TypedDict):" in src
        assert "    key: str" in src

    def test_regenerated_create_matches_original_route_verb_and_types(self, golden_repo: Path) -> None:
        src = (golden_repo / "src/blindpay/resources/webhooks/webhooks.py").read_text()
        assert (
            "async def create(self, data: CreateWebhookEndpointInput) -> "
            "BlindpayApiResponse[CreateWebhookEndpointResponse]:" in src
        )
        assert 'self._client.post(f"/instances/{self._instance_id}/webhook-endpoints", data)' in src
        assert "class CreateWebhookEndpointInput(TypedDict):" in src
        assert "    url: str" in src
        assert "    events: List[WebhookEvents]" in src
        assert "class CreateWebhookEndpointResponse(TypedDict):" in src
        assert "    id: str" in src

    def test_regenerated_type_map_entries_were_restored(self, golden_repo: Path) -> None:
        map_data: dict[str, Any] = json.loads((golden_repo / ".api-sync/spec-map.json").read_text())
        mapped = {e["spec"]: e["sdk"][0]["symbol"] for e in map_data["types"] if isinstance(e["spec"], str)}
        assert mapped.get("WebhookEndpointIn") == "CreateWebhookEndpointInput"
        assert mapped.get("WebhookEndpointOut") == "CreateWebhookEndpointResponse"

    def test_regenerated_tree_passes_pyright(self, golden_repo: Path) -> None:
        result = run(["uv", "run", "pyright"], cwd=golden_repo)
        assert result.returncode == 0, result.stdout + result.stderr

    def test_regenerated_tree_passes_mypy(self, golden_repo: Path) -> None:
        result = run(["uv", "run", "mypy", "."], cwd=golden_repo)
        assert result.returncode == 0, result.stdout + result.stderr

    def test_regenerated_tree_passes_pytest(self, golden_repo: Path) -> None:
        result = run(["uv", "run", "pytest", "-q"], cwd=golden_repo)
        assert result.returncode == 0, result.stdout + result.stderr

    def test_second_apply_is_idempotent(self, golden_repo: Path) -> None:
        before = {
            p: (golden_repo / p).read_bytes()
            for p in ("src/blindpay/resources/webhooks/webhooks.py", ".api-sync/spec-map.json")
        }
        sync = load_sync(golden_repo)
        report_path = golden_repo / "second-apply-report.json"
        assert sync.cmd_apply(sync.DEFAULT_SPEC_PATH, report_path) == 0
        report = json.loads(report_path.read_text())
        assert report["applied"] == []
        assert report["bump"] is None
        for rel, content in before.items():
            assert (golden_repo / rel).read_bytes() == content, f"{rel} changed on a second, no-op apply"

    def test_check_is_green_after_apply(self, golden_repo: Path) -> None:
        sync = load_sync(golden_repo)
        assert sync.cmd_check(None) == 0


class TestMultipartFixtureRoutesToNeedsHuman:
    """A synthetic fixture operation with a multipart/form-data request body
    must be routed to needs-human with a reason that specifically names the
    unsupported content type -- never silently skipped, never misclassified
    as a STANDARD operation-insert."""

    def test_multipart_request_body_is_needs_human_with_precise_reason(self, golden_repo: Path) -> None:
        sync = load_sync(golden_repo)
        map_data = json.loads((golden_repo / ".api-sync/spec-map.json").read_text())
        # Two path params ("instance_id", "id") so this resolves to
        # WebhookEndpointsResource by item-prefix match (shared with its
        # sibling `delete(id)`), exactly like a real new sub-action would --
        # the point of this fixture is that content-type, not resource
        # matching or method-name collision, is what must send it to
        # needs-human. PUT (-> "update") is used rather than POST (-> "create")
        # because this same golden_repo already has a generated create().
        spec: dict[str, Any] = {
            "paths": {
                "/v1/instances/{instance_id}/webhook-endpoints/{id}/attachment": {
                    "put": {
                        "requestBody": {
                            "content": {"multipart/form-data": {"schema": {"type": "object", "properties": {}}}}
                        },
                        "responses": {"200": {"content": {}}},
                    }
                }
            },
            "components": {"schemas": {}},
        }
        plans, problems = sync.reconcile_operations(spec, map_data)
        assert plans == []
        assert len(problems) == 1
        assert problems[0].kind == "needs_human_operation"
        assert "multipart/form-data" in problems[0].detail
