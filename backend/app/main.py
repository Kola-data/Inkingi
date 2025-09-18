from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine

from .core.config import settings
from .db.session import Base, engine

# Import all routers
from .api.routers.auth import router as auth_router
from .api.routers.schools import router as schools_router
from .api.routers.users import router as users_router
from .api.routers.people import router as people_router
from .api.routers.calendar import router as calendar_router
from .api.routers.classes import router as classes_router
from .api.routers.courses import router as courses_router
from .api.routers.enrollments import router as enrollments_router
from .api.routers.timetable import router as timetable_router
from .api.routers.marks import router as marks_router
from .api.routers.finance import router as finance_router
from .api.routers.inventory import router as inventory_router
from .api.routers.messages import router as messages_router

app = FastAPI(
    title="Inkingi Smart School API",
    version="1.0.0",
    description="Multi-tenant school management platform"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(auth_router, prefix="/auth", tags=["authentication"])
app.include_router(schools_router, prefix="/schools", tags=["schools"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(people_router, prefix="", tags=["people"])  # /staff, /students, /parents
app.include_router(calendar_router, prefix="/calendar", tags=["calendar"])
app.include_router(classes_router, prefix="/classes", tags=["classes"])
app.include_router(courses_router, prefix="/courses", tags=["courses"])
app.include_router(enrollments_router, prefix="/enrollments", tags=["enrollments"])
app.include_router(timetable_router, prefix="/timetable", tags=["timetable"])
app.include_router(marks_router, prefix="/marks", tags=["marks"])
app.include_router(finance_router, prefix="/finance", tags=["finance"])
app.include_router(inventory_router, prefix="/inventory", tags=["inventory"])
app.include_router(messages_router, prefix="/messages", tags=["messages"])


@app.on_event("startup")
async def on_startup_create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def read_root():
    return {
        "service": "inkingi-backend",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "Multi-tenant school management",
            "Role-based access control",
            "Academic calendar",
            "Student enrollment",
            "Marks and reports",
            "Fee management",
            "Inventory tracking",
            "Communication (Email/SMS)"
        ]
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"} 