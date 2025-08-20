.PHONY: help setup dev test lint fmt clean docker/build docker/run install

help: ## Show this help message
	@echo "Jeff's API Ripper - Available Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Setup development environment
	pip install -e ".[dev]"
	pre-commit install
	@echo "Development environment setup complete!"

install: ## Install production dependencies
	pip install -e .

dev: ## Run development server
	streamlit run src/app/main.py

test: ## Run test suite
	pytest tests/ -v --cov=src

lint: ## Run linting checks
	ruff check src/ tests/
	mypy src/

fmt: ## Format code
	black src/ tests/
	ruff check --fix src/ tests/

clean: ## Clean build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

docker/build: ## Build Docker image
	docker build -t jeffs-api-ripper .

docker/run: ## Run Docker container
	docker run -p 8501:8501 jeffs-api-ripper

docker/stop: ## Stop Docker container
	docker stop $$(docker ps -q --filter ancestor=jeffs-api-ripper)

docker/clean: ## Clean Docker images
	docker rmi jeffs-api-ripper

build: ## Build the project
	python -m build

dist: ## Create distribution packages
	python -m build --wheel --sdist

publish: ## Publish to PyPI (requires twine)
	twine upload dist/*

check: ## Check package for common issues
	check-manifest
	twine check dist/*
