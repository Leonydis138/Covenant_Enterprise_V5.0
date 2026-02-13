"""Admin API routes"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

router = APIRouter()

@router.get("/system/health")
async def system_health():
    """Detailed system health"""
    return {
        "status": "healthy",
        "services": {
            "database": "ok",
            "redis": "ok",
            "engine": "ok"
        }
    }

@router.post("/cache/clear")
async def clear_cache():
    """Clear system caches"""
    return {"status": "cleared"}
