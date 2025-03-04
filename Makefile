install:
	uv sync

build:
	uv build

package-install:
	uv tool install dist/*.whl

make lint:
	uv run ruff check gendiff

test:
	uv run pytest

check: test lint

test-coverage:
	uv run pytest --cov=hexlet_python_package --cov-report xml

run:
	uv run gendiff

.PHONY: install test lint selfcheck check build