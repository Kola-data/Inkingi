from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, Text, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Assignment(BaseModel):
    __tablename__ = "assignments"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    term_id = Column(Integer, ForeignKey("terms.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=False)
    total_marks = Column(Float, nullable=False)
    weight = Column(Float, nullable=True)  # Weight in final grade calculation
    status = Column(String(20), default="active")  # active, completed, cancelled
    
    # Relationships
    school = relationship("School")
    course = relationship("Course", back_populates="assignments")
    term = relationship("Term", back_populates="assignments")
    assignment_marks = relationship("AssignmentMark", back_populates="assignment")

class Exam(BaseModel):
    __tablename__ = "exams"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    term_id = Column(Integer, ForeignKey("terms.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    exam_date = Column(Date, nullable=False)
    total_marks = Column(Float, nullable=False)
    weight = Column(Float, nullable=True)  # Weight in final grade calculation
    duration_minutes = Column(Integer, nullable=True)
    status = Column(String(20), default="active")  # active, completed, cancelled
    
    # Relationships
    school = relationship("School")
    course = relationship("Course", back_populates="exams")
    term = relationship("Term", back_populates="exams")
    exam_marks = relationship("ExamMark", back_populates="exam")

class AssignmentMark(BaseModel):
    __tablename__ = "assignment_marks"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    marks_obtained = Column(Float, nullable=False)
    max_marks = Column(Float, nullable=False)
    grade = Column(String(10), nullable=True)  # A+, A, B+, etc.
    comments = Column(Text, nullable=True)
    marked_by = Column(Integer, ForeignKey("staff.id"), nullable=True)
    marked_at = Column(Date, nullable=False)
    
    # Relationships
    school = relationship("School")
    assignment = relationship("Assignment", back_populates="assignment_marks")
    student = relationship("Student", back_populates="assignment_marks")
    marker = relationship("Staff")

class ExamMark(BaseModel):
    __tablename__ = "exam_marks"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    marks_obtained = Column(Float, nullable=False)
    max_marks = Column(Float, nullable=False)
    grade = Column(String(10), nullable=True)  # A+, A, B+, etc.
    comments = Column(Text, nullable=True)
    marked_by = Column(Integer, ForeignKey("staff.id"), nullable=True)
    marked_at = Column(Date, nullable=False)
    
    # Relationships
    school = relationship("School")
    exam = relationship("Exam", back_populates="exam_marks")
    student = relationship("Student", back_populates="exam_marks")
    marker = relationship("Staff")