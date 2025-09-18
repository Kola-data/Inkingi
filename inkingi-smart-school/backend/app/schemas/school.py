"""
School schemas
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr


class SchoolBase(BaseModel):
    """School base schema"""
    name: str
    slug: str
    contact_email: EmailStr
    contact_phone: Optional[str] = None
    address_json: Optional[Dict[str, Any]] = None


class SchoolCreate(SchoolBase):
    """School creation schema"""
    pass


class SchoolUpdate(BaseModel):
    """School update schema"""
    name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address_json: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class SchoolResponse(SchoolBase):
    """School response schema"""
    id: int
    status: str
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True