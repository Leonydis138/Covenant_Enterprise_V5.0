"""Core API routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from datetime import datetime
from pydantic import BaseModel

from covenant.core.constitutional_engine import Action, create_engine

router = APIRouter()

class EvaluateRequest(BaseModel):
    action: Dict[str, Any]
    constraints: list[str] = []

class EvaluateResponse(BaseModel):
    is_allowed: bool
    score: float
    violations: list[Dict[str, Any]]
    warnings: list[Dict[str, Any]]
    evaluation_time_ms: float
    audit_id: str

@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_action(request: EvaluateRequest):
    """Evaluate an action through constitutional layers"""
    # Create action
    action = Action(
        type=request.action.get("type", "generic"),
        description=request.action.get("description", ""),
        actor=request.action.get("actor", "system"),
        parameters=request.action.get("parameters", {}),
        context=request.action.get("context", {})
    )
    
    # Get engine from app state
    engine = create_engine()
    
    # Evaluate
    result = await engine.evaluate_action(action)
    
    return EvaluateResponse(
        is_allowed=result.is_allowed,
        score=result.overall_score,
        violations=[v.to_dict() for v in result.violations],
        warnings=result.warnings,
        evaluation_time_ms=result.evaluation_time_ms,
        audit_id=result.audit_id
    )

@router.get("/metrics")
async def get_metrics():
    """Get engine metrics"""
    engine = create_engine()
    return engine.get_metrics()

@router.get("/compliance/report")
async def get_compliance_report(bundle: str = "all"):
    """Get compliance report"""
    engine = create_engine()
    return engine.get_compliance_report(bundle=bundle)