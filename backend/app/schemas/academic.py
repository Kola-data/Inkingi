from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class AcademicYearBase(BaseModel):
    name: str
    start_date: date
    end_date: date

class AcademicYearCreate(AcademicYearBase):
    pass

class AcademicYearUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None

class AcademicYearResponse(AcademicYearBase):
    id: int
    school_id: int
    is_current: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class TermBase(BaseModel):
    name: str
    start_date: date
    end_date: date
    order_index: int

class TermCreate(TermBase):
    academic_year_id: int

class TermUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    order_index: Optional[int] = None
    is_current: Optional[bool] = None
    locked: Optional[bool] = None

class TermResponse(TermBase):
    id: int
    school_id: int
    academic_year_id: int
    is_current: bool
    locked: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ClassBase(BaseModel):
    name: str
    level: Optional[str] = None
    capacity: Optional[int] = None
    description: Optional[str] = None

class ClassCreate(ClassBase):
    pass

class ClassUpdate(BaseModel):
    name: Optional[str] = None
    level: Optional[str] = None
    capacity: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None

class ClassResponse(ClassBase):
    id: int
    school_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True