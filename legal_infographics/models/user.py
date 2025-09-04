"""
User model with role-based access control and security features.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserRole(str, Enum):
    """User roles with different permission levels."""
    
    ADMIN = "admin"
    LAWYER = "lawyer"
    CLIENT = "client"
    VIEWER = "viewer"


class User(Base):
    """User model with authentication and authorization."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(String(20), default=UserRole.VIEWER, nullable=False)
    
    # Security features
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    mfa_enabled = Column(Boolean, default=False, nullable=False)
    mfa_secret = Column(String(255), nullable=True)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    password_changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Profile information
    phone = Column(String(20), nullable=True)
    organization = Column(String(200), nullable=True)
    position = Column(String(100), nullable=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    
    # Relationships
    cases = relationship("CaseParticipant", back_populates="user")
    created_infographics = relationship("Infographic", back_populates="creator")
    infographic_permissions = relationship("InfographicPermission", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
    
    @property
    def full_name(self) -> str:
        """Get the user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_locked(self) -> bool:
        """Check if the user account is locked."""
        if self.locked_until is None:
            return False
        return datetime.utcnow() < self.locked_until
    
    def can_access_infographic(self, infographic_id: int) -> bool:
        """Check if user can access a specific infographic."""
        if self.role == UserRole.ADMIN:
            return True
        
        # Check direct permissions
        for permission in self.infographic_permissions:
            if permission.infographic_id == infographic_id:
                return permission.can_view
        
        # Check case-based permissions
        for case_participant in self.cases:
            for infographic in case_participant.case.infographics:
                if infographic.id == infographic_id:
                    return True
        
        return False
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission."""
        if self.role == UserRole.ADMIN:
            return True
        
        permission_map = {
            UserRole.LAWYER: [
                "create_infographic",
                "edit_infographic", 
                "delete_infographic",
                "view_all_cases",
                "manage_clients"
            ],
            UserRole.CLIENT: [
                "view_assigned_infographics",
                "view_own_case"
            ],
            UserRole.VIEWER: [
                "view_public_infographics"
            ]
        }
        
        return permission in permission_map.get(self.role, [])
