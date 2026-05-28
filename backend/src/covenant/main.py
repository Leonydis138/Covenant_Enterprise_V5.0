"""
COVENANT.AI Enterprise v5.0 - Main Application
Production-ready FastAPI application with advanced constitutional AI features.
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Any
from time import time
from uuid import uuid4

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from prometheus_client import make_asgi_app
import uvicorn
from sqlalchemy import text

from covenant.api import routes
from covenant.api import enterprise_routes
from covenant.api import admin_routes
from covenant.api import auth_routes
from covenant.api import nexus_routes
from covenant.core.constitutional_engine import create_engine
from covenant.utils.logging_config import setup_logging
from covenant.utils.config import settings
from covenant.monitoring.metrics import setup_metrics
from covenant.db.session import engine as db_engine, init_db

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Global engine instance
constitutional_engine = None
rate_limit_store: dict[str, tuple[float, int]] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global constitutional_engine

    app.state.started_at = datetime.now(timezone.utc)
    app.state.db_available = True

    logger.info("🚀 Starting COVENANT.AI Enterprise v5.0")
    
    # Initialize database (non-fatal if unavailable - runs in degraded mode)
    try:
        await init_db()
        logger.info("✓ Database initialized")
    except Exception as e:
        logger.warning(f"⚠ Database unavailable (running in degraded mode): {e}")
        app.state.db_available = False
    
    # Initialize constitutional engine
    constitutional_engine = create_engine({
        "environment": settings.APP_ENV,
        "enable_formal_verification": True,
        "enable_neural_symbolic": True,
        "enable_causal_inference": True,
        "enable_quantum_optimization": settings.ENABLE_QUANTUM_OPTIMIZATION,
    })
    app.state.engine = constitutional_engine
    logger.info("✓ Constitutional engine initialized")
    
    # Setup metrics
    setup_metrics(app)
    logger.info("✓ Metrics configured")
    
    logger.info("✓ Application startup complete")
    
    yield
    
    # Cleanup
    logger.info("Shutting down application...")
    await db_engine.dispose()


# Create FastAPI application
app = FastAPI(
    title="COVENANT.AI Enterprise",
    description="Constitutional Alignment Framework for Autonomous Intelligence v5.0",
    version="5.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

if settings.APP_ENV == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )


@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """Attach baseline security and traceability headers."""
    response = await call_next(request)
    request_id = request.headers.get("x-request-id", str(uuid4()))
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if settings.APP_ENV == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Simple in-memory rate limiter for baseline abuse protection."""
    if not settings.RATE_LIMIT_ENABLED:
        return await call_next(request)

    path = request.url.path
    if path.startswith("/health") or path.startswith("/metrics"):
        return await call_next(request)

    now = time()
    ip = request.client.host if request.client else "unknown"
    window_start, count = rate_limit_store.get(ip, (now, 0))
    if now - window_start > settings.RATE_LIMIT_WINDOW_SECONDS:
        window_start, count = now, 0

    count += 1
    rate_limit_store[ip] = (window_start, count)

    remaining = settings.RATE_LIMIT_MAX_REQUESTS - count
    if count > settings.RATE_LIMIT_MAX_REQUESTS:
        retry_after = max(1, int(settings.RATE_LIMIT_WINDOW_SECONDS - (now - window_start)))
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded", "type": "rate_limit_exceeded"},
            headers={"Retry-After": str(retry_after)},
        )

    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_MAX_REQUESTS)
    response.headers["X-RateLimit-Remaining"] = str(max(0, remaining))
    return response


# Custom exception handler
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Custom HTTP exception handler with logging"""
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return await http_exception_handler(request, exc)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error", "type": "internal_error"}
    )


# Health check endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    now = datetime.now(timezone.utc)
    started_at = getattr(app.state, "started_at", now)
    db_available = bool(getattr(app.state, "db_available", False))
    status_value = "healthy" if db_available else "degraded"

    return {
        "status": status_value,
        "version": "5.0.0",
        "tier": "enterprise",
        "timestamp": str(now),
        "uptime_seconds": max(0, int((now - started_at).total_seconds())),
        "checks": {
            "database": "ok" if db_available else "unavailable"
        }
    }


@app.get("/health/ready", tags=["Health"])
async def readiness_check():
    """Readiness check for Kubernetes"""
    if not getattr(app.state, "db_available", False):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "checks": {"database": "unavailable"}},
        )

    try:
        # Check database
        async with db_engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        
        return {"status": "ready", "checks": {"database": "ok"}}
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "error": "Readiness check failed"}
        )


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "COVENANT.AI Enterprise",
        "version": "5.0.0",
        "description": "Constitutional Alignment Framework for Autonomous Intelligence",
        "features": [
            "Multi-layer constitutional verification",
            "Neural-symbolic reasoning",
            "Formal verification (Z3/SMT)",
            "Causal inference engine",
            "Quantum-inspired optimization",
            "Blockchain audit trails",
            "Real-time compliance monitoring",
            "Advanced ML/AI safety",
            "Zero-trust security",
            "Auto-scaling infrastructure"
        ],
        "endpoints": {
            "documentation": "/api/docs",
            "api": "/api/v1",
            "metrics": "/metrics",
            "health": "/health"
        }
    }


# Include routers
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(routes.router, prefix="/api/v1", tags=["Core"])
app.include_router(enterprise_routes.router, prefix="/api/v1/enterprise", tags=["Enterprise"])
app.include_router(admin_routes.router, prefix="/api/v1/admin", tags=["Admin"])
app.include_router(nexus_routes.router, prefix="/api", tags=["NEXUS v8"])

# Metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=None,  # Use custom logging
        access_log=True
    )