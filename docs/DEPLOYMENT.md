# Deployment Guide

## Prerequisites

- Docker 24+
- Kubernetes 1.28+ (for production)
- PostgreSQL 15+
- Redis 7+
- Node.js 20+
- Python 3.11+

## Local Development

```bash
./scripts/quickstart.sh
```

## Docker Compose

```bash
docker-compose -f docker-compose.full.yml up
```

## Kubernetes

```bash
# Apply configurations
kubectl apply -f infrastructure/kubernetes/

# Check status
kubectl get pods
kubectl get services

# View logs
kubectl logs -f deployment/covenant-api
```

## Environment Variables

See `backend/.env.example` for all configuration options.

Critical variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Application secret key
- `JWT_SECRET`: JWT signing key

## Monitoring

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)

## Scaling

Horizontal Pod Autoscaler automatically scales based on:
- CPU utilization (70% target)
- Memory utilization (80% target)
- Custom metrics

## Backup

```bash
# Database backup
pg_dump covenant > backup.sql

# Restore
psql covenant < backup.sql
```
