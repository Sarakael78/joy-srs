"""
Authentication API routes with security features.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from ..database import get_db
from ..models.user import User
from ..utils.security import create_access_token, verify_password, verify_token

logger = logging.getLogger(__name__)
auth_router = APIRouter()
security = HTTPBearer()


class LoginRequest(BaseModel):
    email: str
    password: str
    mfa_code: Optional[str] = None


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    role: str


@auth_router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db=Depends(get_db)):
    """Authenticate user and return JWT token."""
    try:
        # Find user by email
        user = db.query(User).filter(User.email == request.email).first()
        if not user:
            logger.warning(f"Login attempt with non-existent email: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        # Verify password
        if not verify_password(request.password, user.password_hash):
            logger.warning(f"Failed login attempt for user: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        # Check MFA if enabled
        if user.mfa_enabled:
            if not request.mfa_code:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="MFA code required"
                )
            # TODO: Implement MFA verification
            pass

        # Create access token
        access_token = create_access_token(data={"sub": user.email})

        logger.info(f"Successful login for user: {request.email}")

        return LoginResponse(
            access_token=access_token, user_id=user.id, email=user.email, role=user.role
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@auth_router.get("/me")
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)
):
    """Get current authenticated user."""
    try:
        token = credentials.credentials
        payload = verify_token(token)
        email = payload.get("sub")

        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "mfa_enabled": user.mfa_enabled,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
