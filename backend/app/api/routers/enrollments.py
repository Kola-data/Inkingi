from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.deps import get_db, get_tenant_school_id
from ...models.academics import Enrollment, Class
from ...models.calendar import AcademicYear
from ...models.school import Student
from ...schemas.enrollments import EnrollmentCreate, EnrollmentOut

router = APIRouter()


@router.post("", response_model=EnrollmentOut)
async def enroll_student(
    payload: EnrollmentCreate,
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    student = await db.get(Student, payload.student_id)
    if not student or student.school_id != school_id:
        raise HTTPException(status_code=404, detail="Student not found")
    cls = await db.get(Class, payload.class_id)
    if not cls or cls.school_id != school_id:
        raise HTTPException(status_code=404, detail="Class not found")

    academic_year_id = payload.academic_year_id
    if academic_year_id is None:
        res = await db.execute(
            select(AcademicYear).where(
                AcademicYear.school_id == school_id, AcademicYear.is_current == True
            )
        )
        year = res.scalars().first()
        if not year:
            raise HTTPException(status_code=409, detail="No current academic year set")
        academic_year_id = year.id

    enrollment = Enrollment(
        school_id=school_id,
        student_id=payload.student_id,
        class_id=payload.class_id,
        academic_year_id=academic_year_id,
        status="active",
    )
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment 