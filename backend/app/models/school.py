from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class School(BaseModel):
    __tablename__ = "schools"
    
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(String(20), default="pending")  # pending, active, suspended, inactive
    verified_at = Column(DateTime(timezone=True), nullable=True)
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(20), nullable=True)
    address = Column(JSON, nullable=True)
    logo_url = Column(String(500), nullable=True)
    website = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    staff = relationship("Staff", back_populates="school")
    users = relationship("User", back_populates="school")
    academic_years = relationship("AcademicYear", back_populates="school")
    classes = relationship("Class", back_populates="school")
    courses = relationship("Course", back_populates="school")
    students = relationship("Student", back_populates="school")
    parents = relationship("Parent", back_populates="school")