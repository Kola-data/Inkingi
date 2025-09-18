from sqlalchemy import Column, String, Date, JSON, Enum as SQLEnum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import TenantModel
import enum


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class StaffStatus(str, enum.Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class ContractType(str, enum.Enum):
    PERMANENT = "permanent"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    VOLUNTEER = "volunteer"


class Staff(TenantModel):
    __tablename__ = "staff"
    
    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    other_names = Column(String(200), nullable=True)
    gender = Column(SQLEnum(Gender), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    national_id = Column(String(50), nullable=True)
    passport_number = Column(String(50), nullable=True)
    
    # Contact Information
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    emergency_contact = Column(String(50), nullable=True)
    emergency_contact_name = Column(String(200), nullable=True)
    address_json = Column(JSON, nullable=False, default={})
    
    # Employment Information
    employment_number = Column(String(50), nullable=False)
    position = Column(String(100), nullable=False)
    department = Column(String(100), nullable=True)
    qualification = Column(String(500), nullable=True)
    specialization = Column(String(200), nullable=True)
    hire_date = Column(Date, nullable=False)
    contract_type = Column(SQLEnum(ContractType), nullable=False)
    contract_end_date = Column(Date, nullable=True)
    status = Column(SQLEnum(StaffStatus), default=StaffStatus.ACTIVE, nullable=False)
    
    # Financial Information
    salary_grade = Column(String(20), nullable=True)
    bank_name = Column(String(100), nullable=True)
    bank_account = Column(String(50), nullable=True)
    tax_number = Column(String(50), nullable=True)
    social_security_number = Column(String(50), nullable=True)
    
    # Additional Information
    photo_url = Column(String(500), nullable=True)
    documents_json = Column(JSON, nullable=True, default=[])
    skills_json = Column(JSON, nullable=True, default=[])
    certifications_json = Column(JSON, nullable=True, default=[])
    notes = Column(Text, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="staff", uselist=False)
    class_assignments = relationship("ClassTeacher", back_populates="teacher")
    course_assignments = relationship("CourseTeacher", back_populates="teacher")
    
    def __repr__(self):
        return f"<Staff {self.first_name} {self.last_name}>"