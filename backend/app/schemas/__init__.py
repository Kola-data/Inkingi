from .user import UserCreate, UserUpdate, UserResponse, UserLogin
from .school import SchoolCreate, SchoolUpdate, SchoolResponse
from .staff import StaffCreate, StaffUpdate, StaffResponse
from .student import StudentCreate, StudentUpdate, StudentResponse, ParentCreate, ParentUpdate, ParentResponse
from .academic import AcademicYearCreate, AcademicYearUpdate, AcademicYearResponse, TermCreate, TermUpdate, TermResponse, ClassCreate, ClassUpdate, ClassResponse
from .course import CourseCreate, CourseUpdate, CourseResponse
from .timetable import PeriodCreate, PeriodUpdate, PeriodResponse, RoomCreate, RoomUpdate, RoomResponse, TimetableCreate, TimetableUpdate, TimetableResponse
from .marks import AssignmentCreate, AssignmentUpdate, AssignmentResponse, ExamCreate, ExamUpdate, ExamResponse
from .fees import FeeStructureCreate, FeeStructureUpdate, FeeStructureResponse, FeeCreate, FeeUpdate, FeeResponse
from .inventory import InventoryCreate, InventoryUpdate, InventoryResponse, InventoryItemCreate, InventoryItemUpdate, InventoryItemResponse
from .communication import MessageCreate, MessageResponse
from .ai import ChatSessionCreate, ChatSessionResponse, ChatMessageCreate, ChatMessageResponse

__all__ = [
    "UserCreate", "UserUpdate", "UserResponse", "UserLogin",
    "SchoolCreate", "SchoolUpdate", "SchoolResponse",
    "StaffCreate", "StaffUpdate", "StaffResponse",
    "StudentCreate", "StudentUpdate", "StudentResponse", "ParentCreate", "ParentUpdate", "ParentResponse",
    "AcademicYearCreate", "AcademicYearUpdate", "AcademicYearResponse", "TermCreate", "TermUpdate", "TermResponse", "ClassCreate", "ClassUpdate", "ClassResponse",
    "CourseCreate", "CourseUpdate", "CourseResponse",
    "PeriodCreate", "PeriodUpdate", "PeriodResponse", "RoomCreate", "RoomUpdate", "RoomResponse", "TimetableCreate", "TimetableUpdate", "TimetableResponse",
    "AssignmentCreate", "AssignmentUpdate", "AssignmentResponse", "ExamCreate", "ExamUpdate", "ExamResponse",
    "FeeStructureCreate", "FeeStructureUpdate", "FeeStructureResponse", "FeeCreate", "FeeUpdate", "FeeResponse",
    "InventoryCreate", "InventoryUpdate", "InventoryResponse", "InventoryItemCreate", "InventoryItemUpdate", "InventoryItemResponse",
    "MessageCreate", "MessageResponse",
    "ChatSessionCreate", "ChatSessionResponse", "ChatMessageCreate", "ChatMessageResponse"
]