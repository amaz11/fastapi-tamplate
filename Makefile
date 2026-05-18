.PHONY: help install up down logs restart migrate seed test lint format shell docker-migrate docker-seed new-project

PYTHON := $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)
PIP := $(if $(wildcard .venv/bin/pip),.venv/bin/pip,pip3)

help: ## Show targets
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

install: ## Create venv and install deps
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt -r requirements-dev.txt
	@test -f .env || cp .env.example .env

up: ## Start API + MySQL (Docker)
	docker compose up -d --build

down: ## Stop Docker services
	docker compose down

logs: ## Follow API logs
	docker compose logs -f api

restart: ## Rebuild and restart API container
	docker compose up -d --build api

migrate: ## Run Alembic migrations (local)
	$(PYTHON) -m alembic upgrade head

seed: ## Seed dev admin user (local)
	$(PYTHON) scripts/seed.py

test: ## Run pytest (local)
	$(PYTHON) -m pytest app/tests/ -q

lint: ## Ruff check + format check
	$(PYTHON) -m ruff check .
	$(PYTHON) -m ruff format --check .

format: ## Auto-format with ruff
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check --fix .

shell: ## Open shell in API container
	docker compose exec api sh

docker-migrate: ## Run migrations inside API container
	docker compose exec api alembic upgrade head

docker-seed: ## Run seed inside API container
	docker compose exec api python scripts/seed.py

new-project: ## Create project copy: make new-project DIR=../my-api NAME="My API"
	@test -n "$(DIR)" || (echo "Usage: make new-project DIR=../target-dir [NAME=\"Display Name\"]"; exit 1)
	@chmod +x scripts/new-project.sh
	@./scripts/new-project.sh "$(DIR)" "$(NAME)"
