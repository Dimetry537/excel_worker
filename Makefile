# Makefile docker exec -it excel_worker-web-1 /bin/bash

PROJECT_ROOT=/
APP_DIR=/app

.PHONY: migrate upgrade seed dev dev-build prod prod-build down logs

migrate:
	@cd $(APP_DIR) && \
		DATE=$$(date +%Y-%m-%d-%H:%M) && \
		read -p "Введите сообщение для миграции: " MESSAGE && \
		alembic revision --autogenerate -m "$$DATE"_"$$MESSAGE"

upgrade:
	@cd $(APP_DIR) && \
		alembic upgrade head

seed:
	@cd $(APP_DIR) && \
		python src/db/seed.py

dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up

dev-build:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build

prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

prod-build:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

down:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml down

logs:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml logs -f
