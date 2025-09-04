"""
Main FastAPI application for the Legal Strategy Infographics Platform.
"""

import logging
import os
import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Depends, status, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User management
def get_users() -> Dict[str, str]:
    """Get users from environment variable."""
    users_json = os.getenv("USERS", "{}")
    try:
        return json.loads(users_json)
    except json.JSONDecodeError:
        return {}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user with username and password."""
    users = get_users()
    if username not in users:
        return False
    return verify_password(password, users[username])

def create_access_token(username: str) -> str:
    """Create a simple access token."""
    # In a real app, you'd use JWT tokens
    return f"user_{username}_token"

def verify_token(token: str) -> Optional[str]:
    """Verify a token and return username."""
    if token.startswith("user_") and token.endswith("_token"):
        return token[5:-6]  # Extract username from token
    return None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting Legal Strategy Infographics Platform")
    logger.info("Running in serverless mode with user authentication")
    
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
    
    # Login endpoint
    @app.post("/auth/login")
    async def login(username: str = Form(...), password: str = Form(...)):
        """Authenticate user and return access token."""
        if authenticate_user(username, password):
            token = create_access_token(username)
            logger.info(f"Successful login for user: {username}")
            return {"access_token": token, "token_type": "bearer", "username": username}
        else:
            logger.warning(f"Failed login attempt for user: {username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
    
    # Get current user endpoint
    @app.get("/auth/me")
    async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
        """Get current authenticated user."""
        username = verify_token(credentials.credentials)
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return {"username": username}
    
    # Root endpoint - serve infographic (public)
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
    
    # Protected infographic endpoint
    @app.get("/infographics/", response_class=HTMLResponse)
    async def protected_infographic(credentials: HTTPAuthorizationCredentials = Depends(security)):
        """Serve the infographic HTML file with user authentication."""
        try:
            username = verify_token(credentials.credentials)
            if not username:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token"
                )
            
            logger.info(f"Protected infographic accessed by user: {username}")
            
            infographic_path = Path("public/infographic.html")
            if not infographic_path.exists():
                raise HTTPException(
                    status_code=404, detail="Infographic file not found"
                )
            
            with open(infographic_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            
            return HTMLResponse(content=html_content)
            
        except Exception as e:
            logger.error(f"Error serving protected infographic: {str(e)}")
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
