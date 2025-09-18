from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.session import Base


class School(Base):
    __tablename__ = "schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    status = Column(String(50), nullable=False, default="active")
    contact_email = Column(String(255))
    contact_phone = Column(String(100))
    address_json = Column(Text, nullable=True)  # JSON address data
    verified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    other_names = Column(String(255), nullable=True)
    gender = Column(String(10), nullable=True)
    dob = Column(Date, nullable=True)
    national_id = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(100), nullable=True)
    address_json = Column(Text, nullable=True)  # JSON address data
    employment_no = Column(String(100), nullable=True)
    position = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    qualification = Column(String(255), nullable=True)
    hire_date = Column(Date, nullable=True)
    contract_type = Column(String(50), nullable=True)  # permanent, contract, temporary
    status = Column(String(50), nullable=False, default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="staff", uselist=False)
    class_teachers = relationship("ClassTeacher", back_populates="staff")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=True)
    dob = Column(Date, nullable=True)
    admission_no = Column(String(100), unique=True, nullable=True)
    admission_date = Column(Date, nullable=True)
    status = Column(String(50), nullable=False, default="active")
    address_json = Column(Text, nullable=True)  # JSON address data
    emergency_contact_json = Column(Text, nullable=True)  # JSON emergency contact data
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    parent_relationships = relationship("ParentStudent", back_populates="student")
    enrollments = relationship("Enrollment", back_populates="student")


class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    address_json = Column(Text, nullable=True)  # JSON address data
    occupation = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    student_relationships = relationship("ParentStudent", back_populates="parent")


class ParentStudent(Base):
    __tablename__ = "parent_students"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, index=True)
    relationship_type = Column(String(50), nullable=False)  # father, mother, guardian, etc.
    is_primary = Column(Boolean, default=False, nullable=False)  # Primary contact
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    parent = relationship("Parent", back_populates="student_relationships")
    student = relationship("Student", back_populates="parent_relationships") 