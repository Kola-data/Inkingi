# Import all models in the correct order to avoid circular import issues
from .calendar import AcademicYear, Term
from .school import School, Staff, Student, Parent, ParentStudent
from .user import User, Role, Permission, AccessControlEntry
from .academics import Class, Course, ClassTeacher, CourseTeacher, Enrollment
from .timetable import Room, Period, Timetable, TimetableEntry, TeacherAvailability
from .marks import AssignmentMark, ExamMark, MarkReport, GradingScale, GradingBand
from .finance import (
    FeeStructure, FeeItem, Invoice, InvoiceItem, 
    Payment, PaymentPlan, PaymentInstallment
)
from .inventory import (
    Inventory, ItemCategory, Item, InventoryItem, 
    StockMovement, StockAdjustment, StockAdjustmentItem
)
from .message import (
    Message, MessageRecipient, MessageTemplate, 
    MessageAttachment, MessageLog
)

__all__ = [
    # Calendar
    "AcademicYear", "Term",
    
    # School & People
    "School", "Staff", "Student", "Parent", "ParentStudent",
    
    # Users & Auth
    "User", "Role", "Permission", "AccessControlEntry",
    
    # Academics
    "Class", "Course", "ClassTeacher", "CourseTeacher", "Enrollment",
    
    # Timetable
    "Room", "Period", "Timetable", "TimetableEntry", "TeacherAvailability",
    
    # Marks
    "AssignmentMark", "ExamMark", "MarkReport", "GradingScale", "GradingBand",
    
    # Finance
    "FeeStructure", "FeeItem", "Invoice", "InvoiceItem", 
    "Payment", "PaymentPlan", "PaymentInstallment",
    
    # Inventory
    "Inventory", "ItemCategory", "Item", "InventoryItem", 
    "StockMovement", "StockAdjustment", "StockAdjustmentItem",
    
    # Messages
    "Message", "MessageRecipient", "MessageTemplate", 
    "MessageAttachment", "MessageLog",
]
