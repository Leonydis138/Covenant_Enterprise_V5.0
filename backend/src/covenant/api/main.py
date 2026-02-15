"""
FastAPI Application - Production Ready
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uvicorn

from covenant.core.engine import create_engine, Action, VerificationLevel

app = FastAPI(
    title="COVENANT.AI v5.0",
    description="Ultimate Constitutional AI Platform",
    version="5.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Global engine instance
engine = create_engine()

class EvaluateRequest(BaseModel):
    action_type: str
    description: str
    actor: str = "system"
    parameters: Dict[str, Any] = {}
    context: Dict[str, Any] = {}
    verification_level: str = "STANDARD"

@app.get("/")
async def root():
    return {
        "name": "COVENANT.AI Ultimate",
        "version": "5.0.0",
        "status": "operational",
        "features": [
            "Multi-agent swarm intelligence",
            "5-level verification",
            "Blockchain proofs",
            "Real-time analytics",
            "Auto-scaling ready"
        ]
    }

@app.get("/health")
async def health():
    return engine.get_health()

@app.post("/api/v1/evaluate")
async def evaluate(request: EvaluateRequest):
    """Evaluate action through constitutional framework"""
    action = Action(
        type=request.action_type,
        description=request.description,
        actor=request.actor,
        parameters=request.parameters,
        context=request.context
    )
    
    try:
        level = VerificationLevel[request.verification_level]
    except KeyError:
        level = VerificationLevel.STANDARD
    
    result = await engine.evaluate(action, level)
    return result.to_dict()

@app.get("/api/v1/metrics")
async def get_metrics():
    """Get engine metrics"""
    return engine.get_metrics()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)