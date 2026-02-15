#!/bin/bash
# Quick start script for COVENANT.AI Enterprise

set -e

echo "🚀 COVENANT.AI Enterprise v3.0 Quick Start"
echo "=========================================="

# Check prerequisites
echo "Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { echo "❌ Docker required"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3.11+ required"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js 20+ required"; exit 1; }
echo "✓ Prerequisites met"

# Create environment file
if [ ! -f backend/.env ]; then
    echo "Creating .env file..."
    cp backend/.env.example backend/.env
    echo "✓ Environment file created"
fi

# Start services
echo "Starting services with Docker Compose..."
docker-compose -f docker-compose.full.yml up -d db redis
sleep 5

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -q -r requirements.txt
cd ..

# Install frontend dependencies  
echo "Installing frontend dependencies..."
cd frontend
npm install --silent
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Start backend:  cd backend && uvicorn covenant.main:app --reload"
echo "  2. Start frontend: cd frontend && npm run dev"
echo ""
echo "Access points:"
echo "  - API:       http://localhost:8000"
echo "  - Docs:      http://localhost:8000/api/docs"
echo "  - Dashboard: http://localhost:5173"
echo "  - Metrics:   http://localhost:9090"
echo ""