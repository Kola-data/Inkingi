from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime, date

class StaffBase(BaseModel):
    first_name: str
    last_name: str
    other_names: Optional[str] = None
    gender: str
    date_of_birth: Optional[date] = None
    national_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[Dict[str, Any]] = None
    employment_number: Optional[str] = None
    position: str
    department: Optional[str] = None
    qualification: Optional[str] = None
    hire_date: date
    contract_type: str
    salary: Optional[str] = None
    emergency_contact: Optional[Dict[str, Any]] = None

class StaffCreate(StaffBase):
    pass

class StaffUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    other_names: Optional[str] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    national_id: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[Dict[str, Any]] = None
    employment_number: Optional[str] = None
    position: Optional[str] = None
    department: Optional[str] = None
    qualification: Optional[str] = None
    hire_date: Optional[date] = None
    contract_type: Optional[str] = None
    status: Optional[str] = None
    salary: Optional[str] = None
    emergency_contact: Optional[Dict[str, Any]] = None

class StaffResponse(StaffBase):
    id: int
    school_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True