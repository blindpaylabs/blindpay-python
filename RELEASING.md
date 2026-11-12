# Releasing blindpay-python

Releases are automatic: merging to `main` is publishing to PyPI. There is no manual step in the happy path.

## Version source of truth

release-please owns the version and moves these together. Never edit them by hand:
`.release-please-manifest.json` (`"."`), `pyproject.toml` (`[project].version`), `src/blindpay/_version.py`
(`# x-release-please-version` line, also the User-Agent) and `uv.lock` (the `blindpay` package's `version`).
`tests/test_packaging.py` fails if they disagree. The bump comes from conventional commits since the last `vX.Y.Z`
tag: `feat:` is a minor, `fix:` a patch. A `!` after the type, or a breaking-change footer anywhere in a commit or
squash body, is a major.

## What a merge to `main` triggers

1. `main.yaml` runs lint, type check, tests (3.12-3.14), contract check and api-sync check.
2. `publish.yaml` (push to `main`) runs release-please, which opens or updates the release PR
   `chore(main): release X.Y.Z` (version lines and `CHANGELOG.md` only).
3. The same job merges that PR itself, after two guards: the PR may change nothing outside `CHANGELOG.md` except
   version lines, and its checks must pass (`gh pr checks --watch --fail-fast`).
4. That merge is a push to `main`, so `publish.yaml` runs again: release-please creates tag `vX.Y.Z` and the GitHub
   release, then the `publish` job checks out the tag, checks `_version.py` and `pyproject.toml` match it, runs
   `uv build` and `uv publish`.

## Secrets and owners

| Secret | Used by | Owner |
|---|---|---|
| `SDK_SYNC_PAT` | release-please, the release-PR merge, api-sync PRs. A `GITHUB_TOKEN` push would not start the next workflow, so the chain needs a PAT. Created 2026-05-08: check its expiry | repo admin |
| `PYPI_API_TOKEN` | `uv publish` | PyPI project owner |
| `SLACK_WEBHOOK_URL` | `pipeline-alert.yml` (failure alerts) | repo admin |
| `SNYK_TOKEN` | `snyk.yaml` | repo admin |

`publish.yaml` already grants `id-token: write`. Moving to PyPI trusted publishing means adding this repo and
workflow as a trusted publisher on PyPI and dropping the two `UV_PUBLISH_*` variables.

## When a release gets stuck

- **Release PR open, never merged** (guard or red checks): read the `Merge the release PR` step log. Fix `main`, then
  re-run with `gh workflow run publish.yaml --ref main`; release-please rebuilds the PR from current `main`.
- **Tag and GitHub release exist, PyPI doesn't have the version**: re-run only the failed `publish` job
  (`gh run rerun <run-id> --failed`). A fresh dispatch won't publish: release-please reports `release_created`
  only on the run that created the release.
- **Release PR exists but CI never started on it**: it was pushed with a token that can't trigger workflows. Close
  it and dispatch `publish.yaml`.

## Verify a published version

```bash
uv run --isolated --no-project --with blindpay==X.Y.Z python -c "import blindpay; print(blindpay.__version__)"
curl -s https://pypi.org/pypi/blindpay/json | jq -r .info.version
```

Both must print `X.Y.Z`.

## Known traps

- **No `!`, no breaking-change footer** in commit messages, PR titles or squash bodies, even when describing the
  past. 4.0.0 became a major because release-please replayed old breaking-change footers.
- **`release-type` lives in `release-please-config.json` (`simple`)**, never as an action input: with the input,
  the action ignores the config and its `extra-files` (3.4.1 shipped a stale `_version.py`), and the `python` type
  rewrote `src/blindpay/__init__.py` from a stale copy (4.0.0 shipped without exports).
- **Tags are `vX.Y.Z`** (`include-component-in-tag: false`). The leftover `blindpay-v4.0.0` tag is unused.
- **Stale-content guard**: if it refuses a release PR, don't edit the PR. Land the fix on `main`; the next push
  rebuilds the PR.
- **api-sync PRs auto-merge** (`gh pr merge --auto`). Without required status checks on `main`, auto-merge doesn't
  wait for CI, and the merge publishes. Branch protection with required checks closes that gap.
