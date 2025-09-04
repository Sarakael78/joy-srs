"""
Main FastAPI application for the Legal Strategy Infographics Platform.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Legal Strategy Infographics Platform")
    logger.info("Running in serverless mode")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Legal Strategy Infographics Platform")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="Legal Strategy Infographics",
        description="Secure legal strategy infographics platform",
        version="0.1.0",
        lifespan=lifespan,
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint for load balancers."""
        return {
            "status": "healthy",
            "version": "0.1.0",
            "timestamp": "2024-01-01T00:00:00Z",
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
    
    # Public infographic endpoint
    @app.get("/infographics/public", response_class=HTMLResponse)
    async def public_infographic():
        """Serve the infographic HTML file without authentication."""
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
            logger.error(f"Error serving public infographic: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """Global exception handler for security."""
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )
    
    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    uvicorn.run(
        "legal_infographics.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
