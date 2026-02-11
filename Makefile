all: install

install:
	cd backend && pip install -r requirements-full.txt
	cd frontend && npm install

dev:
	docker-compose -f docker-compose.ultimate.yml up

test:
	cd backend && pytest -v

deploy:
	kubectl apply -f infrastructure/kubernetes/
