"""
API routes for the Legal Strategy Infographics Platform.
"""

from .audit import audit_router
from .auth import auth_router
from .cases import cases_router
from .infographics import infographics_router
from .users import users_router

__all__ = [
    "auth_router",
    "infographics_router",
    "cases_router",
    "users_router",
    "audit_router",
]
