.PHONY: dev-up dev-down dev-ps dev-logs dev-restart dev-db dev-make-migrations dev-test-db dev-test-migrate dev-test prod-up prod-down prod-ps prod-logs prod-restart prod-build
.SILENT:

-include .env
export
ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(ARGS):
	@true

dev-up:
	docker compose -p $(COMPOSE_PROJECT_NAME_DEV) -f docker-compose.yaml -f docker-compose.override.yaml up -d $(ARGS)

dev-down:
	docker compose -p $(COMPOSE_PROJECT_NAME_DEV) down $(ARGS)

dev-ps:
	docker compose -p $(COMPOSE_PROJECT_NAME_DEV) ps $(ARGS)

dev-logs:
	docker compose -p $(COMPOSE_PROJECT_NAME_DEV) logs -f $(ARGS)

dev-restart:
	docker compose -p $(COMPOSE_PROJECT_NAME_DEV) restart $(ARGS)

dev-build:
	docker compose -p $(COMPOSE_PROJECT_NAME_DEV) build $(ARGS)

dev-db:
	docker compose -p $(COMPOSE_PROJECT_NAME_DEV) exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

dev-make-migrations:
	docker compose -p $(COMPOSE_PROJECT_NAME_DEV) exec server bash -lc "python -m alembic revision --autogenerate -m '$(ARGS)'"

dev-test-db:
	docker compose -p $(COMPOSE_PROJECT_NAME_DEV) exec postgres createdb -U $(POSTGRES_USER) $(POSTGRES_DB)_test || true

dev-test-migrate:
	docker compose -p $(COMPOSE_PROJECT_NAME_DEV) exec -e POSTGRES_DB=$(POSTGRES_DB)_test -e PYTHONPATH=/app server bash -lc "alembic upgrade head"

dev-test:
	docker compose -p $(COMPOSE_PROJECT_NAME_DEV) exec -e POSTGRES_DB=$(POSTGRES_DB)_test -e PYTHONPATH=/app server bash -lc "pytest tests/ -v $(ARGS)"

prod-up:
	docker compose -p $(COMPOSE_PROJECT_NAME_PROD) -f docker-compose.yaml -f docker-compose.prod.yaml up -d $(ARGS)

prod-down:
	docker compose -p $(COMPOSE_PROJECT_NAME_PROD) down $(ARGS)

prod-ps:
	docker compose -p $(COMPOSE_PROJECT_NAME_PROD) ps $(ARGS)

prod-logs:
	docker compose -p $(COMPOSE_PROJECT_NAME_PROD) logs -f $(ARGS)

prod-restart:
	docker compose -p $(COMPOSE_PROJECT_NAME_PROD) restart $(ARGS)

prod-build:
	docker compose -p $(COMPOSE_PROJECT_NAME_PROD) build $(ARGS)
