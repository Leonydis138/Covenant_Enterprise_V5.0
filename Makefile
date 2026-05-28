# COVENANT.AI Enterprise v5.0 Makefile

.PHONY: help install dev test build deploy clean

help:
	@echo "COVENANT.AI Enterprise v5.0 - Available commands:"
	@echo "  make install    - Install all dependencies"
	@echo "  make dev        - Start development environment"
	@echo "  make test       - Run all tests"
	@echo "  make build      - Build Docker images"
	@echo "  make deploy     - Deploy to production"
	@echo "  make clean      - Clean build artifacts"

install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

dev:
	@echo "Starting development environment..."
	docker compose -f docker-compose.yml up

test:
	@echo "Running backend tests..."
	cd backend && python -m pytest -v --cov
	@echo "Running frontend tests..."
	cd frontend && npm test

build:
	@echo "Building Docker images..."
	docker compose -f docker-compose.yml build

deploy:
	@echo "Deploying to production..."
	kubectl apply -f infrastructure/kubernetes/

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true