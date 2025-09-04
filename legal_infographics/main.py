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
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import hashlib

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Security
security = HTTPBearer()

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
    try:
        salt, hash_value = hashed_password.split('$')
        computed_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
        return computed_hash == hash_value
    except:
        return False

def get_password_hash(password: str) -> str:
    """Hash a password."""
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"

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
    
    # Login page endpoint (public)
    @app.get("/login", response_class=HTMLResponse)
    async def login_page():
        """Serve the login page."""
        try:
            login_path = Path("public/login.html")
            if not login_path.exists():
                raise HTTPException(
                    status_code=404, detail="Login page not found"
                )
            
            with open(login_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            
            return HTMLResponse(content=html_content)
            
        except Exception as e:
            logger.error(f"Error serving login page: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    # Root endpoint - redirect to login if not authenticated
    @app.get("/", response_class=HTMLResponse)
    async def root(request: Request):
        """Redirect to login page if not authenticated."""
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Redirecting to Login</title>
            <style>
                body { 
                    font-family: 'Inter', Arial, sans-serif; 
                    text-align: center; 
                    padding: 50px; 
                    background-color: #f9fafb;
                    color: #1a3a5a;
                }
                .container {
                    max-width: 400px;
                    margin: 0 auto;
                    background: white;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                    border: 2px solid #4a7a9a;
                }
                h2 { 
                    color: #1a3a5a; 
                    margin-bottom: 1rem;
                    font-weight: 600;
                }
                .spinner { 
                    border: 3px solid #f3f3f3; 
                    border-top: 3px solid #4a7a9a; 
                    border-radius: 50%; 
                    width: 30px; 
                    height: 30px; 
                    animation: spin 1s linear infinite; 
                    margin: 20px auto; 
                }
                @keyframes spin { 
                    0% { transform: rotate(0deg); } 
                    100% { transform: rotate(360deg); } 
                }
                p { 
                    color: #4a7a9a; 
                    margin-bottom: 1rem;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🔐 Authentication Required</h2>
                <div class="spinner"></div>
                <p>Redirecting to login page...</p>
                <script>
                    setTimeout(function() {
                        window.location.href = '/login';
                    }, 1500);
                </script>
            </div>
        </body>
        </html>
        """)
    
    # Protected infographic endpoint
    @app.get("/infographic", response_class=HTMLResponse)
    async def protected_infographic(request: Request):
        """Serve the infographic HTML file with user authentication."""
        try:
            # Check for token in Authorization header or query parameter
            auth_header = request.headers.get("authorization")
            token = None
            
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header[7:]  # Remove "Bearer " prefix
            else:
                # Check for token in query parameter (for simple redirects)
                token = request.query_params.get("token")
            
            if not token:
                # No valid token, redirect to login
                return HTMLResponse(content="""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Redirecting to Login</title>
                    <style>
                        body { 
                            font-family: 'Inter', Arial, sans-serif; 
                            text-align: center; 
                            padding: 50px; 
                            background-color: #f9fafb;
                            color: #1a3a5a;
                        }
                        .container {
                            max-width: 400px;
                            margin: 0 auto;
                            background: white;
                            padding: 2rem;
                            border-radius: 10px;
                            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                            border: 2px solid #4a7a9a;
                        }
                        h2 { 
                            color: #1a3a5a; 
                            margin-bottom: 1rem;
                            font-weight: 600;
                        }
                        .spinner { 
                            border: 3px solid #f3f3f3; 
                            border-top: 3px solid #4a7a9a; 
                            border-radius: 50%; 
                            width: 30px; 
                            height: 30px; 
                            animation: spin 1s linear infinite; 
                            margin: 20px auto; 
                        }
                        @keyframes spin { 
                            0% { transform: rotate(0deg); } 
                            100% { transform: rotate(360deg); } 
                        }
                        p { 
                            color: #4a7a9a; 
                            margin-bottom: 1rem;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>🔐 Authentication Required</h2>
                        <div class="spinner"></div>
                        <p>Redirecting to login page...</p>
                        <script>
                            setTimeout(function() {
                                window.location.href = '/login';
                            }, 1500);
                        </script>
                    </div>
                </body>
                </html>
                """)
            
            username = verify_token(token)
            if not username:
                # Invalid token, redirect to login
                return HTMLResponse(content="""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Redirecting to Login</title>
                    <style>
                        body { 
                            font-family: 'Inter', Arial, sans-serif; 
                            text-align: center; 
                            padding: 50px; 
                            background-color: #f9fafb;
                            color: #1a3a5a;
                        }
                        .container {
                            max-width: 400px;
                            margin: 0 auto;
                            background: white;
                            padding: 2rem;
                            border-radius: 10px;
                            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
                            border: 2px solid #4a7a9a;
                        }
                        h2 { 
                            color: #1a3a5a; 
                            margin-bottom: 1rem;
                            font-weight: 600;
                        }
                        .spinner { 
                            border: 3px solid #f3f3f3; 
                            border-top: 3px solid #4a7a9a; 
                            border-radius: 50%; 
                            width: 30px; 
                            height: 30px; 
                            animation: spin 1s linear infinite; 
                            margin: 20px auto; 
                        }
                        @keyframes spin { 
                            0% { transform: rotate(0deg); } 
                            100% { transform: rotate(360deg); } 
                        }
                        p { 
                            color: #4a7a9a; 
                            margin-bottom: 1rem;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h2>🔐 Invalid Token</h2>
                        <div class="spinner"></div>
                        <p>Redirecting to login page...</p>
                        <script>
                            setTimeout(function() {
                                window.location.href = '/login';
                            }, 1500);
                        </script>
                    </div>
                </body>
                </html>
                """)
            
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
    
    # Static file serving
    @app.get("/{filename:path}")
    async def serve_static_files(filename: str):
        """Serve static files from the public directory."""
        try:
            file_path = Path("public") / filename
            if not file_path.exists():
                raise HTTPException(
                    status_code=404, detail="File not found"
                )
            
            # Only serve files from the public directory
            if not str(file_path).startswith(str(Path("public"))):
                raise HTTPException(
                    status_code=403, detail="Access denied"
                )
            
            return FileResponse(file_path)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error serving static file {filename}: {str(e)}")
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
