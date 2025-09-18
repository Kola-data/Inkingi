from sqlalchemy import Column, String, Integer, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Course(BaseModel):
    __tablename__ = "courses"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String(200), nullable=False)  # e.g., "Mathematics", "English Language"
    code = Column(String(50), nullable=True)  # e.g., "MATH101"
    description = Column(Text, nullable=True)
    level = Column(String(50), nullable=True)  # e.g., "Primary", "Secondary"
    subject_area = Column(String(100), nullable=True)  # e.g., "Sciences", "Languages"
    credits = Column(Integer, nullable=True)
    status = Column(String(20), default="active")  # active, inactive
    
    # Relationships
    school = relationship("School", back_populates="courses")
    course_teachers = relationship("CourseTeacher", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")
    exams = relationship("Exam", back_populates="course")

class CourseTeacher(BaseModel):
    __tablename__ = "course_teachers"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    assigned_at = Column(String(50), nullable=False)  # Date as string for simplicity
    is_primary = Column(Boolean, default=True)
    
    # Relationships
    school = relationship("School")
    course = relationship("Course", back_populates="course_teachers")
    staff = relationship("Staff", back_populates="course_teachers")