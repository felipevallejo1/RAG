# Convenience wrappers. Everything also works with plain `docker compose` commands.
.PHONY: up down logs ps test lint fmt reset

up: ## Build and start the whole stack
	docker compose up -d --build

down: ## Stop the stack (keeps data)
	docker compose down

reset: ## Stop the stack and DELETE all data volumes
	docker compose down -v

logs: ## Follow logs (usage: make logs s=backend)
	docker compose logs -f $(s)

ps: ## Show service status
	docker compose ps

test: ## Run backend tests
	cd backend && uv run pytest

lint: ## Lint and check formatting
	cd backend && uv run ruff check . && uv run ruff format --check .

fmt: ## Auto-format
	cd backend && uv run ruff check --fix . && uv run ruff format .
