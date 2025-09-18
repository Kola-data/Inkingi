from sqlalchemy import Column, String, Boolean, DateTime, JSON, Text, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel
import enum


class SchoolStatus(str, enum.Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    INACTIVE = "inactive"


class School(BaseModel):
    __tablename__ = "schools"
    
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    status = Column(SQLEnum(SchoolStatus), default=SchoolStatus.PENDING, nullable=False)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Contact Information
    contact_email = Column(String(255), nullable=False)
    contact_phone = Column(String(50), nullable=False)
    website = Column(String(255), nullable=True)
    
    # Address
    address_json = Column(JSON, nullable=False, default={})
    
    # School Details
    logo_url = Column(String(500), nullable=True)
    motto = Column(String(500), nullable=True)
    founded_year = Column(String(4), nullable=True)
    school_type = Column(String(50), nullable=True)  # primary, secondary, combined
    curriculum = Column(String(100), nullable=True)
    
    # Subscription/Billing
    subscription_plan = Column(String(50), default="free", nullable=False)
    subscription_expires_at = Column(DateTime(timezone=True), nullable=True)
    max_students = Column(String(10), default="100", nullable=False)
    max_staff = Column(String(10), default="20", nullable=False)
    
    # Settings
    settings_json = Column(JSON, nullable=False, default={})
    features_json = Column(JSON, nullable=False, default={})
    
    # Metadata
    notes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<School {self.name} ({self.slug})>"