from fastapi import APIRouter
from app.api.v1.endpoints import auth, schools, users, staff, students, academic, classes, courses, timetable, marks, fees, inventory, communication

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(schools.router, prefix="/schools", tags=["schools"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(staff.router, prefix="/staff", tags=["staff"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(academic.router, prefix="/academic", tags=["academic"])
api_router.include_router(classes.router, prefix="/classes", tags=["classes"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(timetable.router, prefix="/timetable", tags=["timetable"])
api_router.include_router(marks.router, prefix="/marks", tags=["marks"])
api_router.include_router(fees.router, prefix="/fees", tags=["fees"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(communication.router, prefix="/communication", tags=["communication"])