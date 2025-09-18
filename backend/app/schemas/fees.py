from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import date

class FeeStructureBase(BaseModel):
    name: str
    description: Optional[str] = None
    amount: float
    currency: str = "USD"
    due_date: Optional[date] = None
    is_mandatory: bool = True
    payment_terms: Optional[Dict[str, Any]] = None

class FeeStructureCreate(FeeStructureBase):
    academic_year_id: int
    class_id: Optional[int] = None

class FeeStructureUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    amount: Optional[float] = None
    currency: Optional[str] = None
    due_date: Optional[date] = None
    is_mandatory: Optional[bool] = None
    payment_terms: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class FeeStructureResponse(FeeStructureBase):
    id: int
    school_id: int
    academic_year_id: int
    class_id: Optional[int]
    status: str
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True

class FeeBase(BaseModel):
    amount: float
    currency: str = "USD"
    due_date: Optional[date] = None
    notes: Optional[str] = None

class FeeCreate(FeeBase):
    student_id: int
    fee_structure_id: int

class FeeUpdate(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class FeeResponse(FeeBase):
    id: int
    school_id: int
    student_id: int
    fee_structure_id: int
    status: str
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True