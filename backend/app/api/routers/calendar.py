from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.deps import get_db, get_tenant_school_id
from ...models.calendar import AcademicYear
from ...schemas.calendar import AcademicYearCreate, AcademicYearOut

router = APIRouter()


@router.post("/academic-years", response_model=AcademicYearOut)
async def create_academic_year(
    payload: AcademicYearCreate,
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    year = AcademicYear(
        school_id=school_id,
        name=payload.name,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_current=False,
    )
    db.add(year)
    await db.commit()
    await db.refresh(year)
    return year


@router.post("/academic-years/{year_id}/set-current")
async def set_current_year(
    year_id: int,
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    await db.execute(
        update(AcademicYear)
        .where(AcademicYear.school_id == school_id)
        .values(is_current=False)
    )
    year = await db.get(AcademicYear, year_id)
    if not year or year.school_id != school_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Year not found")
    year.is_current = True
    await db.commit()
    return {"ok": True}


@router.get("/academic-years/current", response_model=AcademicYearOut)
async def get_current_year(
    db: AsyncSession = Depends(get_db),
    school_id: int = Depends(get_tenant_school_id),
):
    res = await db.execute(
        select(AcademicYear).where(
            AcademicYear.school_id == school_id, AcademicYear.is_current == True
        )
    )
    year = res.scalars().first()
    if not year:
        raise HTTPException(status_code=409, detail="No current academic year set")
    return year 