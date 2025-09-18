"""
Classes endpoints
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_tenant
from app.db.session import get_db
from app.models.user import User
from app.schemas.academic import ClassCreate, ClassResponse, ClassUpdate, ClassTeacherAssign
from app.services.academic import ClassService

router = APIRouter()


@router.post("/", response_model=ClassResponse)
def create_class(
    *,
    db: Session = Depends(get_db),
    class_in: ClassCreate,
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(require_tenant)
) -> Any:
    """
    Create new class
    """
    # Check permissions - school admin or system admin
    can_create = (
        any(role.name in ["system_admin", "school_admin"] for role in current_user.roles)
    )
    
    if not can_create:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to create class"
        )
    
    class_service = ClassService()
    
    # Check if class with same name exists in school
    existing_class = class_service.get_class_by_name(db, tenant_id, class_in.name)
    if existing_class:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Class with this name already exists"
        )
    
    class_obj = class_service.create_class(db, class_in, tenant_id)
    return class_obj


@router.get("/", response_model=List[ClassResponse])
def read_classes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(require_tenant)
) -> Any:
    """
    Retrieve classes for the current school
    """
    class_service = ClassService()
    classes = class_service.get_classes(db, tenant_id, skip=skip, limit=limit)
    return classes


@router.get("/{class_id}", response_model=ClassResponse)
def read_class(
    *,
    db: Session = Depends(get_db),
    class_id: int,
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(require_tenant)
) -> Any:
    """
    Get class by ID
    """
    class_service = ClassService()
    class_obj = class_service.get_class(db, class_id, tenant_id)
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    return class_obj


@router.put("/{class_id}", response_model=ClassResponse)
def update_class(
    *,
    db: Session = Depends(get_db),
    class_id: int,
    class_in: ClassUpdate,
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(require_tenant)
) -> Any:
    """
    Update class
    """
    # Check permissions
    can_update = (
        any(role.name in ["system_admin", "school_admin"] for role in current_user.roles)
    )
    
    if not can_update:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to update class"
        )
    
    class_service = ClassService()
    class_obj = class_service.get_class(db, class_id, tenant_id)
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    class_obj = class_service.update_class(db, class_obj, class_in)
    return class_obj


@router.post("/{class_id}/assign-teacher", response_model=dict)
def assign_teacher_to_class(
    *,
    db: Session = Depends(get_db),
    class_id: int,
    assignment: ClassTeacherAssign,
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(require_tenant)
) -> Any:
    """
    Assign teacher to class (homeroom teacher)
    """
    # Check permissions
    can_assign = (
        any(role.name in ["system_admin", "school_admin"] for role in current_user.roles)
    )
    
    if not can_assign:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to assign teacher"
        )
    
    class_service = ClassService()
    
    # Verify class exists
    class_obj = class_service.get_class(db, class_id, tenant_id)
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    # Assign teacher
    try:
        class_service.assign_teacher_to_class(
            db, class_id, assignment.staff_id, tenant_id
        )
        return {"message": "Teacher assigned successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{class_id}", response_model=dict)
def delete_class(
    *,
    db: Session = Depends(get_db),
    class_id: int,
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(require_tenant)
) -> Any:
    """
    Delete class
    """
    # Check permissions
    can_delete = (
        any(role.name in ["system_admin", "school_admin"] for role in current_user.roles)
    )
    
    if not can_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete class"
        )
    
    class_service = ClassService()
    class_obj = class_service.get_class(db, class_id, tenant_id)
    
    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )
    
    # Check if class has enrollments
    if class_obj.enrollments:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete class with enrolled students"
        )
    
    class_service.delete_class(db, class_obj)
    return {"message": "Class deleted successfully"}