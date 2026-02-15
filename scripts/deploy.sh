#!/bin/bash
# Production deployment script

set -e

echo "🚀 Deploying COVENANT.AI Enterprise v3.0"
echo "========================================"

# Build images
echo "Building Docker images..."
docker-compose -f docker-compose.full.yml build

# Tag images
echo "Tagging images..."
docker tag covenant-api:latest gcr.io/your-project/covenant-api:3.0.0

# Push to registry
echo "Pushing to registry..."
docker push gcr.io/your-project/covenant-api:3.0.0

# Deploy to Kubernetes
echo "Deploying to Kubernetes..."
kubectl apply -f infrastructure/kubernetes/

# Wait for rollout
echo "Waiting for rollout..."
kubectl rollout status deployment/covenant-api

echo "✅ Deployment complete!"