"""
Infographics API routes for serving static files with security.
"""

import logging
import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..database import get_db
from ..models.user import User
from ..utils.security import verify_token

logger = logging.getLogger(__name__)
infographics_router = APIRouter()
security = HTTPBearer()


@infographics_router.get("/", response_class=HTMLResponse)
async def serve_infographic(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db),
):
    """Serve the main infographic HTML file with authentication."""
    try:
        # Verify authentication
        token = credentials.credentials
        payload = verify_token(token)
        email = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        # Get user from database
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        # Check if user has permission to view infographics
        if user.role not in ["admin", "lawyer", "client"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )

        # Log access for audit
        logger.info(f"Infographic accessed by user: {email} (role: {user.role})")

        # Serve the infographic HTML file
        infographic_path = Path("public/infographic.html")
        if not infographic_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Infographic file not found",
            )

        # Read and return the HTML content
        with open(infographic_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        return HTMLResponse(content=html_content)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving infographic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@infographics_router.get("/public", response_class=HTMLResponse)
async def serve_public_infographic(request: Request):
    """Serve the infographic HTML file without authentication (public access)."""
    try:
        # Log public access
        client_ip = request.client.host
        logger.info(f"Public infographic accessed from IP: {client_ip}")

        # Serve the infographic HTML file
        infographic_path = Path("public/infographic.html")
        if not infographic_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Infographic file not found",
            )

        # Read and return the HTML content
        with open(infographic_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        return HTMLResponse(content=html_content)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving public infographic: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
