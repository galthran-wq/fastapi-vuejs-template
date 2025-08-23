.PHONY: dev-up dev-down dev-ps dev-logs dev-restart prod-up prod-down prod-ps prod-logs prod-restart dev-superuser prod-superuser dev-balance prod-balance dev-user prod-user
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
