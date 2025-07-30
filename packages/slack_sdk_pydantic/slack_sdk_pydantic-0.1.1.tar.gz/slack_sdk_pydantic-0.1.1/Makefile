test:
	uv run pytest --cov=slack_sdk_pydantic
	uv run ruff check && uv run mypy -p slack_sdk_pydantic

fmt:
	uv run ruff check --select I,F401 --fix
	uv run ruff format

dist:
	uv build

dist/clean:
	rm -rf dist/

dist/release:
	uv publish
