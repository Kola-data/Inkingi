from sqlalchemy import Column, String, Date, JSON, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class Staff(BaseModel):
    __tablename__ = "staff"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    other_names = Column(String(200), nullable=True)
    gender = Column(String(10), nullable=False)  # male, female, other
    date_of_birth = Column(Date, nullable=True)
    national_id = Column(String(50), nullable=True, unique=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(JSON, nullable=True)
    employment_number = Column(String(50), nullable=True, unique=True)
    position = Column(String(100), nullable=False)
    department = Column(String(100), nullable=True)
    qualification = Column(String(255), nullable=True)
    hire_date = Column(Date, nullable=False)
    contract_type = Column(String(50), nullable=False)  # permanent, contract, part-time
    status = Column(String(20), default="active")  # active, inactive, terminated
    salary = Column(String(50), nullable=True)
    emergency_contact = Column(JSON, nullable=True)
    
    # Relationships
    school = relationship("School", back_populates="staff")
    user = relationship("User", back_populates="staff", uselist=False)
    class_teachers = relationship("ClassTeacher", back_populates="staff")
    course_teachers = relationship("CourseTeacher", back_populates="staff")