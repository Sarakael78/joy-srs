"""
Infographic model with version control and permission management.
"""

from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class InfographicStatus(str, Enum):
    """Infographic status enumeration."""
    
    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class InfographicType(str, Enum):
    """Infographic type enumeration."""
    
    CASE_STRATEGY = "case_strategy"
    EVIDENCE_FLOW = "evidence_flow"
    TIMELINE = "timeline"
    DECISION_TREE = "decision_tree"
    RISK_ASSESSMENT = "risk_assessment"
    COST_ANALYSIS = "cost_analysis"
    COMPARISON_CHART = "comparison_chart"
    CUSTOM = "custom"


class Infographic(Base):
    """Infographic model with version control."""
    
    __tablename__ = "infographics"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String(50), default=InfographicType.CUSTOM, nullable=False)
    status = Column(String(20), default=InfographicStatus.DRAFT, nullable=False)
    
    # Content and data
    content = Column(JSON, nullable=False)  # Chart configuration and data
    metadata = Column(JSON, nullable=True)  # Additional metadata
    tags = Column(JSON, nullable=True)  # Array of tags
    
    # File information
    file_path = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)
    file_type = Column(String(50), nullable=True)
    
    # Security and access
    is_public = Column(Boolean, default=False, nullable=False)
    is_encrypted = Column(Boolean, default=True, nullable=False)
    encryption_key_id = Column(String(255), nullable=True)
    
    # Relationships
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    published_at = Column(DateTime, nullable=True)
    
    # Relationships
    creator = relationship("User", back_populates="created_infographics")
    case = relationship("Case", back_populates="infographics")
    versions = relationship("InfographicVersion", back_populates="infographic", cascade="all, delete-orphan")
    permissions = relationship("InfographicPermission", back_populates="infographic", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Infographic(id={self.id}, title='{self.title}', type='{self.type}')>"
    
    @property
    def current_version(self) -> Optional["InfographicVersion"]:
        """Get the current version of the infographic."""
        if self.versions:
            return max(self.versions, key=lambda v: v.version_number)
        return None
    
    @property
    def version_count(self) -> int:
        """Get the total number of versions."""
        return len(self.versions)
    
    def create_version(self, content: Dict[str, Any], description: str = None) -> "InfographicVersion":
        """Create a new version of the infographic."""
        version_number = self.version_count + 1
        version = InfographicVersion(
            infographic_id=self.id,
            version_number=version_number,
            content=content,
            description=description
        )
        return version
    
    def can_be_accessed_by(self, user_id: int, user_role: str) -> bool:
        """Check if a user can access this infographic."""
        if self.is_public:
            return True
        
        if user_role == "admin":
            return True
        
        # Check direct permissions
        for permission in self.permissions:
            if permission.user_id == user_id and permission.can_view:
                return True
        
        return False


class InfographicVersion(Base):
    """Version control for infographics."""
    
    __tablename__ = "infographic_versions"
    
    id = Column(Integer, primary_key=True, index=True)
    infographic_id = Column(Integer, ForeignKey("infographics.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    
    # Version content
    content = Column(JSON, nullable=False)
    description = Column(Text, nullable=True)
    changes_summary = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    infographic = relationship("Infographic", back_populates="versions")
    creator = relationship("User")
    
    def __repr__(self) -> str:
        return f"<InfographicVersion(id={self.id}, infographic_id={self.infographic_id}, version={self.version_number})>"


class InfographicPermission(Base):
    """Granular permissions for infographic access."""
    
    __tablename__ = "infographic_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    infographic_id = Column(Integer, ForeignKey("infographics.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Permissions
    can_view = Column(Boolean, default=False, nullable=False)
    can_edit = Column(Boolean, default=False, nullable=False)
    can_delete = Column(Boolean, default=False, nullable=False)
    can_share = Column(Boolean, default=False, nullable=False)
    can_export = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    infographic = relationship("Infographic", back_populates="permissions")
    user = relationship("User", back_populates="infographic_permissions")
    
    def __repr__(self) -> str:
        return f"<InfographicPermission(id={self.id}, infographic_id={self.infographic_id}, user_id={self.user_id})>"
    
    @property
    def is_expired(self) -> bool:
        """Check if the permission has expired."""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
