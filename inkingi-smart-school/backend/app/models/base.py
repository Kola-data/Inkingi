from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from app.core.database import Base
import uuid


class BaseModel(Base):
    """Base model with common fields"""
    __abstract__ = True
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
    
    def dict(self):
        """Convert model to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TenantModel(BaseModel):
    """Base model for tenant-specific tables"""
    __abstract__ = True
    
    @declared_attr
    def school_id(cls):
        return Column(
            UUID(as_uuid=True),
            nullable=False,
            index=True
        )