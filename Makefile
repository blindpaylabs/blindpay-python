.PHONY: lint-check lint-fix typecheck

lint-check:
	uv run ruff format --check
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .
	uv run ruff format

typecheck:
	uv run pyright
	uv run mypy .
