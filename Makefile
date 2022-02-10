.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

init: ## Install your local environment for first time
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install ".[dev]"
test: ## Run project tests
	python -m pytest tests
lint: ## Run code linting
	python -m flake8 .
format: ## Format code with Black
	black .
coverage: ## Run package tests and upload coverage reports
	python -m pytest --cov-report term --cov-report xml --cov=django_inertia
publish: ## Publish package to pypi
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg src/inertia_django.egg-info
