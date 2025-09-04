"""
Case model for legal case management.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CaseStatus(str, Enum):
    """Case status enumeration."""
    
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    CLOSED = "closed"
    ARCHIVED = "archived"


class CaseType(str, Enum):
    """Case type enumeration."""
    
    CIVIL = "civil"
    CRIMINAL = "criminal"
    FAMILY = "family"
    CORPORATE = "corporate"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    LABOR = "labor"
    TAX = "tax"
    OTHER = "other"


class Case(Base):
    """Legal case model."""
    
    __tablename__ = "cases"
    
    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    type = Column(SQLEnum(CaseType), default=CaseType.OTHER, nullable=False)
    status = Column(SQLEnum(CaseStatus), default=CaseStatus.OPEN, nullable=False)
    
    # Case details
    filing_date = Column(DateTime, nullable=True)
    court_name = Column(String(200), nullable=True)
    judge_name = Column(String(200), nullable=True)
    opposing_party = Column(String(200), nullable=True)
    opposing_counsel = Column(String(200), nullable=True)
    
    # Financial information
    estimated_value = Column(Integer, nullable=True)  # In cents
    actual_costs = Column(Integer, nullable=True)  # In cents
    billing_rate = Column(Integer, nullable=True)  # In cents per hour
    
    # Security
    is_confidential = Column(Boolean, default=True, nullable=False)
    confidentiality_level = Column(String(50), default="high", nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    closed_at = Column(DateTime, nullable=True)
    
    # Relationships
    participants = relationship("CaseParticipant", back_populates="case", cascade="all, delete-orphan")
    infographics = relationship("Infographic", back_populates="case")
    
    def __repr__(self) -> str:
        return f"<Case(id={self.id}, case_number='{self.case_number}', title='{self.title}')>"
    
    @property
    def is_active(self) -> bool:
        """Check if the case is active."""
        return self.status in [CaseStatus.OPEN, CaseStatus.IN_PROGRESS, CaseStatus.PENDING_REVIEW]
    
    @property
    def total_participants(self) -> int:
        """Get the total number of participants."""
        return len(self.participants)
    
    def get_participants_by_role(self, role: str) -> list["CaseParticipant"]:
        """Get participants by their role."""
        return [p for p in self.participants if p.role == role]


class CaseParticipant(Base):
    """Case participant model for managing case access."""
    
    __tablename__ = "case_participants"
    
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Role and permissions
    role = Column(String(50), nullable=False)  # lead_lawyer, associate, client, expert, etc.
    can_view_case = Column(Boolean, default=True, nullable=False)
    can_edit_case = Column(Boolean, default=False, nullable=False)
    can_manage_participants = Column(Boolean, default=False, nullable=False)
    can_view_financials = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    joined_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    left_at = Column(DateTime, nullable=True)
    
    # Relationships
    case = relationship("Case", back_populates="participants")
    user = relationship("User", back_populates="cases")
    
    def __repr__(self) -> str:
        return f"<CaseParticipant(id={self.id}, case_id={self.case_id}, user_id={self.user_id}, role='{self.role}')>"
    
    @property
    def is_active(self) -> bool:
        """Check if the participant is still active in the case."""
        return self.left_at is None
