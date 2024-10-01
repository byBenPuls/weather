.PHONY: all

SHELL=/bin/bash -e


install: ## Install common dependencies
	poetry install --no-dev


install-dev: ## Install dev dependencies
	poetry install --dev


lint: ## Lint code
	poetry run ruff check --fix .


format: ## Format code
	poetry run ruff format .


test: ## Test project
	poetry run pytest . -p no:logging -p no:warnings -p


prepare: ## Do lint and tests
	make lint
	make test


run: ## Setup project with docker-compose
	docker-compose build
	docker-compose up


bind ?= 127.0.0.1
port ?= 8000
serve: ## Setup project with uvicorn
	uvicorn src.main:create_app --host $(bind) --port $(port)


help: ## Show help message
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/:/'`); \
	printf "%s\n\n" "Usage: make [task]"; \
	printf "%-20s %s\n" "task" "help" ; \
	printf "%-20s %s\n" "------" "----" ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$':' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf '\033[36m'; \
		printf "%-20s %s" $$help_command ; \
		printf '\033[0m'; \
		printf "%s\n" $$help_info; \
	done