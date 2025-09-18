from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, Text, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.session import Base


class AssignmentMark(Base):
    __tablename__ = "assignment_marks"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False, index=True)
    term_id = Column(Integer, ForeignKey('terms.id'), nullable=False, index=True)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'), nullable=False, index=True)
    
    # Assignment details
    assignment_name = Column(String(255), nullable=False)
    assignment_type = Column(String(100), nullable=True)  # homework, quiz, project, etc.
    score = Column(Numeric(5, 2), nullable=False)  # Actual score
    max_score = Column(Numeric(5, 2), nullable=False)  # Maximum possible score
    weight = Column(Float, nullable=False, default=1.0)  # Weight in final calculation
    
    # Metadata
    assigned_date = Column(DateTime(timezone=True), nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    submitted_date = Column(DateTime(timezone=True), nullable=True)
    graded_by = Column(Integer, ForeignKey('staff.id'), nullable=False, index=True)
    comments = Column(Text, nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    student = relationship("Student")
    course = relationship("Course")
    class_ = relationship("Class")
    term = relationship("Term")
    academic_year = relationship("AcademicYear")
    grader = relationship("Staff")


class ExamMark(Base):
    __tablename__ = "exam_marks"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False, index=True)
    term_id = Column(Integer, ForeignKey('terms.id'), nullable=False, index=True)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'), nullable=False, index=True)
    
    # Exam details
    exam_name = Column(String(255), nullable=False)
    exam_type = Column(String(100), nullable=False)  # midterm, final, quiz, etc.
    score = Column(Numeric(5, 2), nullable=False)  # Actual score
    max_score = Column(Numeric(5, 2), nullable=False)  # Maximum possible score
    weight = Column(Float, nullable=False, default=1.0)  # Weight in final calculation
    
    # Metadata
    exam_date = Column(DateTime(timezone=True), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    graded_by = Column(Integer, ForeignKey('staff.id'), nullable=False, index=True)
    comments = Column(Text, nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    student = relationship("Student")
    course = relationship("Course")
    class_ = relationship("Class")
    term = relationship("Term")
    academic_year = relationship("AcademicYear")
    grader = relationship("Staff")


class MarkReport(Base):
    __tablename__ = "mark_reports"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=False, index=True)
    term_id = Column(Integer, ForeignKey('terms.id'), nullable=False, index=True)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'), nullable=False, index=True)
    
    # Calculated totals
    assignment_total = Column(Numeric(5, 2), nullable=False, default=0)
    exam_total = Column(Numeric(5, 2), nullable=False, default=0)
    total = Column(Numeric(5, 2), nullable=False, default=0)
    percentage = Column(Numeric(5, 2), nullable=False, default=0)
    grade = Column(String(10), nullable=True)  # A, B, C, D, F or custom grading
    
    # Rankings
    position = Column(Integer, nullable=True)  # Position in class/course
    total_students = Column(Integer, nullable=True)  # Total students in comparison
    
    # Metadata
    computed_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    computed_by = Column(Integer, ForeignKey('users.id'), nullable=True)

    # Relationships
    student = relationship("Student")
    course = relationship("Course")
    class_ = relationship("Class")
    term = relationship("Term")
    academic_year = relationship("AcademicYear")
    computed_by_user = relationship("User")


class GradingScale(Base):
    __tablename__ = "grading_scales"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    bands = relationship("GradingBand", back_populates="scale", cascade="all, delete-orphan")


class GradingBand(Base):
    __tablename__ = "grading_bands"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    grading_scale_id = Column(Integer, ForeignKey('grading_scales.id'), nullable=False, index=True)
    grade = Column(String(10), nullable=False)  # A, B, C, etc.
    min_percentage = Column(Numeric(5, 2), nullable=False)
    max_percentage = Column(Numeric(5, 2), nullable=False)
    description = Column(String(255), nullable=True)  # Excellent, Good, etc.
    gpa_value = Column(Numeric(3, 2), nullable=True)  # 4.0, 3.5, etc.

    # Relationships
    scale = relationship("GradingScale", back_populates="bands") 