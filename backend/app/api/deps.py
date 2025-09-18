from typing import AsyncGenerator
from fastapi import Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.session import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


def get_tenant_school_id(x_school_id: int | None = Header(default=None)) -> int:
    if x_school_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing X-School-ID header for tenant context",
        )
    return x_school_id 