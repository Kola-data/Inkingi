from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.pool import NullPool
from .config import settings


# Custom naming convention for constraints
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = metadata


# Async engine for async operations
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=settings.DATABASE_POOL_PRE_PING,
)

# Sync engine for migrations
sync_engine = create_engine(
    settings.DATABASE_SYNC_URL,
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=settings.DATABASE_POOL_PRE_PING,
)

# Session factories
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

SessionLocal = sessionmaker(
    sync_engine,
    autocommit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for FastAPI routes to get DB session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_session():
    """Get sync session for Celery tasks"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


class TenantContext:
    """Context manager for setting tenant context in PostgreSQL"""
    
    def __init__(self, session: AsyncSession, tenant_id: Optional[str] = None):
        self.session = session
        self.tenant_id = tenant_id
    
    async def __aenter__(self):
        if self.tenant_id:
            await self.session.execute(
                f"SET LOCAL app.tenant_id = '{self.tenant_id}'"
            )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.tenant_id:
            await self.session.execute("RESET app.tenant_id")


@asynccontextmanager
async def with_tenant(session: AsyncSession, tenant_id: Optional[str] = None):
    """Set tenant context for the session"""
    if tenant_id:
        await session.execute(f"SET LOCAL app.tenant_id = '{tenant_id}'")
    try:
        yield session
    finally:
        if tenant_id:
            await session.execute("RESET app.tenant_id")