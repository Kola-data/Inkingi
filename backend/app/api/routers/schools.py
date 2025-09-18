from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...api.deps import get_db
from ...models.school import School

router = APIRouter()


@router.post("")
async def create_school(
    school_data: dict,
    db: AsyncSession = Depends(get_db),
):
    school = School(
        name=school_data["name"],
        slug=school_data["slug"],
        contact_email=school_data.get("contact_email"),
        contact_phone=school_data.get("contact_phone"),
        status="active"
    )
    db.add(school)
    await db.commit()
    await db.refresh(school)
    return school


@router.get("")
async def list_schools(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(School).where(School.status == "active"))
    return result.scalars().all()


@router.get("/{school_id}")
async def get_school(school_id: int, db: AsyncSession = Depends(get_db)):
    school = await db.get(School, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school 