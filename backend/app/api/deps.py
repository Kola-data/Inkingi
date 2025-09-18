from typing import AsyncGenerator
from fastapi import Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from ..db.session import SessionLocal
from ..core.config import settings


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


async def get_tenant_db(
    x_school_id: int | None = Header(default=None),
) -> AsyncGenerator[AsyncSession, None]:
    """Yield a DB session with per-request tenant GUC set for Postgres.

    Sets `SET LOCAL app.tenant_id` when using Postgres to enable RLS policies.
    """
    if x_school_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing X-School-ID header for tenant context",
        )
    async with SessionLocal() as session:
        # Best-effort: only attempt on Postgres. Ignore on other engines.
        if settings.database_url.startswith("postgresql"):
            try:
                await session.execute(
                    text("SET LOCAL app.tenant_id = :tenant_id"),
                    {"tenant_id": int(x_school_id)},
                )
            except Exception:
                # Do not block request if SET fails (e.g., non-Postgres)
                pass
        yield session