.PHONY: dev run lint-check lint test test-integration test-matching setup-elasticsearch

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
	@ORDERS_INDEX=orders_test poetry run pytest tests/integration

test-matching:
	@ORDERS_INDEX=orders_test poetry run pytest --pdb -k ${K}

setup-elasticsearch:
	@poetry run python -m scripts.setup_es

run-migrations:
	@poetry run alembic upgrade head
