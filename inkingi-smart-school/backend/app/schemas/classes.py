from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum


class ClassLevel(str, Enum):
    NURSERY = "nursery"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    HIGH_SCHOOL = "high_school"


class ClassStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class EnrollmentStatus(str, Enum):
    ACTIVE = "active"
    TRANSFERRED = "transferred"
    DROPPED = "dropped"
    COMPLETED = "completed"


# Class schemas
class ClassCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, description="Class name (e.g., P1, P2, S1)")
    level: ClassLevel
    section: Optional[str] = Field(None, max_length=10, description="Section (e.g., A, B)")
    capacity: Optional[int] = Field(None, gt=0, description="Maximum number of students")
    description: Optional[str] = Field(None, max_length=500)


class ClassUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    level: Optional[ClassLevel] = None
    section: Optional[str] = Field(None, max_length=10)
    capacity: Optional[int] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[ClassStatus] = None


class ClassResponse(BaseModel):
    id: str
    school_id: str
    name: str
    level: ClassLevel
    section: Optional[str]
    capacity: Optional[int]
    status: ClassStatus
    description: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=str(obj.id),
            school_id=str(obj.school_id),
            name=obj.name,
            level=obj.level,
            section=obj.section,
            capacity=obj.capacity,
            status=obj.status,
            description=obj.description,
            created_at=obj.created_at.isoformat(),
            updated_at=obj.updated_at.isoformat()
        )


# Class Teacher schemas
class ClassTeacherAssign(BaseModel):
    staff_id: str = Field(..., description="ID of the staff member to assign")
    is_primary: bool = Field(True, description="Whether this is the primary class teacher")


class ClassTeacherResponse(BaseModel):
    id: str
    class_id: str
    staff_id: str
    assigned_at: date
    is_active: bool
    is_primary: bool
    teacher_name: str
    class_name: str
    
    class Config:
        from_attributes = True


# Enrollment schemas
class EnrollmentCreate(BaseModel):
    student_id: str = Field(..., description="ID of the student to enroll")
    class_id: str = Field(..., description="ID of the class")
    academic_year_id: Optional[str] = Field(None, description="Academic year ID (uses current if not provided)")


class EnrollmentUpdate(BaseModel):
    status: EnrollmentStatus


class EnrollmentResponse(BaseModel):
    id: str
    student_id: str
    class_id: str
    academic_year_id: str
    enrolled_at: date
    status: EnrollmentStatus
    student_name: str
    student_admission_number: str
    class_name: str
    
    class Config:
        from_attributes = True


# Bulk operations
class BulkEnrollment(BaseModel):
    class_id: str
    student_ids: list[str]
    academic_year_id: Optional[str] = None


class ClassStatistics(BaseModel):
    total_students: int
    male_students: int
    female_students: int
    average_age: float
    capacity_utilization: float