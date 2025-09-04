"""
Cases API routes.
"""

from fastapi import APIRouter

cases_router = APIRouter()


@cases_router.get("/")
async def list_cases():
    """List all cases."""
    return {"message": "Cases endpoint - to be implemented"}
