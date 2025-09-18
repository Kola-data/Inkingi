from sqlalchemy import Column, String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    status = Column(String(20), default="active")  # active, inactive, suspended
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)
    
    # Relationships
    school = relationship("School", back_populates="users")
    staff = relationship("Staff", back_populates="user")
    user_roles = relationship("UserRole", back_populates="user")
    roles = relationship("Role", secondary="user_roles", back_populates="users")

class Role(BaseModel):
    __tablename__ = "roles"
    
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    scope = Column(String(50), default="school")  # system, school
    
    # Relationships
    user_roles = relationship("UserRole", back_populates="role")
    users = relationship("User", secondary="user_roles", back_populates="roles")
    role_permissions = relationship("RolePermission", back_populates="role")

class Permission(BaseModel):
    __tablename__ = "permissions"
    
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    resource = Column(String(100), nullable=False)  # school, user, class, course, etc.
    action = Column(String(50), nullable=False)  # create, read, update, delete, manage
    
    # Relationships
    role_permissions = relationship("RolePermission", back_populates="permission")

class UserRole(BaseModel):
    __tablename__ = "user_roles"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    assigned_at = Column(DateTime(timezone=True), nullable=False)
    assigned_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="user_roles", foreign_keys=[user_id])
    role = relationship("Role", back_populates="user_roles")
    school = relationship("School")
    assigned_by_user = relationship("User", foreign_keys=[assigned_by])

class RolePermission(BaseModel):
    __tablename__ = "role_permissions"
    
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    
    # Relationships
    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")