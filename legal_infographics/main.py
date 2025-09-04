"""
Main FastAPI application for the Legal Strategy Infographics Platform.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer

from .api import (
    audit_router,
    auth_router,
    cases_router,
    infographics_router,
    users_router,
)
from .config import settings
from .database import get_db, init_db
from .middleware import AuditMiddleware, RateLimitMiddleware, SecurityMiddleware
from .utils.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Legal Strategy Infographics Platform")
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.warning(f"Database initialization failed: {e}")

    yield

    # Shutdown
    logger.info("Shutting down Legal Strategy Infographics Platform")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=settings.app_name,
        description="Secure legal strategy infographics platform for lawyers and clients",
        version="0.1.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan,
    )

    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"],
    )

    app.add_middleware(SecurityMiddleware)
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(AuditMiddleware)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
    app.include_router(
        infographics_router, prefix="/infographics", tags=["Infographics"]
    )
    app.include_router(cases_router, prefix="/cases", tags=["Cases"])
    app.include_router(users_router, prefix="/users", tags=["Users"])
    app.include_router(audit_router, prefix="/audit", tags=["Audit"])

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint for load balancers."""
        return {
            "status": "healthy",
            "version": "0.1.0",
            "timestamp": "2024-01-01T00:00:00Z",
        }

    # Metrics endpoint
    @app.get("/metrics", tags=["Monitoring"])
    async def metrics():
        """Prometheus metrics endpoint."""
        return {
            "requests_total": 0,
            "requests_duration_seconds": 0,
            "active_users": 0,
            "infographics_total": 0,
            "cases_total": 0,
        }

    # Root endpoint - serve infographic
    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Serve the main infographic HTML file."""
        try:
            infographic_path = Path("public/infographic.html")
            if not infographic_path.exists():
                raise HTTPException(
                    status_code=404, detail="Infographic file not found"
                )

            with open(infographic_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            return HTMLResponse(content=html_content)

        except Exception as e:
            logger.error(f"Error serving infographic: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler for security."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)

        # Don't expose internal errors in production
        if settings.debug:
            return JSONResponse(status_code=500, content={"detail": str(exc)})
        else:
            return JSONResponse(
                status_code=500, content={"detail": "Internal server error"}
            )

    # Security headers middleware
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        """Add security headers to all responses."""
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com;"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )

        return response

    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "legal_infographics.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.monitoring.log_level.lower(),
    )
