from .base import Base
from .school import School
from .user import User, Role, Permission, UserRole, RolePermission
from .staff import Staff
from .student import Student, Parent
from .academic import AcademicYear, Term, Class, ClassTeacher, Enrollment
from .course import Course, CourseTeacher
from .timetable import Period, Room, Timetable
from .marks import Assignment, Exam, AssignmentMark, ExamMark
from .fees import FeeStructure, Fee, Payment
from .inventory import Inventory, InventoryItem, StockMovement
from .communication import Message, MessageRecipient
from .ai import ChatSession, ChatMessage

__all__ = [
    "Base",
    "School",
    "User", "Role", "Permission", "UserRole", "RolePermission",
    "Staff", "Student", "Parent",
    "AcademicYear", "Term", "Class", "ClassTeacher", "Enrollment",
    "Course", "CourseTeacher",
    "Period", "Room", "Timetable",
    "Assignment", "Exam", "AssignmentMark", "ExamMark",
    "FeeStructure", "Fee", "Payment",
    "Inventory", "InventoryItem", "StockMovement",
    "Message", "MessageRecipient",
    "ChatSession", "ChatMessage"
]