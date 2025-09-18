from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime, date

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    other_names: Optional[str] = None
    gender: str
    date_of_birth: date
    student_number: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[Dict[str, Any]] = None
    emergency_contact: Optional[Dict[str, Any]] = None
    medical_info: Optional[Dict[str, Any]] = None

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    other_names: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    student_number: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[Dict[str, Any]] = None
    emergency_contact: Optional[Dict[str, Any]] = None
    medical_info: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    school_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ParentBase(BaseModel):
    first_name: str
    last_name: str
    other_names: Optional[str] = None
    gender: str
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[Dict[str, Any]] = None
    occupation: Optional[str] = None
    relationship: Optional[str] = None

class ParentCreate(ParentBase):
    pass

class ParentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    other_names: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[Dict[str, Any]] = None
    occupation: Optional[str] = None
    relationship: Optional[str] = None
    status: Optional[str] = None

class ParentResponse(ParentBase):
    id: int
    school_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True