"""
Users API routes.
"""

from fastapi import APIRouter

users_router = APIRouter()


@users_router.get("/")
async def list_users():
    """List all users."""
    return {"message": "Users endpoint - to be implemented"}
