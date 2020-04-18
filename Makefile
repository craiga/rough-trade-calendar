default:  ## Build and serve the web site.
	pipenv run python manage.py migrate
	pipenv run python manage.py loaddata locations
	pipenv run python manage.py runserver

setup:  ## Install required environments and packages.
	pipenv install --dev
	npm ci
	printf "DEBUG=1\n" > .env

scrape:  ## Run the scraper.
	pipenv run python manage.py migrate
	pipenv run python manage.py loaddata locations
	pipenv run scrapy crawl rough_trade_events
	pipenv run scrapy crawl rough_trade_event_detail

test: ## Run tests.
	pipenv run pytest

lint-html: ## Lint HTML.
	npm run prettier -- **/*.html --check

fix-html: ## Attempt to fix HTML issues reported by the linter.
	npm run prettier -- **/*.html --write

lint-python: ## Lint Python.
	pipenv run isort --check-only
	pipenv run black --check --diff .
	find . -iname "*.py" | xargs pipenv run pylint
	pipenv run python manage.py makemigrations --check

fix-python: ## Attempt to automatically Python issues reported by linter.
	pipenv run isort --apply
	pipenv run black .

help: ## Display this help screen.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
