# COVENANT.AI Enterprise v6.0 - Quick Start Guide

Get up and running with COVENANT.AI in minutes!

## Prerequisites

- Docker & Docker Compose
- (Optional) Node.js 18+ and Python 3.12+

## 🚀 Quick Start (5 minutes)

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/Covenant_Enterprise_V6.0.git
cd Covenant_Enterprise_V6.0
```

### 2. Configure Environment

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys (optional)
```

### 3. Start Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis cache
- Qdrant vector database
- Backend API
- Frontend dashboard
- Prometheus monitoring
- Grafana dashboards

### 4. Access Applications

- **Frontend Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **GraphQL Playground**: http://localhost:8000/graphql
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)

### 5. Test the API

```bash
curl -X POST http://localhost:8000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "action": {
      "type": "content_moderation",
      "data": "Sample action to evaluate"
    }
  }'
```

## 📖 Next Steps

1. **Read the Documentation**: Check [docs/ARCHITECTURE.md](ARCHITECTURE.md)
2. **Configure Agents**: Customize constitutional principles
3. **Add LLM Integration**: Add OpenAI or Anthropic API keys
4. **Deploy to Production**: See [DEPLOYMENT.md](DEPLOYMENT.md)

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs -f

# Restart services
docker-compose restart
```

### Database Connection Issues

```bash
# Reset database
docker-compose down -v
docker-compose up -d
```

## 🎯 Example Usage

### Python SDK

```python
import requests

api_url = "http://localhost:8000"
token = "your-jwt-token"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.post(
    f"{api_url}/api/v1/evaluate",
    json={
        "action": {
            "type": "decision",
            "description": "Approve loan application"
        }
    },
    headers=headers
)

result = response.json()
print(f"Allowed: {result['allowed']}")
print(f"Confidence: {result['confidence']}")
print(f"Reasoning: {result['reasoning']}")
```

### JavaScript/TypeScript

```typescript
const apiUrl = 'http://localhost:8000';
const token = 'your-jwt-token';

const response = await fetch(`${apiUrl}/api/v1/evaluate`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    action: {
      type: 'decision',
      description: 'Approve loan application',
    },
  }),
});

const result = await response.json();
console.log('Allowed:', result.allowed);
console.log('Confidence:', result.confidence);
console.log('Reasoning:', result.reasoning);
```

## 🔗 Useful Links

- [API Documentation](http://localhost:8000/docs)
- [Architecture Guide](ARCHITECTURE.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Contributing Guide](../CONTRIBUTING.md)

---

**Need Help?** Open an issue on GitHub or join our Discord community.