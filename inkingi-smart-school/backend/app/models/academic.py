from sqlalchemy import Column, String, Date, Boolean, ForeignKey, Integer, Enum as SQLEnum, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import TenantModel
import enum


class ClassLevel(str, enum.Enum):
    NURSERY = "nursery"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    HIGH_SCHOOL = "high_school"


class ClassStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class EnrollmentStatus(str, enum.Enum):
    ACTIVE = "active"
    TRANSFERRED = "transferred"
    DROPPED = "dropped"
    COMPLETED = "completed"


class CourseStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class AcademicYear(TenantModel):
    __tablename__ = "academic_years"
    __table_args__ = (
        UniqueConstraint("school_id", "name", name="uq_academic_year_name"),
        Index("ix_academic_year_current", "school_id", "is_current"),
    )
    
    name = Column(String(50), nullable=False)  # e.g., "2025/2026"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_current = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    terms = relationship("Term", back_populates="academic_year", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="academic_year")
    
    def __repr__(self):
        return f"<AcademicYear {self.name}>"


class Term(TenantModel):
    __tablename__ = "terms"
    __table_args__ = (
        UniqueConstraint("school_id", "academic_year_id", "order_index", name="uq_term_order"),
        Index("ix_term_current", "school_id", "is_current"),
    )
    
    academic_year_id = Column(UUID(as_uuid=True), ForeignKey("academic_years.id"), nullable=False)
    name = Column(String(50), nullable=False)  # e.g., "Term 1", "Semester 1"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    order_index = Column(Integer, nullable=False)  # 1, 2, 3
    is_current = Column(Boolean, default=False, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    academic_year = relationship("AcademicYear", back_populates="terms")
    assignments = relationship("Assignment", back_populates="term")
    exams = relationship("Exam", back_populates="term")
    report_cards = relationship("ReportCard", back_populates="term")
    
    def __repr__(self):
        return f"<Term {self.name}>"


class Class(TenantModel):
    __tablename__ = "classes"
    __table_args__ = (
        UniqueConstraint("school_id", "name", name="uq_class_name"),
    )
    
    name = Column(String(50), nullable=False)  # e.g., "P1", "P2", "S1"
    level = Column(SQLEnum(ClassLevel), nullable=False)
    section = Column(String(10), nullable=True)  # e.g., "A", "B" for multiple sections
    capacity = Column(Integer, nullable=True)
    status = Column(SQLEnum(ClassStatus), default=ClassStatus.ACTIVE, nullable=False)
    description = Column(String(500), nullable=True)
    
    # Relationships
    teachers = relationship("ClassTeacher", back_populates="class_obj", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="class_obj")
    timetable_entries = relationship("TimetableEntry", back_populates="class_obj")
    
    def __repr__(self):
        return f"<Class {self.name}>"


class ClassTeacher(TenantModel):
    __tablename__ = "class_teachers"
    __table_args__ = (
        Index("ix_class_teacher_active", "class_id", "is_active"),
    )
    
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=False)
    assigned_at = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_primary = Column(Boolean, default=True, nullable=False)  # Main class teacher vs assistant
    
    # Relationships
    class_obj = relationship("Class", back_populates="teachers")
    teacher = relationship("Staff", back_populates="class_assignments")
    
    def __repr__(self):
        return f"<ClassTeacher {self.class_id} - {self.staff_id}>"


class Enrollment(TenantModel):
    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint("student_id", "class_id", "academic_year_id", name="uq_enrollment"),
        Index("ix_enrollment_student", "student_id", "academic_year_id"),
    )
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    academic_year_id = Column(UUID(as_uuid=True), ForeignKey("academic_years.id"), nullable=False)
    enrolled_at = Column(Date, nullable=False)
    status = Column(SQLEnum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE, nullable=False)
    
    # Relationships
    student = relationship("Student", back_populates="enrollments")
    class_obj = relationship("Class", back_populates="enrollments")
    academic_year = relationship("AcademicYear", back_populates="enrollments")
    
    def __repr__(self):
        return f"<Enrollment {self.student_id} in {self.class_id}>"


class Course(TenantModel):
    __tablename__ = "courses"
    __table_args__ = (
        UniqueConstraint("school_id", "code", name="uq_course_code"),
    )
    
    code = Column(String(20), nullable=False)  # e.g., "MATH101"
    name = Column(String(100), nullable=False)  # e.g., "Mathematics"
    description = Column(String(500), nullable=True)
    credits = Column(Integer, nullable=True)
    status = Column(SQLEnum(CourseStatus), default=CourseStatus.ACTIVE, nullable=False)
    
    # Relationships
    teachers = relationship("CourseTeacher", back_populates="course", cascade="all, delete-orphan")
    timetable_entries = relationship("TimetableEntry", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")
    exams = relationship("Exam", back_populates="course")
    
    def __repr__(self):
        return f"<Course {self.code} - {self.name}>"


class CourseTeacher(TenantModel):
    __tablename__ = "course_teachers"
    __table_args__ = (
        UniqueConstraint("course_id", "staff_id", "class_id", name="uq_course_teacher"),
    )
    
    course_id = Column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=False)
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=True)  # Optional: specific class
    assigned_at = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    course = relationship("Course", back_populates="teachers")
    teacher = relationship("Staff", back_populates="course_assignments")
    
    def __repr__(self):
        return f"<CourseTeacher {self.course_id} - {self.staff_id}>"