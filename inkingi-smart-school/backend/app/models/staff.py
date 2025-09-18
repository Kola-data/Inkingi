"""
Staff model
"""
from sqlalchemy import Column, Integer, String, Date, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel


class GenderEnum(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class ContractTypeEnum(str, enum.Enum):
    PERMANENT = "permanent"
    CONTRACT = "contract"
    TEMPORARY = "temporary"
    VOLUNTEER = "volunteer"


class StaffStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


class Staff(BaseModel):
    """Staff model"""
    __tablename__ = "staff"
    
    # Multi-tenancy
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    other_names = Column(String(200), nullable=True)
    gender = Column(Enum(GenderEnum), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    national_id = Column(String(20), nullable=True)
    
    # Contact information
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    address_json = Column(JSON, nullable=True)
    
    # Employment information
    employment_no = Column(String(50), nullable=True)
    position = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    qualification = Column(String(200), nullable=True)
    hire_date = Column(Date, nullable=True)
    contract_type = Column(Enum(ContractTypeEnum), default=ContractTypeEnum.PERMANENT)
    status = Column(Enum(StaffStatusEnum), default=StaffStatusEnum.ACTIVE, nullable=False)
    
    # Relationships
    school = relationship("School", back_populates="staff")
    user = relationship("User", back_populates="staff", uselist=False)
    class_assignments = relationship("ClassTeacher", back_populates="staff")
    
    def __repr__(self):
        return f"<Staff(id={self.id}, name='{self.first_name} {self.last_name}', school_id={self.school_id})>"
    
    @property
    def full_name(self):
        """Get full name"""
        names = [self.first_name, self.other_names, self.last_name]
        return " ".join(filter(None, names))