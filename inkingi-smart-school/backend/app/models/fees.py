from sqlalchemy import Column, String, Float, ForeignKey, Date, Text, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import TenantModel
import enum


class FeeType(str, enum.Enum):
    TUITION = "tuition"
    ADMISSION = "admission"
    EXAMINATION = "examination"
    LIBRARY = "library"
    LABORATORY = "laboratory"
    SPORTS = "sports"
    TRANSPORT = "transport"
    BOARDING = "boarding"
    UNIFORM = "uniform"
    BOOKS = "books"
    OTHER = "other"


class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    MOBILE_MONEY = "mobile_money"
    CHEQUE = "cheque"
    CARD = "card"
    OTHER = "other"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    PARTIAL = "partial"
    FAILED = "failed"
    REFUNDED = "refunded"


class FeeCategory(TenantModel):
    __tablename__ = "fee_categories"
    __table_args__ = (
        UniqueConstraint("school_id", "name", name="uq_fee_category_name"),
    )
    
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    fee_type = Column(SQLEnum(FeeType), nullable=False)
    is_mandatory = Column(String, default="true", nullable=False)
    
    # Relationships
    fee_structures = relationship("FeeStructure", back_populates="category")
    
    def __repr__(self):
        return f"<FeeCategory {self.name}>"


class FeeStructure(TenantModel):
    __tablename__ = "fee_structures"
    __table_args__ = (
        UniqueConstraint("school_id", "academic_year_id", "term_id", "class_id", "category_id", 
                         name="uq_fee_structure"),
    )
    
    academic_year_id = Column(UUID(as_uuid=True), ForeignKey("academic_years.id"), nullable=False)
    term_id = Column(UUID(as_uuid=True), ForeignKey("terms.id"), nullable=True)  # Optional for annual fees
    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=True)  # Optional for school-wide fees
    category_id = Column(UUID(as_uuid=True), ForeignKey("fee_categories.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=True)
    late_fee_amount = Column(Float, default=0, nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationships
    category = relationship("FeeCategory", back_populates="fee_structures")
    student_fees = relationship("StudentFee", back_populates="fee_structure")
    
    def __repr__(self):
        return f"<FeeStructure {self.category_id} - {self.amount}>"


class StudentFee(TenantModel):
    __tablename__ = "student_fees"
    __table_args__ = (
        UniqueConstraint("student_id", "fee_structure_id", name="uq_student_fee"),
    )
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    fee_structure_id = Column(UUID(as_uuid=True), ForeignKey("fee_structures.id"), nullable=False)
    
    amount = Column(Float, nullable=False)  # Can be different from structure (discounts/scholarships)
    discount_amount = Column(Float, default=0, nullable=False)
    discount_reason = Column(Text, nullable=True)
    
    amount_paid = Column(Float, default=0, nullable=False)
    balance = Column(Float, nullable=False)  # Computed: amount - amount_paid
    
    due_date = Column(Date, nullable=False)
    is_paid = Column(String, default="false", nullable=False)
    paid_date = Column(Date, nullable=True)
    
    # Relationships
    student = relationship("Student", back_populates="fees")
    fee_structure = relationship("FeeStructure", back_populates="student_fees")
    payments = relationship("Payment", back_populates="student_fee")
    
    def __repr__(self):
        return f"<StudentFee {self.student_id} - {self.amount}>"


class Payment(TenantModel):
    __tablename__ = "payments"
    
    student_fee_id = Column(UUID(as_uuid=True), ForeignKey("student_fees.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    payment_method = Column(SQLEnum(PaymentMethod), nullable=False)
    payment_date = Column(Date, nullable=False)
    reference_number = Column(String(100), nullable=True)
    
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    
    # Payment details
    bank_name = Column(String(100), nullable=True)
    cheque_number = Column(String(50), nullable=True)
    transaction_id = Column(String(100), nullable=True)
    
    # Receipt
    receipt_number = Column(String(50), nullable=True)
    receipt_issued = Column(String, default="false", nullable=False)
    receipt_issued_date = Column(Date, nullable=True)
    
    notes = Column(Text, nullable=True)
    received_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    
    # Relationships
    student_fee = relationship("StudentFee", back_populates="payments")
    
    def __repr__(self):
        return f"<Payment {self.reference_number} - {self.amount}>"