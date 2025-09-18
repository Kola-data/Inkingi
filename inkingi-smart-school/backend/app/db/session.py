"""
Database session management
"""
from contextlib import asynccontextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.core.config import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    poolclass=StaticPool,
    connect_args={
        "check_same_thread": False  # Only needed for SQLite
    } if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def get_db_context():
    """Get database session as async context manager"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def set_tenant_context(db: Session, tenant_id: int) -> None:
    """Set tenant context for Row-Level Security"""
    if tenant_id:
        db.execute(text(f"SET app.tenant_id = '{tenant_id}'"))


def clear_tenant_context(db: Session) -> None:
    """Clear tenant context"""
    db.execute(text("RESET app.tenant_id"))