from sqlalchemy import Column, String, Date, JSON, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Student(BaseModel):
    __tablename__ = "students"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    other_names = Column(String(200), nullable=True)
    gender = Column(String(10), nullable=False)  # male, female, other
    date_of_birth = Column(Date, nullable=False)
    student_number = Column(String(50), nullable=True, unique=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(JSON, nullable=True)
    emergency_contact = Column(JSON, nullable=True)
    medical_info = Column(JSON, nullable=True)
    status = Column(String(20), default="active")  # active, inactive, graduated, transferred
    
    # Relationships
    school = relationship("School", back_populates="students")
    parents = relationship("Parent", secondary="student_parents", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")
    assignment_marks = relationship("AssignmentMark", back_populates="student")
    exam_marks = relationship("ExamMark", back_populates="student")
    fees = relationship("Fee", back_populates="student")

class Parent(BaseModel):
    __tablename__ = "parents"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    other_names = Column(String(200), nullable=True)
    gender = Column(String(10), nullable=False)  # male, female, other
    phone = Column(String(20), nullable=False)
    email = Column(String(255), nullable=True)
    address = Column(JSON, nullable=True)
    occupation = Column(String(100), nullable=True)
    relationship = Column(String(50), nullable=True)  # father, mother, guardian
    status = Column(String(20), default="active")  # active, inactive
    
    # Relationships
    school = relationship("School", back_populates="parents")
    students = relationship("Student", secondary="student_parents", back_populates="parents")

# Association table for many-to-many relationship
from sqlalchemy import Table
student_parents = Table(
    "student_parents",
    BaseModel.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("parent_id", Integer, ForeignKey("parents.id"), primary_key=True),
    Column("relationship", String(50), nullable=True),  # father, mother, guardian
    Column("is_primary", Boolean, default=False)
)