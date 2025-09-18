"""
Schools endpoints
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.school import SchoolCreate, SchoolResponse, SchoolUpdate
from app.services.school import SchoolService

router = APIRouter()


@router.post("/", response_model=SchoolResponse)
def create_school(
    *,
    db: Session = Depends(get_db),
    school_in: SchoolCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new school
    """
    # Only system admins can create schools
    if not any(role.name == "system_admin" for role in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    school_service = SchoolService()
    
    # Check if school with slug already exists
    if school_service.get_school_by_slug(db, school_in.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="School with this slug already exists"
        )
    
    school = school_service.create_school(db, school_in)
    return school


@router.get("/", response_model=List[SchoolResponse])
def read_schools(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve schools
    """
    # Only system admins can list all schools
    if not any(role.name == "system_admin" for role in current_user.roles):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    school_service = SchoolService()
    schools = school_service.get_schools(db, skip=skip, limit=limit)
    return schools


@router.get("/{school_id}", response_model=SchoolResponse)
def read_school(
    *,
    db: Session = Depends(get_db),
    school_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get school by ID
    """
    school_service = SchoolService()
    school = school_service.get_school(db, school_id)
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    # Users can only access their own school unless they're system admin
    if (current_user.school_id != school_id and 
        not any(role.name == "system_admin" for role in current_user.roles)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return school


@router.put("/{school_id}", response_model=SchoolResponse)
def update_school(
    *,
    db: Session = Depends(get_db),
    school_id: int,
    school_in: SchoolUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update school
    """
    school_service = SchoolService()
    school = school_service.get_school(db, school_id)
    
    if not school:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="School not found"
        )
    
    # Only system admins or school admins can update school
    can_update = (
        any(role.name == "system_admin" for role in current_user.roles) or
        (current_user.school_id == school_id and 
         any(role.name == "school_admin" for role in current_user.roles))
    )
    
    if not can_update:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    school = school_service.update_school(db, school, school_in)
    return school