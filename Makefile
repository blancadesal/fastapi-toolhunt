.PHONY: help init-db migrate seed start stop restart clean lint test logs db-shell status

help:  ## Show this help message
	@echo "Make targets:"
	@echo "============="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

start:  ## Start docker-compose services
	@docker-compose up -d

stop:  ## Stop docker-compose services
	@docker-compose down

restart: stop start  ## Restart docker-compose services

status:  ## Show the status of docker-compose services
	@docker-compose ps

web-logs:  ## View logs from the web service
	@docker-compose logs -f fastapi-web

init-db:  ## Initialize the database
	@docker-compose exec fastapi-web python toolhunt/db.py

migrate:  ## Perform database migrations
	@docker-compose exec fastapi-web aerich upgrade

seed:  ## Seed the database
	@docker-compose exec fastapi-web python scripts/seed.py

db-shell:  ## Access the database shell
	@docker-compose exec db mysql -u root -p

lint:  ## Run linting using tox
	@docker-compose exec fastapi-web tox

test:  ## Run tests using pytest
	@docker-compose exec fastapi-web python -m pytest

clean:  ## Clean up Docker images and containers
	@docker image prune -f
	@docker container prune -f
