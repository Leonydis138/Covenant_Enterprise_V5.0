# COVENANT.AI Enterprise Makefile

.PHONY: help install dev test clean build deploy

help:
	@echo "COVENANT.AI Enterprise v3.0 - Available commands:"
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
	docker-compose -f docker-compose.full.yml up

test:
	@echo "Running backend tests..."
	cd backend && pytest -v --cov
	@echo "Running frontend tests..."
	cd frontend && npm test

build:
	@echo "Building Docker images..."
	docker-compose -f docker-compose.full.yml build

deploy:
	@echo "Deploying to production..."
	kubectl apply -f infrastructure/kubernetes/

clean:
	@echo "Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete