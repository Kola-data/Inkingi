"""
User and RBAC models
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel


class UserStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"


class RoleScopeEnum(str, enum.Enum):
    SYSTEM = "system"
    SCHOOL = "school"


class ScopeTypeEnum(str, enum.Enum):
    SCHOOL = "school"
    CLASS = "class"
    COURSE = "course"


# Association tables
user_role_table = Table(
    'user_roles',
    BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('school_id', Integer, ForeignKey('schools.id'), nullable=False),
)

role_permission_table = Table(
    'role_permissions',
    BaseModel.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True),
)


class User(BaseModel):
    """User model"""
    __tablename__ = "users"
    
    # Multi-tenancy
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    
    # Staff relationship (nullable for non-staff users like parents)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=True, unique=True)
    
    # Authentication
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    
    # Status
    status = Column(Enum(UserStatusEnum), default=UserStatusEnum.PENDING, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    
    # Relationships
    school = relationship("School", back_populates="users")
    staff = relationship("Staff", back_populates="user")
    roles = relationship("Role", secondary=user_role_table, back_populates="users")
    access_entries = relationship("AccessControlEntry", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', school_id={self.school_id})>"


class Role(BaseModel):
    """Role model for RBAC"""
    __tablename__ = "roles"
    
    name = Column(String(100), nullable=False, unique=True)
    scope = Column(Enum(RoleScopeEnum), default=RoleScopeEnum.SCHOOL, nullable=False)
    description = Column(String(500), nullable=True)
    
    # Relationships
    users = relationship("User", secondary=user_role_table, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permission_table, back_populates="roles")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}', scope='{self.scope}')>"


class Permission(BaseModel):
    """Permission model for RBAC"""
    __tablename__ = "permissions"
    
    name = Column(String(100), nullable=False, unique=True)
    resource = Column(String(100), nullable=False)  # e.g., 'class', 'user', 'fee'
    action = Column(String(50), nullable=False)     # e.g., 'create', 'read', 'update', 'delete'
    description = Column(String(500), nullable=True)
    
    # Relationships
    roles = relationship("Role", secondary=role_permission_table, back_populates="permissions")
    
    def __repr__(self):
        return f"<Permission(id={self.id}, name='{self.name}')>"


class UserRole(BaseModel):
    """User-Role association with school context"""
    __tablename__ = "user_roles_detail"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    
    # Relationships
    user = relationship("User")
    role = relationship("Role")
    school = relationship("School")


class RolePermission(BaseModel):
    """Role-Permission association"""
    __tablename__ = "role_permissions_detail"
    
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    
    # Relationships
    role = relationship("Role")
    permission = relationship("Permission")


class AccessControlEntry(BaseModel):
    """Fine-grained access control entries"""
    __tablename__ = "access_control_entries"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    scope_type = Column(Enum(ScopeTypeEnum), nullable=False)
    scope_id = Column(Integer, nullable=False)  # ID of the scope object (class_id, course_id, etc.)
    
    # Relationships
    school = relationship("School")
    user = relationship("User", back_populates="access_entries")
    
    def __repr__(self):
        return f"<AccessControlEntry(user_id={self.user_id}, scope_type='{self.scope_type}', scope_id={self.scope_id})>"