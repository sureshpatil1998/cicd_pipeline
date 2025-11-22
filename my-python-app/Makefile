.PHONY: help install install-dev test lint format type-check security clean docker-build docker-run docker-stop

help:
	@echo "Available commands:"
	@echo "  make install       - Install production dependencies"
	@echo "  make install-dev   - Install development dependencies"
	@echo "  make test          - Run tests with pytest"
	@echo "  make lint          - Run flake8 linter"
	@echo "  make format        - Format code with black"
	@echo "  make format-check  - Check code formatting"
	@echo "  make type-check    - Run mypy type checker"
	@echo "  make security      - Run security checks"
	@echo "  make clean         - Remove build artifacts and cache"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"
	@echo "  make docker-stop   - Stop Docker container"

install:
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v --cov=app --cov-report=html --cov-report=term

test-quick:
	pytest tests/ -v

lint:
	flake8 app tests

format:
	black app tests

format-check:
	black --check app tests

type-check:
	mypy app --ignore-missing-imports

security:
	@echo "Running bandit security check..."
	bandit -r app --skip B101 || true
	@echo "\nRunning safety check..."
	safety check || true

all-checks: format-check lint type-check test security

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov
	rm -rf .tox
	rm -rf .ruff_cache

docker-build:
	docker build -t my-python-app .

docker-run:
	docker run -p 8000:8000 my-python-app

docker-stop:
	docker stop my-python-app || true
	docker rm my-python-app || true

compose-up:
	docker-compose up -d

compose-down:
	docker-compose down

compose-logs:
	docker-compose logs -f

dev-server:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
