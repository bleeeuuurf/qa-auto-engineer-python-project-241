install:
	uv sync

lint:
	uv run ruff check .

lint-fix:
	uv run ruff check --fix .

test:
	uv run pytest

test-coverage:
	uv run pytest --cov --cov-report=term-missing