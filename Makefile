.PHONY: run-user-api run-order-api run-all

run-user-api:
	@docker network create -d bridge order-api_default || true
	@docker compose -f user-api/docker-compose.yml up -d
	@docker compose -f user-api/docker-compose.yml exec api_user poetry run alembic upgrade head 

run-order-api:
	@docker network create -d bridge user-api_default || true
	@docker compose -f order-api/docker-compose.yml up -d
	sleep 30
	@docker compose -f order-api/docker-compose.yml exec api_order poetry run poetry run python -m scripts.setup_es

run-all: run-user-api run-order-api
