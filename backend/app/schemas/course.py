from pydantic import BaseModel
from typing import Optional

class CourseBase(BaseModel):
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    level: Optional[str] = None
    subject_area: Optional[str] = None
    credits: Optional[int] = None

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    level: Optional[str] = None
    subject_area: Optional[str] = None
    credits: Optional[int] = None
    status: Optional[str] = None

class CourseResponse(CourseBase):
    id: int
    school_id: int
    status: str
    created_at: str
    updated_at: Optional[str]
    
    class Config:
        from_attributes = True