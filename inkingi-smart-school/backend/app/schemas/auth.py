"""
Authentication schemas
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str
    expires_in: int


class TokenPayload(BaseModel):
    """Token payload schema"""
    sub: Optional[str] = None
    tenant_id: Optional[int] = None
    email: Optional[str] = None


class UserBase(BaseModel):
    """User base schema"""
    email: EmailStr
    phone: Optional[str] = None


class UserCreate(UserBase):
    """User creation schema"""
    password: str
    school_id: int
    staff_id: Optional[int] = None


class UserUpdate(BaseModel):
    """User update schema"""
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[str] = None


class UserResponse(UserBase):
    """User response schema"""
    id: int
    school_id: int
    staff_id: Optional[int] = None
    status: str
    roles: List[str] = []
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        """Convert from ORM object"""
        data = {
            "id": obj.id,
            "email": obj.email,
            "phone": obj.phone,
            "school_id": obj.school_id,
            "staff_id": obj.staff_id,
            "status": obj.status,
            "roles": [role.name for role in obj.roles] if obj.roles else []
        }
        return cls(**data)