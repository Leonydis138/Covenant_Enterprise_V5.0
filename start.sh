#!/bin/bash
# Start COVENANT.AI Enterprise + NEXUS v8.0

set -euo pipefail

echo "Starting COVENANT.AI Enterprise v5.0 + NEXUS v8.0..."

# Kill any previous instances on our ports so restarts are clean
fuser -k 8000/tcp 2>/dev/null || true
fuser -k 5000/tcp 2>/dev/null || true
sleep 1

# Start backend in background
cd /home/JuiceSSH/Covenant_Enterprise_V5.0/backend
uvicorn src.covenant.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
echo "Backend started (PID $BACKEND_PID) on :8000"

# Start frontend (Vite dev server on port 5000)
cd /home/JuiceSSH/Covenant_Enterprise_V5.0/frontend
npm run dev

