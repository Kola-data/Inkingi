"""
Academic models for calendar, classes, and enrollment
"""
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel


class ClassStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class EnrollmentStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    TRANSFERRED = "transferred"
    WITHDRAWN = "withdrawn"
    COMPLETED = "completed"


class AcademicYear(BaseModel):
    """Academic year model"""
    __tablename__ = "academic_years"
    
    # Multi-tenancy
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    
    name = Column(String(20), nullable=False)  # e.g., "2025/2026"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_current = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    school = relationship("School", back_populates="academic_years")
    terms = relationship("Term", back_populates="academic_year")
    enrollments = relationship("Enrollment", back_populates="academic_year")
    
    def __repr__(self):
        return f"<AcademicYear(id={self.id}, name='{self.name}', school_id={self.school_id})>"


class Term(BaseModel):
    """Term/Semester model"""
    __tablename__ = "terms"
    
    # Multi-tenancy
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    
    name = Column(String(50), nullable=False)  # e.g., "Term 1", "Semester 1"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    order_index = Column(Integer, nullable=False)  # 1, 2, 3...
    is_current = Column(Boolean, default=False, nullable=False)
    locked = Column(Boolean, default=False, nullable=False)  # Lock past terms
    
    # Relationships
    school = relationship("School")
    academic_year = relationship("AcademicYear", back_populates="terms")
    
    def __repr__(self):
        return f"<Term(id={self.id}, name='{self.name}', academic_year_id={self.academic_year_id})>"


class Class(BaseModel):
    """Class model"""
    __tablename__ = "classes"
    
    # Multi-tenancy
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    
    name = Column(String(100), nullable=False)  # e.g., "P2", "Grade 7A"
    level = Column(String(20), nullable=True)   # e.g., "Primary", "Secondary"
    status = Column(Enum(ClassStatusEnum), default=ClassStatusEnum.ACTIVE, nullable=False)
    
    # Relationships
    school = relationship("School", back_populates="classes")
    teachers = relationship("ClassTeacher", back_populates="class_")
    enrollments = relationship("Enrollment", back_populates="class_")
    
    def __repr__(self):
        return f"<Class(id={self.id}, name='{self.name}', school_id={self.school_id})>"


class ClassTeacher(BaseModel):
    """Class teacher assignment"""
    __tablename__ = "class_teachers"
    
    # Multi-tenancy
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    
    assigned_at = Column(DateTime, nullable=False)
    
    # Relationships
    school = relationship("School")
    class_ = relationship("Class", back_populates="teachers")
    staff = relationship("Staff", back_populates="class_assignments")
    
    def __repr__(self):
        return f"<ClassTeacher(class_id={self.class_id}, staff_id={self.staff_id})>"


class Enrollment(BaseModel):
    """Student enrollment in class"""
    __tablename__ = "enrollments"
    
    # Multi-tenancy
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    
    # Note: student_id would reference a Student model (not implemented in MVP scope)
    student_id = Column(Integer, nullable=False, index=True)  # Future: ForeignKey("students.id")
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    
    enrolled_at = Column(DateTime, nullable=False)
    status = Column(Enum(EnrollmentStatusEnum), default=EnrollmentStatusEnum.ACTIVE, nullable=False)
    
    # Relationships
    school = relationship("School")
    class_ = relationship("Class", back_populates="enrollments")
    academic_year = relationship("AcademicYear", back_populates="enrollments")
    
    def __repr__(self):
        return f"<Enrollment(student_id={self.student_id}, class_id={self.class_id}, academic_year_id={self.academic_year_id})>"