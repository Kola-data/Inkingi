from sqlalchemy import Column, String, Date, JSON, Enum as SQLEnum, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import TenantModel
from app.models.staff import Gender
import enum


class StudentStatus(str, enum.Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRANSFERRED = "transferred"
    GRADUATED = "graduated"
    DROPPED = "dropped"


class ParentRelationType(str, enum.Enum):
    FATHER = "father"
    MOTHER = "mother"
    GUARDIAN = "guardian"
    OTHER = "other"


class Student(TenantModel):
    __tablename__ = "students"
    
    # Personal Information
    admission_number = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    other_names = Column(String(200), nullable=True)
    gender = Column(SQLEnum(Gender), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    nationality = Column(String(100), nullable=True)
    birth_certificate_no = Column(String(50), nullable=True)
    
    # Admission Information
    admission_date = Column(Date, nullable=False)
    previous_school = Column(String(255), nullable=True)
    entry_grade = Column(String(20), nullable=True)
    status = Column(SQLEnum(StudentStatus), default=StudentStatus.ACTIVE, nullable=False)
    
    # Medical Information
    blood_group = Column(String(10), nullable=True)
    allergies = Column(Text, nullable=True)
    medical_conditions = Column(Text, nullable=True)
    emergency_medication = Column(Text, nullable=True)
    
    # Contact Information
    address_json = Column(JSON, nullable=False, default={})
    
    # Additional Information
    photo_url = Column(String(500), nullable=True)
    special_needs = Column(Text, nullable=True)
    talents_hobbies = Column(Text, nullable=True)
    documents_json = Column(JSON, nullable=True, default=[])
    notes = Column(Text, nullable=True)
    
    # Relationships
    parents = relationship("StudentParent", back_populates="student", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="student")
    fees = relationship("StudentFee", back_populates="student")
    assignment_marks = relationship("AssignmentMark", back_populates="student")
    exam_marks = relationship("ExamMark", back_populates="student")
    report_cards = relationship("ReportCard", back_populates="student")
    
    def __repr__(self):
        return f"<Student {self.admission_number} - {self.first_name} {self.last_name}>"


class Parent(TenantModel):
    __tablename__ = "parents"
    
    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    other_names = Column(String(200), nullable=True)
    gender = Column(SQLEnum(Gender), nullable=True)
    national_id = Column(String(50), nullable=True)
    
    # Contact Information
    phone_primary = Column(String(50), nullable=False)
    phone_secondary = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    address_json = Column(JSON, nullable=False, default={})
    
    # Professional Information
    occupation = Column(String(100), nullable=True)
    employer = Column(String(200), nullable=True)
    work_phone = Column(String(50), nullable=True)
    work_address = Column(Text, nullable=True)
    
    # Additional Information
    photo_url = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    children = relationship("StudentParent", back_populates="parent", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Parent {self.first_name} {self.last_name}>"


class StudentParent(TenantModel):
    __tablename__ = "student_parents"
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("parents.id"), nullable=False)
    relationship_type = Column(SQLEnum(ParentRelationType), nullable=False)
    is_primary_contact = Column(Boolean, default=False, nullable=False)
    is_authorized_pickup = Column(Boolean, default=True, nullable=False)
    receives_notifications = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    student = relationship("Student", back_populates="parents")
    parent = relationship("Parent", back_populates="children")
    
    def __repr__(self):
        return f"<StudentParent {self.student_id} - {self.parent_id}>"