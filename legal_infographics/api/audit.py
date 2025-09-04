"""
Audit API routes.
"""

from fastapi import APIRouter

audit_router = APIRouter()


@audit_router.get("/")
async def list_audit_logs():
    """List audit logs."""
    return {"message": "Audit endpoint - to be implemented"}
