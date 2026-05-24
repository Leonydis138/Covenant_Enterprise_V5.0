"""Core API routes"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
from datetime import datetime
from pydantic import BaseModel
import logging

from covenant.core.constitutional_engine import Action, create_engine

logger = logging.getLogger(__name__)
router = APIRouter()


class EvaluateRequest(BaseModel):
    """Request model for action evaluation"""
    action: Dict[str, Any]
    constraints: list[str] = []


class EvaluateResponse(BaseModel):
    """Response model for action evaluation"""
    is_allowed: bool
    score: float
    violations: list[Dict[str, Any]]
    warnings: list[Dict[str, Any]]
    evaluation_time_ms: float
    audit_id: str


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_action(request: EvaluateRequest) -> EvaluateResponse:
    """Evaluate an action through constitutional layers"""
    try:
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
    except Exception as e:
        logger.error(f"Error evaluating action: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation failed: {str(e)}"
        )


@router.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """Get engine metrics"""
    try:
        engine = create_engine()
        return engine.get_metrics()
    except Exception as e:
        logger.error(f"Error retrieving metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve metrics"
        )


@router.get("/compliance/report")
async def get_compliance_report(bundle: str = "all") -> Dict[str, Any]:
    """Get compliance report"""
    try:
        engine = create_engine()
        return engine.get_compliance_report(bundle=bundle)
    except ValueError as e:
        logger.warning(f"Invalid compliance bundle: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid bundle: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error generating compliance report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate compliance report"
        )
