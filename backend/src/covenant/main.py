"""
COVENANT.AI Enterprise v3.0 - Main Application
Production-ready FastAPI application with advanced features
"""

import logging
import sys
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException
from prometheus_client import make_asgi_app
import uvicorn

from covenant.api import routes
from covenant.api import enterprise_routes
from covenant.api import admin_routes
from covenant.api import auth_routes
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global constitutional_engine
    
    logger.info("🚀 Starting COVENANT.AI Enterprise v3.0")
    
    # Initialize database
    try:
        await init_db()
        logger.info("✓ Database initialized")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        sys.exit(1)
    
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
    description="Constitutional Alignment Framework for Autonomous Intelligence v3.0",
    version="3.0.0",
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
    return {
        "status": "healthy",
        "version": "3.0.0",
        "tier": "enterprise",
        "timestamp": str(datetime.utcnow())
    }


@app.get("/health/ready", tags=["Health"])
async def readiness_check():
    """Readiness check for Kubernetes"""
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
        "version": "3.0.0",
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
