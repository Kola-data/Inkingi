from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Numeric, Text, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..db.session import Base


class FeeStructure(Base):
    __tablename__ = "fee_structures"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey('classes.id'), nullable=True, index=True)  # Null means applies to all classes
    
    # Fee details
    total_amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    payment_schedule = Column(String(50), nullable=False, default="termly")  # termly, monthly, yearly
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    effective_date = Column(Date, nullable=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    academic_year = relationship("AcademicYear")
    class_ = relationship("Class")
    creator = relationship("User")
    items = relationship("FeeItem", back_populates="structure", cascade="all, delete-orphan")
    invoices = relationship("Invoice", back_populates="fee_structure")


class FeeItem(Base):
    __tablename__ = "fee_items"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    fee_structure_id = Column(Integer, ForeignKey('fee_structures.id'), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    is_mandatory = Column(Boolean, default=True, nullable=False)
    category = Column(String(100), nullable=True)  # tuition, books, transport, etc.

    # Relationships
    structure = relationship("FeeStructure", back_populates="items")


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    invoice_number = Column(String(100), nullable=False, unique=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, index=True)
    fee_structure_id = Column(Integer, ForeignKey('fee_structures.id'), nullable=False, index=True)
    term_id = Column(Integer, ForeignKey('terms.id'), nullable=True, index=True)
    academic_year_id = Column(Integer, ForeignKey('academic_years.id'), nullable=False, index=True)
    
    # Invoice details
    subtotal = Column(Numeric(10, 2), nullable=False)
    discount_amount = Column(Numeric(10, 2), nullable=False, default=0)
    tax_amount = Column(Numeric(10, 2), nullable=False, default=0)
    total_amount = Column(Numeric(10, 2), nullable=False)
    paid_amount = Column(Numeric(10, 2), nullable=False, default=0)
    balance = Column(Numeric(10, 2), nullable=False)
    
    # Dates
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    
    # Status
    status = Column(String(50), nullable=False, default="pending")  # pending, paid, overdue, cancelled
    notes = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    student = relationship("Student")
    fee_structure = relationship("FeeStructure", back_populates="invoices")
    term = relationship("Term")
    academic_year = relationship("AcademicYear")
    creator = relationship("User")
    payments = relationship("Payment", back_populates="invoice")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False, index=True)
    fee_item_id = Column(Integer, ForeignKey('fee_items.id'), nullable=True, index=True)
    description = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    fee_item = relationship("FeeItem")


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    payment_reference = Column(String(100), nullable=False, unique=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, index=True)
    
    # Payment details
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)  # cash, bank_transfer, card, mobile_money
    payment_date = Column(Date, nullable=False)
    
    # Transaction details
    transaction_id = Column(String(255), nullable=True)  # External transaction ID
    reference_number = Column(String(255), nullable=True)  # Bank reference, receipt number
    
    # Status
    status = Column(String(50), nullable=False, default="completed")  # pending, completed, failed, cancelled
    notes = Column(Text, nullable=True)
    
    # Metadata
    received_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    invoice = relationship("Invoice", back_populates="payments")
    student = relationship("Student")
    receiver = relationship("User")


class PaymentPlan(Base):
    __tablename__ = "payment_plans"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False, index=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False, index=True)
    
    # Plan details
    total_amount = Column(Numeric(10, 2), nullable=False)
    installments = Column(Integer, nullable=False)
    installment_amount = Column(Numeric(10, 2), nullable=False)
    
    # Status
    status = Column(String(50), nullable=False, default="active")  # active, completed, cancelled
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    student = relationship("Student")
    invoice = relationship("Invoice")
    creator = relationship("User")
    installments_due = relationship("PaymentInstallment", back_populates="plan", cascade="all, delete-orphan")


class PaymentInstallment(Base):
    __tablename__ = "payment_installments"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, nullable=False, index=True)
    payment_plan_id = Column(Integer, ForeignKey('payment_plans.id'), nullable=False, index=True)
    installment_number = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    due_date = Column(Date, nullable=False)
    paid_amount = Column(Numeric(10, 2), nullable=False, default=0)
    status = Column(String(50), nullable=False, default="pending")  # pending, paid, overdue

    # Relationships
    plan = relationship("PaymentPlan", back_populates="installments_due") 