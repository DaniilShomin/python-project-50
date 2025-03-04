install:
	uv sync

build:
	uv build

package-install:
	uv tool install dist/*.whl

make lint:
	uv run ruff check gendiff