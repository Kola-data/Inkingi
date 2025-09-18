"""
Academic schemas
"""
from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel


# Academic Year Schemas
class AcademicYearBase(BaseModel):
    """Academic year base schema"""
    name: str
    start_date: date
    end_date: date
    is_current: bool = False


class AcademicYearCreate(AcademicYearBase):
    """Academic year creation schema"""
    pass


class AcademicYearResponse(AcademicYearBase):
    """Academic year response schema"""
    id: int
    school_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Term Schemas
class TermBase(BaseModel):
    """Term base schema"""
    name: str
    start_date: date
    end_date: date
    order_index: int
    is_current: bool = False
    locked: bool = False


class TermCreate(TermBase):
    """Term creation schema"""
    academic_year_id: int


class TermResponse(TermBase):
    """Term response schema"""
    id: int
    school_id: int
    academic_year_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Class Schemas
class ClassBase(BaseModel):
    """Class base schema"""
    name: str
    level: Optional[str] = None


class ClassCreate(ClassBase):
    """Class creation schema"""
    pass


class ClassUpdate(BaseModel):
    """Class update schema"""
    name: Optional[str] = None
    level: Optional[str] = None
    status: Optional[str] = None


class ClassTeacherAssign(BaseModel):
    """Class teacher assignment schema"""
    staff_id: int


class ClassResponse(ClassBase):
    """Class response schema"""
    id: int
    school_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    # Optional teacher information
    current_teacher: Optional[str] = None
    enrollment_count: Optional[int] = 0
    
    class Config:
        from_attributes = True


# Enrollment Schemas
class EnrollmentBase(BaseModel):
    """Enrollment base schema"""
    student_id: int
    class_id: int
    academic_year_id: Optional[int] = None  # Will use current if not provided


class EnrollmentCreate(EnrollmentBase):
    """Enrollment creation schema"""
    pass


class EnrollmentResponse(EnrollmentBase):
    """Enrollment response schema"""
    id: int
    school_id: int
    academic_year_id: int
    enrolled_at: datetime
    status: str
    
    # Additional information
    class_name: Optional[str] = None
    academic_year_name: Optional[str] = None
    
    class Config:
        from_attributes = True