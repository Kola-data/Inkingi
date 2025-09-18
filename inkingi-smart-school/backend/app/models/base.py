"""
Base model with common fields
"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

# Create a separate base for the models module
_Base = declarative_base()


class TimestampMixin:
    """Mixin for timestamp fields"""
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class BaseModel(_Base, TimestampMixin):
    """Base model with ID and timestamps"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)