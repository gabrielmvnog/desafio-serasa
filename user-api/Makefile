.PHONY: dev run lint-check lint test test-integration test-matching create-migration run-migrations

dev: 
	@poetry run uvicorn app.main:app --reload

run:
	@poetry run uvicorn app.main:app

lint-check:
	@poetry run ruff check .

lint:
	@poetry run ruff check . --fix

test:
	@poetry run pytest tests/unit

test-integration:
	@POSTGRES_DB=app_test poetry run pytest tests/integration

test-matching:
	@POSTGRES_DB=app_test poetry run pytest --pdb -k ${K}

create-migration:
	@poetry run alembic revision --autogenerate -m ${M}

run-migrations:
	@poetry run alembic upgrade head

load-api:
	@poetry run python -m scripts.load_api
