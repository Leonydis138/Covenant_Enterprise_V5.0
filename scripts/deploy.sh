#!/bin/bash
# Production deployment script

set -e

#!/bin/bash
# Production deployment script - COVENANT.AI Enterprise v5.0

set -euo pipefail

echo "🚀 Deploying COVENANT.AI Enterprise v5.0"
echo "=========================================="

# Build images
echo "Building Docker images..."
docker compose -f docker-compose.yml build

# Tag images
echo "Tagging images..."
docker tag covenant-enterprise-backend:latest "${REGISTRY:-gcr.io}/covenant-api:5.0.0"

# Push to registry
echo "Pushing to registry..."
docker push "${REGISTRY:-gcr.io}/covenant-api:5.0.0"

# Deploy to Kubernetes
echo "Deploying to Kubernetes..."
kubectl apply -f infrastructure/kubernetes/

# Wait for rollout
echo "Waiting for rollout..."
kubectl rollout status deployment/covenant-api

echo "✅ Deployment complete!"
