# Package Versioning Guide

This project uses [release-please](https://github.com/googleapis/release-please) to automate versioning, changelog generation, and publishing to PyPI. Versions follow [Semantic Versioning (semver)](https://semver.org/) and are determined automatically based on [Conventional Commits](https://www.conventionalcommits.org/).

## How It Works

### The Release Pipeline

1. You merge a PR into `main` with conventional commit messages.
2. **release-please** (running in `.github/workflows/publish.yaml`) automatically opens or updates a **Release PR** titled `chore(main): release X.Y.Z`.
3. That Release PR bumps the version in all tracked files and updates `CHANGELOG.md`.
4. When the Release PR is merged, release-please creates a GitHub Release and tag, which triggers the **publish** job to build and upload the package to PyPI.

### What release-please Updates Automatically

When the Release PR is merged, release-please bumps the version in these files (you should **never** bump them manually):

- `pyproject.toml` (`version = "X.Y.Z"`)
- `src/blindpay/__init__.py` (`__version__ = "X.Y.Z"`)
- `.release-please-manifest.json` (`".": "X.Y.Z"`)
- `CHANGELOG.md` (appends the new version entry)

These are configured in `release-please-config.json` under `extra-files` and the default Python release type.

## Conventional Commits

The commit message format determines the version bump. **Only the PR title matters** when using squash merges (GitHub uses the PR title as the commit message).

### Patch Release (`X.Y.Z` -> `X.Y.Z+1`)

For bug fixes and minor corrections that don't add new functionality:

```
fix: correct receiver address validation
fix: handle empty response from virtual accounts endpoint
```

### Minor Release (`X.Y.Z` -> `X.Y+1.0`)

For new features that are **backward-compatible**:

```
feat: add new tos and solana endpoints
feat: add swift code check endpoint
```

### Major Release (`X.Y.Z` -> `X+1.0.0`)

For **breaking changes** — anything that could cause existing users' code to fail:

```
feat!: update receiver and virtual account types to match API reference
```

Or using a `BREAKING CHANGE` footer:

```
feat: update receiver and virtual account types

BREAKING CHANGE: removed OwnerUpdate type, CreateVirtualAccountInput now requires banking_partner field
```

### Other Commit Types (No Release)

These commit types do **not** trigger a version bump:

```
chore: update CI workflow
docs: update README
test: add unit tests for receivers
ci: fix lint workflow
refactor: reorganize internal utils
```

## What Counts as a Breaking Change?

When working on this SDK, the following changes are **breaking** and require a `feat!:` prefix or `BREAKING CHANGE` footer:

| Change | Breaking? | Why |
|--------|-----------|-----|
| Removing a previously exported type (e.g., `OwnerUpdate`) | Yes | Users importing it will get `ImportError` |
| Adding a new **required** field to an input `TypedDict` | Yes | Existing calls will fail type checking / miss the field |
| Removing a field from an input `TypedDict` | Yes | Users passing that field will get a type error |
| Changing a field's type (e.g., `str` -> `int`) | Yes | Users' existing values may become invalid |
| Changing `owners` from `List[OwnerUpdate]` to `List[Owner]` | Yes | Different type with different fields |
| Making a required field **optional** | No | Existing code still works, just less strict |
| Adding a new **optional** field to a `TypedDict` | No | Existing code ignores it |
| Adding a new exported type | No | Doesn't affect existing code |
| Adding new values to a `Literal` type | No | Existing values still valid |

## Step-by-Step: Making a New Release

### 1. Create Your Feature Branch

```bash
git checkout -b eric/my-new-feature
```

### 2. Make Your Changes

Edit the source code under `src/blindpay/`.

### 3. Commit with Conventional Commit Messages

Use the appropriate prefix based on the nature of your changes:

```bash
# For a new non-breaking feature:
git commit -m "feat: add webhook retry configuration"

# For a breaking change:
git commit -m "feat!: redesign receiver creation flow

BREAKING CHANGE: CreateIndividualWithStandardKYCInput now requires account_purpose field"

# For a bug fix:
git commit -m "fix: handle timeout in payout status polling"
```

### 4. Open a Pull Request

Make sure the **PR title** follows conventional commits format, since this repo uses squash merges (the PR title becomes the final commit message on `main`).

- Non-breaking feature: `feat: add webhook retry configuration`
- Breaking change: `feat!: redesign receiver creation flow`
- Bug fix: `fix: handle timeout in payout status polling`

### 5. Merge to `main`

After CI passes and the PR is approved, merge it.

### 6. Release PR Is Created/Updated Automatically

release-please will open (or update) a PR titled something like:

```
chore(main): release 1.3.0
```

This PR contains:
- Version bumps in `pyproject.toml`, `src/blindpay/__init__.py`, `.release-please-manifest.json`
- Updated `CHANGELOG.md` with entries derived from commit messages

### 7. Review and Merge the Release PR

Once you're ready to publish the new version, merge the Release PR. This triggers:
1. A GitHub Release is created with the tag (e.g., `v1.3.0`)
2. The publish workflow builds and uploads the package to PyPI

## Configuration Files

| File | Purpose |
|------|---------|
| `release-please-config.json` | Configures release-please behavior (release type, changelog path, extra files to update) |
| `.release-please-manifest.json` | Tracks the current released version (updated by release-please, don't edit manually) |
| `.github/workflows/publish.yaml` | Workflow that runs release-please and publishes to PyPI |

## Important Rules

1. **Never manually bump versions** in `pyproject.toml`, `__init__.py`, or the manifest. release-please handles this.
2. **Always use conventional commit prefixes** in your PR title (for squash merges).
3. **Mark breaking changes explicitly** with `!` after the type or with a `BREAKING CHANGE:` footer.
4. **Don't merge the Release PR until you're ready** to publish to PyPI — merging it triggers the publish immediately.

## Past Release History

| Version | Type | Commit Prefix | Description |
|---------|------|---------------|-------------|
| `v0.1.0` | Initial | — | Initial release |
| `v1.0.0` | Major | `feat!:` | Stable release with breaking changes |
| `v1.1.0` | Minor | `feat:` | Added swift code check endpoint |
| `v1.2.0` | Minor | `feat:` | Added new TOS and Solana endpoints |
