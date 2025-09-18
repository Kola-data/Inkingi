from sqlalchemy import Column, String, Integer, ForeignKey, Float, Date, Text, Boolean, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class FeeStructure(BaseModel):
    __tablename__ = "fee_structures"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String(200), nullable=False)  # e.g., "Primary School Fees 2025"
    description = Column(Text, nullable=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)  # NULL for all classes
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    due_date = Column(Date, nullable=True)
    is_mandatory = Column(Boolean, default=True)
    payment_terms = Column(JSON, nullable=True)  # Installment options, etc.
    status = Column(String(20), default="active")  # active, inactive
    
    # Relationships
    school = relationship("School")
    academic_year = relationship("AcademicYear")
    class_entity = relationship("Class")
    fees = relationship("Fee", back_populates="fee_structure")

class Fee(BaseModel):
    __tablename__ = "fees"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    due_date = Column(Date, nullable=True)
    status = Column(String(20), default="pending")  # pending, paid, overdue, waived, cancelled
    notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("staff.id"), nullable=True)
    
    # Relationships
    school = relationship("School")
    student = relationship("Student", back_populates="fees")
    fee_structure = relationship("FeeStructure", back_populates="fees")
    creator = relationship("Staff")
    payments = relationship("Payment", back_populates="fee")

class Payment(BaseModel):
    __tablename__ = "payments"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    fee_id = Column(Integer, ForeignKey("fees.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="USD")
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String(50), nullable=False)  # cash, bank_transfer, mobile_money, etc.
    reference_number = Column(String(100), nullable=True)
    status = Column(String(20), default="completed")  # completed, pending, failed, refunded
    notes = Column(Text, nullable=True)
    received_by = Column(Integer, ForeignKey("staff.id"), nullable=True)
    
    # Relationships
    school = relationship("School")
    fee = relationship("Fee", back_populates="payments")
    receiver = relationship("Staff")