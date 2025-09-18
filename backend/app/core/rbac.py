from enum import Enum
from typing import List, Set
from fastapi import HTTPException, status


class UserRole(str, Enum):
    SYSTEM_ADMIN = "system_admin"
    SCHOOL_ADMIN = "school_admin" 
    ACCOUNTANT = "accountant"
    TEACHER = "teacher"
    PARENT = "parent"
    STUDENT = "student"


class Permission(str, Enum):
    # School management
    MANAGE_SCHOOLS = "manage_schools"
    VIEW_SCHOOLS = "view_schools"
    
    # User management
    MANAGE_USERS = "manage_users"
    VIEW_USERS = "view_users"
    
    # People management
    MANAGE_STAFF = "manage_staff"
    VIEW_STAFF = "view_staff"
    MANAGE_STUDENTS = "manage_students"
    VIEW_STUDENTS = "view_students"
    MANAGE_PARENTS = "manage_parents"
    VIEW_PARENTS = "view_parents"
    
    # Academic management
    MANAGE_CALENDAR = "manage_calendar"
    VIEW_CALENDAR = "view_calendar"
    MANAGE_CLASSES = "manage_classes"
    VIEW_CLASSES = "view_classes"
    MANAGE_COURSES = "manage_courses"
    VIEW_COURSES = "view_courses"
    MANAGE_TIMETABLE = "manage_timetable"
    VIEW_TIMETABLE = "view_timetable"
    
    # Marks management
    MANAGE_MARKS = "manage_marks"
    VIEW_MARKS = "view_marks"
    VIEW_OWN_MARKS = "view_own_marks"
    
    # Finance management
    MANAGE_FEES = "manage_fees"
    VIEW_FEES = "view_fees"
    VIEW_OWN_FEES = "view_own_fees"
    
    # Inventory management
    MANAGE_INVENTORY = "manage_inventory"
    VIEW_INVENTORY = "view_inventory"
    
    # Communication
    SEND_MESSAGES = "send_messages"
    VIEW_MESSAGES = "view_messages"


# Role-Permission mapping
ROLE_PERMISSIONS: dict[UserRole, Set[Permission]] = {
    UserRole.SYSTEM_ADMIN: {
        Permission.MANAGE_SCHOOLS, Permission.VIEW_SCHOOLS,
        Permission.MANAGE_USERS, Permission.VIEW_USERS,
        # System admin has all permissions
    },
    UserRole.SCHOOL_ADMIN: {
        Permission.VIEW_SCHOOLS,
        Permission.MANAGE_USERS, Permission.VIEW_USERS,
        Permission.MANAGE_STAFF, Permission.VIEW_STAFF,
        Permission.MANAGE_STUDENTS, Permission.VIEW_STUDENTS,
        Permission.MANAGE_PARENTS, Permission.VIEW_PARENTS,
        Permission.MANAGE_CALENDAR, Permission.VIEW_CALENDAR,
        Permission.MANAGE_CLASSES, Permission.VIEW_CLASSES,
        Permission.MANAGE_COURSES, Permission.VIEW_COURSES,
        Permission.MANAGE_TIMETABLE, Permission.VIEW_TIMETABLE,
        Permission.MANAGE_MARKS, Permission.VIEW_MARKS,
        Permission.MANAGE_FEES, Permission.VIEW_FEES,
        Permission.MANAGE_INVENTORY, Permission.VIEW_INVENTORY,
        Permission.SEND_MESSAGES, Permission.VIEW_MESSAGES,
    },
    UserRole.ACCOUNTANT: {
        Permission.VIEW_STUDENTS, Permission.VIEW_PARENTS,
        Permission.VIEW_CALENDAR, Permission.VIEW_CLASSES,
        Permission.MANAGE_FEES, Permission.VIEW_FEES,
        Permission.VIEW_MESSAGES,
    },
    UserRole.TEACHER: {
        Permission.VIEW_STAFF, Permission.VIEW_STUDENTS, Permission.VIEW_PARENTS,
        Permission.VIEW_CALENDAR, Permission.VIEW_CLASSES, Permission.VIEW_COURSES,
        Permission.VIEW_TIMETABLE, Permission.MANAGE_MARKS, Permission.VIEW_MARKS,
        Permission.VIEW_FEES, Permission.SEND_MESSAGES, Permission.VIEW_MESSAGES,
    },
    UserRole.PARENT: {
        Permission.VIEW_CALENDAR, Permission.VIEW_CLASSES, Permission.VIEW_COURSES,
        Permission.VIEW_TIMETABLE, Permission.VIEW_OWN_MARKS, Permission.VIEW_OWN_FEES,
        Permission.VIEW_MESSAGES,
    },
    UserRole.STUDENT: {
        Permission.VIEW_CALENDAR, Permission.VIEW_CLASSES, Permission.VIEW_COURSES,
        Permission.VIEW_TIMETABLE, Permission.VIEW_OWN_MARKS, Permission.VIEW_OWN_FEES,
        Permission.VIEW_MESSAGES,
    },
}


def check_permission(user_roles: List[UserRole], required_permission: Permission) -> bool:
    """Check if user has required permission based on their roles"""
    for role in user_roles:
        if role == UserRole.SYSTEM_ADMIN:
            return True  # System admin has all permissions
        if required_permission in ROLE_PERMISSIONS.get(role, set()):
            return True
    return False


def require_permission(user_roles: List[UserRole], required_permission: Permission) -> None:
    """Raise HTTP exception if user doesn't have required permission"""
    if not check_permission(user_roles, required_permission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied. Required: {required_permission.value}"
        ) 