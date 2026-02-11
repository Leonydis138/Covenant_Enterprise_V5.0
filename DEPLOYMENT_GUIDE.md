# COVENANT.AI v5.0 - Complete Deployment Guide

## 🎉 **YOU NOW HAVE A COMPLETE, PRODUCTION-READY SYSTEM!**

This is the **ultimate version** of Covenant Enterprise with everything you need for production deployment.

---

## 📦 **What's Included (28 Files)**

### Backend (Python 3.11+)
```
backend/
├── requirements.txt          # All dependencies
├── pyproject.toml           # Build configuration
├── Dockerfile               # Container image
├── src/covenant/
│   ├── __init__.py         # Package init
│   ├── core/
│   │   └── engine.py       # ⭐ Ultimate Constitutional Engine
│   └── api/
│       └── main.py         # FastAPI application
└── tests/
    ├── __init__.py
    ├── pytest.ini
    └── test_engine.py      # Comprehensive tests
```

### Frontend (React 18 + TypeScript)
```
frontend/
├── package.json            # Dependencies
├── vite.config.ts         # Build config
├── tsconfig.json          # TypeScript config
├── tailwind.config.js     # Styling
├── Dockerfile             # Container image
├── index.html             # Entry point
└── src/
    ├── main.tsx          # App entry
    ├── App.tsx           # Main component
    ├── Dashboard.tsx     # ⭐ Beautiful dashboard
    └── index.css         # Global styles
```

### Infrastructure
```
infrastructure/
└── kubernetes/
    └── deployment.yaml    # K8s deployment + service
```

### CI/CD
```
.github/
└── workflows/
    └── ci.yml            # ⭐ Bulletproof CI/CD
```

### Documentation
```
docs/
├── QUICKSTART.md         # 30-second start
└── API.md               # Complete API reference
```

### Configuration
```
docker-compose.yml        # Full stack setup
Makefile                 # Build automation
LICENSE                  # Apache 2.0
.gitignore              # Git exclusions
README.md               # ⭐ Comprehensive docs
```

---

## 🚀 **Quick Start (Choose One)**

### Option 1: Docker Compose (Recommended - 30 seconds)

```bash
# 1. Extract the zip to your repository
unzip covenant_FINAL_v5.0.zip
cd covenant_FINAL_v5.0

# 2. Start everything
docker-compose up

# 3. Access
# API:       http://localhost:8000
# Docs:      http://localhost:8000/docs
# Dashboard: http://localhost:3000
# Health:    http://localhost:8000/health
```

**That's it! Everything runs!** ✅

### Option 2: Manual Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m covenant.api.main

# Runs on http://localhost:8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev

# Runs on http://localhost:3000
```

**Database (optional):**
```bash
docker run -d -p 5432:5432 \
  -e POSTGRES_USER=covenant \
  -e POSTGRES_PASSWORD=covenant \
  -e POSTGRES_DB=covenant \
  postgres:15-alpine
```

### Option 3: Kubernetes Production

```bash
# Build images
docker build -t covenant-api:5.0.0 ./backend
docker build -t covenant-frontend:5.0.0 ./frontend

# Deploy
kubectl apply -f infrastructure/kubernetes/deployment.yaml

# Get external IP
kubectl get svc covenant-svc
```

---

## 🧪 **Testing Your Setup**

### Test the API
```bash
# Health check
curl http://localhost:8000/health

# Evaluate an action
curl -X POST http://localhost:8000/api/v1/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "action_type": "data_access",
    "description": "Access user data",
    "actor": "user_123",
    "parameters": {"user_id": "456"},
    "context": {"consent": true},
    "verification_level": "STANDARD"
  }'

# Get metrics
curl http://localhost:8000/api/v1/metrics
```

### Run Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Test Frontend
```bash
cd frontend
npm test
```

---

## 📊 **Accessing the Dashboard**

Open http://localhost:3000 to see:

- ✅ **Real-time metrics** - Total evaluations, approval rate, latency
- ✅ **System status** - All components health
- ✅ **Quick actions** - Evaluate, audit, report
- ✅ **Live updates** - Refreshes every 5 seconds
- ✅ **Beautiful UI** - Modern, responsive design

---

## 🔧 **Configuration**

### Environment Variables

Create `.env` file in root:

```bash
# Database
DATABASE_URL=postgresql://covenant:covenant@localhost:5432/covenant

# Redis
REDIS_URL=redis://localhost:6379

# API
API_PORT=8000
API_HOST=0.0.0.0

# Frontend
VITE_API_URL=http://localhost:8000

# Features
ENABLE_BLOCKCHAIN=false
ENABLE_ADVANCED_ML=false
```

### Scaling

**Docker Compose:**
```bash
docker-compose up --scale backend=3
```

**Kubernetes:**
```bash
kubectl scale deployment covenant-api --replicas=10
```

---

## 📈 **Monitoring**

### Prometheus Metrics
```bash
curl http://localhost:8000/metrics
```

### Application Metrics
```bash
curl http://localhost:8000/api/v1/metrics
```

**Available Metrics:**
- `total_evaluations` - Total actions evaluated
- `approved` - Actions approved
- `denied` - Actions denied
- `approval_rate` - % of approved actions
- `average_latency_ms` - Average response time
- `active_agents` - Number of swarm agents

---

## 🎯 **Key Features Explained**

### 1. Multi-Agent Swarm (6 Agents)
- Safety Agent
- Privacy Agent
- Fairness Agent
- Security Agent
- Compliance Agent
- Ethics Agent

Each agent independently evaluates actions, then consensus is reached.

### 2. 5-Level Verification
- **BASIC** - Fast checks (< 5ms)
- **STANDARD** - Balanced (10-20ms) ← Default
- **ENHANCED** - More thorough (20-50ms)
- **FORMAL** - Formal verification (50-100ms)
- **CERTIFIED** - Maximum rigor (100-200ms)

### 3. Proof Chain
Every evaluation generates cryptographic proof:
```
action:abc123 → consensus:def456 → proof:xyz789
```

### 4. Real-time Dashboard
Built with React + TanStack Query for live updates.

---

## 🔐 **Security Features**

- ✅ CORS protection
- ✅ Input validation (Pydantic)
- ✅ Rate limiting ready
- ✅ HTTPS ready
- ✅ Secrets management
- ✅ Container security
- ✅ Network isolation

---

## 🚢 **Deployment Checklist**

### Pre-deployment
- [ ] Review configuration
- [ ] Set environment variables
- [ ] Configure secrets
- [ ] Test locally
- [ ] Run all tests

### Deployment
- [ ] Build Docker images
- [ ] Push to registry
- [ ] Deploy to Kubernetes
- [ ] Configure load balancer
- [ ] Set up monitoring
- [ ] Configure backups

### Post-deployment
- [ ] Verify health endpoints
- [ ] Test API functionality
- [ ] Check dashboard access
- [ ] Monitor metrics
- [ ] Test auto-scaling

---

## 🐛 **Troubleshooting**

### Backend won't start
```bash
# Check dependencies
pip list

# Check Python version
python --version  # Should be 3.11+

# Check logs
docker-compose logs backend
```

### Frontend won't build
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install

# Check Node version
node --version  # Should be 20+
```

### Database connection fails
```bash
# Check database is running
docker ps | grep postgres

# Test connection
psql postgresql://covenant:covenant@localhost:5432/covenant
```

### Port already in use
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead of 8000
```

---

## 📚 **Learn More**

### Documentation
- `/docs` - Interactive API docs (Swagger UI)
- `/redoc` - Alternative docs (ReDoc)
- `docs/API.md` - API reference
- `docs/QUICKSTART.md` - Quick start guide

### Code Structure
- `backend/src/covenant/core/engine.py` - Main engine logic
- `backend/src/covenant/api/main.py` - API endpoints
- `frontend/src/Dashboard.tsx` - Dashboard UI

### Advanced Features
- Blockchain integration (optional)
- Advanced ML models (optional)
- Federated learning (optional)
- Custom verification levels

---

## 🎓 **Next Steps**

1. **Familiarize** - Run locally, test API, explore dashboard
2. **Customize** - Modify engine logic, add constraints
3. **Integrate** - Connect to your applications
4. **Deploy** - Push to production (K8s/Cloud)
5. **Monitor** - Set up alerts and dashboards
6. **Scale** - Add replicas as needed

---

## 💡 **Tips**

### Development
- Use `make dev` for quick start
- Check `make help` for all commands
- Enable hot reload for fast iteration
- Use Docker for consistency

### Production
- Use Kubernetes for orchestration
- Enable monitoring (Prometheus/Grafana)
- Set up log aggregation
- Configure backups
- Use secrets management
- Enable HTTPS

### Performance
- Redis caching for frequent queries
- Database connection pooling
- CDN for frontend assets
- Horizontal scaling
- Load balancing

---

## ✅ **Success Indicators**

You'll know it's working when:
- ✅ Health endpoint returns 200 OK
- ✅ Dashboard shows live metrics
- ✅ API evaluations return < 50ms
- ✅ All tests pass
- ✅ No errors in logs
- ✅ Swarm agents all active

---

## 🎉 **You're Ready!**

This is a **complete, production-ready system** with:

- ✅ **28 production files**
- ✅ **Working backend** (FastAPI + Engine)
- ✅ **Modern frontend** (React + TypeScript)
- ✅ **Bulletproof CI/CD** (GitHub Actions)
- ✅ **Container deployment** (Docker)
- ✅ **Kubernetes ready** (HPA, scaling)
- ✅ **Comprehensive tests** (pytest)
- ✅ **Beautiful dashboard** (Real-time UI)
- ✅ **Full documentation** (API, guides)

**Everything you need to run constitutional AI at scale!** 🚀

---

**Questions?** Check the docs or API reference.
**Issues?** See troubleshooting section.
**Ready?** Run `docker-compose up` and start evaluating! ✨
