from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.schools import router as schools_router
from app.api.v1.users import router as users_router
from app.api.v1.people import router as people_router
from app.api.v1.calendar import router as calendar_router
from app.api.v1.classes import router as classes_router
from app.api.v1.courses import router as courses_router
from app.api.v1.timetable import router as timetable_router
from app.api.v1.marks import router as marks_router
from app.api.v1.fees import router as fees_router
from app.api.v1.inventory import router as inventory_router
from app.api.v1.communication import router as communication_router
from app.api.v1.ai import router as ai_router

api_router = APIRouter()

# Include all routers
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(schools_router, prefix="/schools", tags=["Schools"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(people_router, prefix="/people", tags=["People"])
api_router.include_router(calendar_router, prefix="/calendar", tags=["Academic Calendar"])
api_router.include_router(classes_router, prefix="/classes", tags=["Classes"])
api_router.include_router(courses_router, prefix="/courses", tags=["Courses"])
api_router.include_router(timetable_router, prefix="/timetable", tags=["Timetable"])
api_router.include_router(marks_router, prefix="/marks", tags=["Marks"])
api_router.include_router(fees_router, prefix="/fees", tags=["Fees"])
api_router.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])
api_router.include_router(communication_router, prefix="/communication", tags=["Communication"])
api_router.include_router(ai_router, prefix="/ai", tags=["AI Agent"])