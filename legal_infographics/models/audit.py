"""
Audit logging model for comprehensive activity tracking and compliance.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class AuditAction(str, Enum):
    """Audit action enumeration."""
    
    # User actions
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_CREATE = "user_create"
    USER_UPDATE = "user_update"
    USER_DELETE = "user_delete"
    USER_PASSWORD_CHANGE = "user_password_change"
    USER_MFA_ENABLE = "user_mfa_enable"
    USER_MFA_DISABLE = "user_mfa_disable"
    
    # Infographic actions
    INFOGRAPHIC_CREATE = "infographic_create"
    INFOGRAPHIC_UPDATE = "infographic_update"
    INFOGRAPHIC_DELETE = "infographic_delete"
    INFOGRAPHIC_VIEW = "infographic_view"
    INFOGRAPHIC_EXPORT = "infographic_export"
    INFOGRAPHIC_SHARE = "infographic_share"
    INFOGRAPHIC_VERSION_CREATE = "infographic_version_create"
    
    # Case actions
    CASE_CREATE = "case_create"
    CASE_UPDATE = "case_update"
    CASE_DELETE = "case_delete"
    CASE_PARTICIPANT_ADD = "case_participant_add"
    CASE_PARTICIPANT_REMOVE = "case_participant_remove"
    
    # Permission actions
    PERMISSION_GRANT = "permission_grant"
    PERMISSION_REVOKE = "permission_revoke"
    PERMISSION_UPDATE = "permission_update"
    
    # System actions
    SYSTEM_BACKUP = "system_backup"
    SYSTEM_RESTORE = "system_restore"
    SYSTEM_CONFIG_UPDATE = "system_config_update"
    SECURITY_ALERT = "security_alert"


class AuditSeverity(str, Enum):
    """Audit severity levels."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AuditLog(Base):
    """Audit log model for tracking all system activities."""
    
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User information
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null for system actions
    user_ip = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(Text, nullable=True)
    session_id = Column(String(255), nullable=True)
    
    # Action details
    action = Column(String(100), nullable=False)
    severity = Column(String(20), default=AuditSeverity.LOW, nullable=False)
    resource_type = Column(String(50), nullable=True)  # user, infographic, case, etc.
    resource_id = Column(Integer, nullable=True)
    
    # Action data
    details = Column(JSON, nullable=True)  # Additional action details
    metadata = Column(JSON, nullable=True)  # System metadata
    
    # Timestamps
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action='{self.action}', user_id={self.user_id}, timestamp='{self.timestamp}')>"
    
    @property
    def is_system_action(self) -> bool:
        """Check if this is a system-generated action."""
        return self.user_id is None
    
    @property
    def is_security_related(self) -> bool:
        """Check if this action is security-related."""
        security_actions = [
            AuditAction.USER_LOGIN,
            AuditAction.USER_LOGOUT,
            AuditAction.USER_PASSWORD_CHANGE,
            AuditAction.USER_MFA_ENABLE,
            AuditAction.USER_MFA_DISABLE,
            AuditAction.PERMISSION_GRANT,
            AuditAction.PERMISSION_REVOKE,
            AuditAction.SECURITY_ALERT,
        ]
        return self.action in security_actions
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert audit log to dictionary for export."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_ip": self.user_ip,
            "action": self.action,
            "severity": self.severity,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
        }
