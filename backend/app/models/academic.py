from sqlalchemy import Column, String, Date, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class AcademicYear(BaseModel):
    __tablename__ = "academic_years"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String(100), nullable=False)  # e.g., "2025/2026"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_current = Column(Boolean, default=False)
    
    # Relationships
    school = relationship("School", back_populates="academic_years")
    terms = relationship("Term", back_populates="academic_year")
    enrollments = relationship("Enrollment", back_populates="academic_year")

class Term(BaseModel):
    __tablename__ = "terms"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    name = Column(String(100), nullable=False)  # e.g., "Term 1", "Semester 1"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    order_index = Column(Integer, nullable=False)
    is_current = Column(Boolean, default=False)
    locked = Column(Boolean, default=False)
    
    # Relationships
    school = relationship("School")
    academic_year = relationship("AcademicYear", back_populates="terms")
    assignments = relationship("Assignment", back_populates="term")
    exams = relationship("Exam", back_populates="term")

class Class(BaseModel):
    __tablename__ = "classes"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String(100), nullable=False)  # e.g., "P2", "Grade 5A"
    level = Column(String(50), nullable=True)  # e.g., "Primary", "Secondary"
    status = Column(String(20), default="active")  # active, inactive
    capacity = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)
    
    # Relationships
    school = relationship("School", back_populates="classes")
    class_teachers = relationship("ClassTeacher", back_populates="class_entity")
    enrollments = relationship("Enrollment", back_populates="class_entity")

class ClassTeacher(BaseModel):
    __tablename__ = "class_teachers"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    assigned_at = Column(Date, nullable=False)
    is_primary = Column(Boolean, default=True)
    
    # Relationships
    school = relationship("School")
    class_entity = relationship("Class", back_populates="class_teachers")
    staff = relationship("Staff", back_populates="class_teachers")

class Enrollment(BaseModel):
    __tablename__ = "enrollments"
    
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    enrolled_at = Column(Date, nullable=False)
    status = Column(String(20), default="active")  # active, inactive, transferred, graduated
    
    # Relationships
    student = relationship("Student", back_populates="enrollments")
    class_entity = relationship("Class", back_populates="enrollments")
    school = relationship("School")
    academic_year = relationship("AcademicYear", back_populates="enrollments")