"""
Enrollments endpoints
"""
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_tenant
from app.db.session import get_db
from app.models.user import User
from app.schemas.academic import EnrollmentCreate, EnrollmentResponse
from app.services.academic import EnrollmentService, AcademicYearService

router = APIRouter()


@router.post("/", response_model=EnrollmentResponse)
def create_enrollment(
    *,
    db: Session = Depends(get_db),
    enrollment_in: EnrollmentCreate,
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(require_tenant)
) -> Any:
    """
    Enroll student in class
    """
    # Check permissions
    can_enroll = (
        any(role.name in ["system_admin", "school_admin"] for role in current_user.roles)
    )
    
    if not can_enroll:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to enroll student"
        )
    
    enrollment_service = EnrollmentService()
    academic_year_service = AcademicYearService()
    
    # Get current academic year if not provided
    academic_year_id = enrollment_in.academic_year_id
    if not academic_year_id:
        current_year = academic_year_service.get_current_academic_year(db, tenant_id)
        if not current_year:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No current academic year set. Please set a current academic year first."
            )
        academic_year_id = current_year.id
    
    # Check if student is already enrolled in this class for this academic year
    existing_enrollment = enrollment_service.get_enrollment_by_student_class_year(
        db, enrollment_in.student_id, enrollment_in.class_id, academic_year_id, tenant_id
    )
    
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already enrolled in this class for this academic year"
        )
    
    # Create enrollment
    enrollment_data = enrollment_in.model_copy()
    enrollment_data.academic_year_id = academic_year_id
    
    enrollment = enrollment_service.create_enrollment(db, enrollment_data, tenant_id)
    return enrollment


@router.get("/", response_model=List[EnrollmentResponse])
def read_enrollments(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    class_id: int = None,
    student_id: int = None,
    academic_year_id: int = None,
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(require_tenant)
) -> Any:
    """
    Retrieve enrollments with optional filters
    """
    enrollment_service = EnrollmentService()
    enrollments = enrollment_service.get_enrollments(
        db, 
        tenant_id,
        skip=skip, 
        limit=limit,
        class_id=class_id,
        student_id=student_id,
        academic_year_id=academic_year_id
    )
    return enrollments


@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
def read_enrollment(
    *,
    db: Session = Depends(get_db),
    enrollment_id: int,
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(require_tenant)
) -> Any:
    """
    Get enrollment by ID
    """
    enrollment_service = EnrollmentService()
    enrollment = enrollment_service.get_enrollment(db, enrollment_id, tenant_id)
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    return enrollment


@router.delete("/{enrollment_id}", response_model=dict)
def delete_enrollment(
    *,
    db: Session = Depends(get_db),
    enrollment_id: int,
    current_user: User = Depends(get_current_user),
    tenant_id: int = Depends(require_tenant)
) -> Any:
    """
    Delete enrollment (withdraw student)
    """
    # Check permissions
    can_delete = (
        any(role.name in ["system_admin", "school_admin"] for role in current_user.roles)
    )
    
    if not can_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to withdraw student"
        )
    
    enrollment_service = EnrollmentService()
    enrollment = enrollment_service.get_enrollment(db, enrollment_id, tenant_id)
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    # Update status to withdrawn instead of deleting
    enrollment_service.withdraw_enrollment(db, enrollment)
    return {"message": "Student withdrawn successfully"}