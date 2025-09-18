from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_async_session, with_tenant
from app.api.deps import get_current_user, get_current_school, require_school_admin
from app.models.user import User
from app.models.school import School
from app.models.academic import Class, ClassTeacher, Enrollment, AcademicYear
from app.models.staff import Staff
from app.models.student import Student
from app.schemas.classes import (
    ClassCreate, ClassResponse, ClassUpdate,
    ClassTeacherAssign, ClassTeacherResponse,
    EnrollmentCreate, EnrollmentResponse
)
from datetime import date
import uuid

router = APIRouter()


@router.post("/", response_model=ClassResponse)
async def create_class(
    class_data: ClassCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_school_admin),
    current_school: School = Depends(get_current_school)
):
    """Create a new class"""
    async with with_tenant(db, str(current_school.id)):
        # Check if class name already exists
        result = await db.execute(
            select(Class).where(
                Class.school_id == current_school.id,
                Class.name == class_data.name
            )
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Class with this name already exists"
            )
        
        # Create class
        new_class = Class(
            id=uuid.uuid4(),
            school_id=current_school.id,
            name=class_data.name,
            level=class_data.level,
            section=class_data.section,
            capacity=class_data.capacity,
            description=class_data.description,
            status="active"
        )
        db.add(new_class)
        await db.commit()
        await db.refresh(new_class)
        
        return ClassResponse.from_orm(new_class)


@router.get("/", response_model=List[ClassResponse])
async def list_classes(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
    current_school: School = Depends(get_current_school)
):
    """List all classes for the current school"""
    async with with_tenant(db, str(current_school.id)):
        result = await db.execute(
            select(Class).where(
                Class.school_id == current_school.id,
                Class.status == "active"
            ).order_by(Class.level, Class.name)
        )
        classes = result.scalars().all()
        
        return [ClassResponse.from_orm(cls) for cls in classes]


@router.get("/{class_id}", response_model=ClassResponse)
async def get_class(
    class_id: str,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
    current_school: School = Depends(get_current_school)
):
    """Get a specific class by ID"""
    async with with_tenant(db, str(current_school.id)):
        result = await db.execute(
            select(Class).where(
                Class.id == class_id,
                Class.school_id == current_school.id
            )
        )
        class_obj = result.scalar_one_or_none()
        
        if not class_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
        
        return ClassResponse.from_orm(class_obj)


@router.put("/{class_id}", response_model=ClassResponse)
async def update_class(
    class_id: str,
    class_data: ClassUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_school_admin),
    current_school: School = Depends(get_current_school)
):
    """Update a class"""
    async with with_tenant(db, str(current_school.id)):
        result = await db.execute(
            select(Class).where(
                Class.id == class_id,
                Class.school_id == current_school.id
            )
        )
        class_obj = result.scalar_one_or_none()
        
        if not class_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
        
        # Update fields
        for field, value in class_data.dict(exclude_unset=True).items():
            setattr(class_obj, field, value)
        
        await db.commit()
        await db.refresh(class_obj)
        
        return ClassResponse.from_orm(class_obj)


@router.post("/{class_id}/assign-teacher", response_model=ClassTeacherResponse)
async def assign_class_teacher(
    class_id: str,
    assignment: ClassTeacherAssign,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_school_admin),
    current_school: School = Depends(get_current_school)
):
    """Assign a teacher to a class"""
    async with with_tenant(db, str(current_school.id)):
        # Verify class exists
        class_result = await db.execute(
            select(Class).where(
                Class.id == class_id,
                Class.school_id == current_school.id
            )
        )
        class_obj = class_result.scalar_one_or_none()
        if not class_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found"
            )
        
        # Verify staff exists
        staff_result = await db.execute(
            select(Staff).where(
                Staff.id == assignment.staff_id,
                Staff.school_id == current_school.id,
                Staff.status == "active"
            )
        )
        staff = staff_result.scalar_one_or_none()
        if not staff:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Staff member not found or inactive"
            )
        
        # Deactivate existing primary teacher if assigning new primary
        if assignment.is_primary:
            existing_result = await db.execute(
                select(ClassTeacher).where(
                    ClassTeacher.class_id == class_id,
                    ClassTeacher.is_active == True,
                    ClassTeacher.is_primary == True
                )
            )
            existing = existing_result.scalar_one_or_none()
            if existing:
                existing.is_active = False
        
        # Create new assignment
        class_teacher = ClassTeacher(
            id=uuid.uuid4(),
            school_id=current_school.id,
            class_id=class_id,
            staff_id=assignment.staff_id,
            assigned_at=date.today(),
            is_active=True,
            is_primary=assignment.is_primary
        )
        db.add(class_teacher)
        await db.commit()
        await db.refresh(class_teacher)
        
        return ClassTeacherResponse(
            id=str(class_teacher.id),
            class_id=str(class_teacher.class_id),
            staff_id=str(class_teacher.staff_id),
            assigned_at=class_teacher.assigned_at,
            is_active=class_teacher.is_active,
            is_primary=class_teacher.is_primary,
            teacher_name=f"{staff.first_name} {staff.last_name}",
            class_name=class_obj.name
        )


@router.post("/enrollments", response_model=EnrollmentResponse)
async def create_enrollment(
    enrollment_data: EnrollmentCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(require_school_admin),
    current_school: School = Depends(get_current_school)
):
    """Enroll a student in a class"""
    async with with_tenant(db, str(current_school.id)):
        # Get current academic year if not provided
        academic_year_id = enrollment_data.academic_year_id
        if not academic_year_id:
            year_result = await db.execute(
                select(AcademicYear).where(
                    AcademicYear.school_id == current_school.id,
                    AcademicYear.is_current == True
                )
            )
            current_year = year_result.scalar_one_or_none()
            if not current_year:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="No current academic year set. Please set a current academic year first."
                )
            academic_year_id = current_year.id
        
        # Verify student exists
        student_result = await db.execute(
            select(Student).where(
                Student.id == enrollment_data.student_id,
                Student.school_id == current_school.id,
                Student.status == "active"
            )
        )
        student = student_result.scalar_one_or_none()
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found or inactive"
            )
        
        # Verify class exists
        class_result = await db.execute(
            select(Class).where(
                Class.id == enrollment_data.class_id,
                Class.school_id == current_school.id,
                Class.status == "active"
            )
        )
        class_obj = class_result.scalar_one_or_none()
        if not class_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Class not found or inactive"
            )
        
        # Check if already enrolled
        existing_result = await db.execute(
            select(Enrollment).where(
                Enrollment.student_id == enrollment_data.student_id,
                Enrollment.class_id == enrollment_data.class_id,
                Enrollment.academic_year_id == academic_year_id
            )
        )
        if existing_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student is already enrolled in this class for this academic year"
            )
        
        # Create enrollment
        enrollment = Enrollment(
            id=uuid.uuid4(),
            school_id=current_school.id,
            student_id=enrollment_data.student_id,
            class_id=enrollment_data.class_id,
            academic_year_id=academic_year_id,
            enrolled_at=date.today(),
            status="active"
        )
        db.add(enrollment)
        await db.commit()
        await db.refresh(enrollment)
        
        return EnrollmentResponse(
            id=str(enrollment.id),
            student_id=str(enrollment.student_id),
            class_id=str(enrollment.class_id),
            academic_year_id=str(enrollment.academic_year_id),
            enrolled_at=enrollment.enrolled_at,
            status=enrollment.status,
            student_name=f"{student.first_name} {student.last_name}",
            student_admission_number=student.admission_number,
            class_name=class_obj.name
        )


@router.get("/{class_id}/students", response_model=List[EnrollmentResponse])
async def get_class_students(
    class_id: str,
    academic_year_id: str = None,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
    current_school: School = Depends(get_current_school)
):
    """Get all students enrolled in a class"""
    async with with_tenant(db, str(current_school.id)):
        # Get academic year
        if not academic_year_id:
            year_result = await db.execute(
                select(AcademicYear).where(
                    AcademicYear.school_id == current_school.id,
                    AcademicYear.is_current == True
                )
            )
            current_year = year_result.scalar_one_or_none()
            if not current_year:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="No current academic year set"
                )
            academic_year_id = current_year.id
        
        # Get enrollments with student details
        result = await db.execute(
            select(Enrollment, Student, Class).join(
                Student, Enrollment.student_id == Student.id
            ).join(
                Class, Enrollment.class_id == Class.id
            ).where(
                Enrollment.class_id == class_id,
                Enrollment.academic_year_id == academic_year_id,
                Enrollment.status == "active"
            ).order_by(Student.first_name, Student.last_name)
        )
        
        enrollments = []
        for enrollment, student, class_obj in result:
            enrollments.append(EnrollmentResponse(
                id=str(enrollment.id),
                student_id=str(enrollment.student_id),
                class_id=str(enrollment.class_id),
                academic_year_id=str(enrollment.academic_year_id),
                enrolled_at=enrollment.enrolled_at,
                status=enrollment.status,
                student_name=f"{student.first_name} {student.last_name}",
                student_admission_number=student.admission_number,
                class_name=class_obj.name
            ))
        
        return enrollments