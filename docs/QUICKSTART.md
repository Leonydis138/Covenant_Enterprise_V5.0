# Quick Start Guide

## Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+

## 30-Second Start

```bash
# 1. Clone
git clone <your-repo>
cd Covenant_Enterprise_V4.0

# 2. Run
docker-compose up

# 3. Access
# API: http://localhost:8000
# Dashboard: http://localhost:3000
# Docs: http://localhost:8000/docs
```

## Manual Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
python -m covenant.api.main
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## First Evaluation

```bash
curl -X POST http://localhost:8000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "action_type": "data_access",
    "description": "Access user profile",
    "actor": "user_123",
    "parameters": {"user_id": "456"},
    "context": {"consent": true}
  }'
```

## Next Steps
- Read [API.md](API.md) for API reference
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for design
