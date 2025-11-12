# Makefile docker exec -it excel_worker-web-1 /bin/bash

PROJECT_ROOT=/
APP_DIR=/app

.PHONY: migrate upgrade

migrate:
	@cd $(APP_DIR) && \
		DATE=$$(date +%Y-%m-%d-%H:%M) && \
		read -p "Введите сообщение для миграции: " MESSAGE && \
		alembic revision --autogenerate -m "$$DATE"_"$$MESSAGE"

upgrade:
	@cd $(APP_DIR) && \
		alembic upgrade head
