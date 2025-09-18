from pydantic import BaseModel
from typing import Optional
from datetime import date

class AssignmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    due_date: date
    total_marks: float
    weight: Optional[float] = None

class AssignmentCreate(AssignmentBase):
    course_id: int
    term_id: int

class AssignmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    total_marks: Optional[float] = None
    weight: Optional[float] = None
    status: Optional[str] = None

class AssignmentResponse(AssignmentBase):
    id: int
    school_id: int
    course_id: int
    term_id: int
    status: str
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True

class ExamBase(BaseModel):
    name: str
    description: Optional[str] = None
    exam_date: date
    total_marks: float
    weight: Optional[float] = None
    duration_minutes: Optional[int] = None

class ExamCreate(ExamBase):
    course_id: int
    term_id: int

class ExamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    exam_date: Optional[date] = None
    total_marks: Optional[float] = None
    weight: Optional[float] = None
    duration_minutes: Optional[int] = None
    status: Optional[str] = None

class ExamResponse(ExamBase):
    id: int
    school_id: int
    course_id: int
    term_id: int
    status: str
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True