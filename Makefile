# =============== Simple Makefile (Docker + Dev/Test DB) ===============

DC  := docker compose
WEB := web
DB  := db

# ---------- Dev ----------
.PHONY: up down logs migrate makemigration

up:               ## Build & start dev stack
	$(DC) up -d --build

down:             ## Stop all containers (keep volumes)
	$(DC) down

down-volumes:
	$(DC) down -v

logs:             ## Tail logs
	$(DC) logs -f

migrate:          ## Apply Alembic migrations (current DB seen by web)
	$(DC) exec -w /app $(WEB) flask db upgrade

seed:
	$(DC) exec $(WEB) flask seed-doctors

makemigration:    ## Create a new Alembic migration (pass m="message")
	@[ -n "$(m)" ] || (echo "Usage: make makemigration m='your message'"; exit 1)
	$(DC) exec -w /app $(WEB) flask db migrate -m "$(m)"

# ---------- Test ----------
# Assumes TEST_DATABASE_URL is set in .env (and points to e.g. medical_db_test)

.PHONY: test-db-create test test-fast tf cov test-db-drop test-db-reset

test-db-create:   ## One-time: create the test DB inside Postgres (idempotent)
	@DBNAME=$$(grep -E '^TEST_DATABASE_URL=' .env | sed -E 's#.*/([^/?]+).*#\1#' || echo medical_db_test); \
	echo "Ensuring test database '$$DBNAME' exists..."; \
	$(DC) up -d $(DB); \
	$(DC) exec -T $(DB) psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname='$$DBNAME'" | grep -q 1 || \
	  $(DC) exec -T $(DB) psql -U postgres -c "CREATE DATABASE $$DBNAME;"

test: test-db-create
	$(DC) run --rm -w /app \
	  -e FLASK_ENV=test -e APP_ENV=test -e PYTHONPATH=/app \
	  $(WEB) flask db upgrade
	$(DC) run --rm -w /app \
	  -e FLASK_ENV=test -e APP_ENV=test -e PYTHONPATH=/app \
	  $(WEB) pytest -q

test-fast: test-db-create
	$(DC) up -d $(WEB)
	$(DC) exec -w /app $(WEB) env PYTHONPATH=/app flask db upgrade
	$(DC) exec -w /app $(WEB) env PYTHONPATH=/app pytest -q

tf: test-db-create
	@:[ -n "$(file)" ] || (echo "Usage: make tf file=PATH[::TEST]"; exit 1)
	$(DC) up -d $(WEB)
	$(DC) exec -w /app $(WEB) env PYTHONPATH=/app flask db upgrade
	$(DC) exec -w /app $(WEB) env PYTHONPATH=/app pytest -q $(file)

cov: test-db-create
	$(DC) run --rm -w /app \
	  -e FLASK_ENV=test -e APP_ENV=test -e PYTHONPATH=/app \
	  $(WEB) flask db upgrade
	$(DC) run --rm -w /app \
	  -e FLASK_ENV=test -e APP_ENV=test -e PYTHONPATH=/app \
	  $(WEB) pytest --cov=app --cov-report=term-missing

# Drop the TEST database (terminate connections first), then recreate it

test-db-drop:
	@DBNAME=$$(grep -E '^TEST_DATABASE_URL=' .env | sed -E 's#.*/([^/?]+).*#\1#' || echo medical_db_test); \
	echo "Dropping test database '$$DBNAME'..."; \
	$(DC) up -d db; \
	$(DC) exec -T db psql -U postgres -d postgres -v ON_ERROR_STOP=1 \
	  -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname='$$DBNAME';" ; \
	$(DC) exec -T db psql -U postgres -d postgres -v ON_ERROR_STOP=1 \
	  -c "DROP DATABASE IF EXISTS \"$$DBNAME\";"

test-db-reset: test-db-drop test-db-create

