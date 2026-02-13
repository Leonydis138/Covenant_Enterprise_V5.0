# Contributing to COVENANT.AI Enterprise

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Development Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install

# Start development servers
docker-compose up -d  # Database & Redis
python -m uvicorn covenant.main:app --reload
npm run dev
```

## Code Standards

- Python: Black, Ruff, MyPy
- TypeScript: ESLint, Prettier
- Write tests for new features
- Update documentation

## Testing

```bash
# Backend tests
pytest -v --cov

# Frontend tests
npm test

# Integration tests
pytest tests/integration/

# E2E tests
npm run test:e2e
```

## Pull Request Process

1. Update README if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers
