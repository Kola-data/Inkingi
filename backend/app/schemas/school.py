from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class SchoolBase(BaseModel):
    name: str
    slug: str
    contact_email: EmailStr
    contact_phone: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    website: Optional[str] = None
    description: Optional[str] = None

class SchoolCreate(SchoolBase):
    pass

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    contact_phone: Optional[str] = None
    address: Optional[Dict[str, Any]] = None
    website: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class SchoolResponse(SchoolBase):
    id: int
    status: str
    verified_at: Optional[datetime]
    logo_url: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True