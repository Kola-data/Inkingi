"""
School model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON
from sqlalchemy.orm import relationship

from .base import BaseModel


class School(BaseModel):
    """School model for multi-tenancy"""
    __tablename__ = "schools"
    
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(String(20), default="pending", nullable=False)  # pending, active, suspended
    verified_at = Column(DateTime, nullable=True)
    
    # Contact information
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(20), nullable=True)
    address_json = Column(JSON, nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="school")
    staff = relationship("Staff", back_populates="school")
    academic_years = relationship("AcademicYear", back_populates="school")
    classes = relationship("Class", back_populates="school")
    
    def __repr__(self):
        return f"<School(id={self.id}, name='{self.name}', slug='{self.slug}')>"