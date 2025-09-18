"""
API v1 router
"""
from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, schools, classes, enrollments

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(schools.router, prefix="/schools", tags=["schools"])
api_router.include_router(classes.router, prefix="/classes", tags=["classes"])
api_router.include_router(enrollments.router, prefix="/enrollments", tags=["enrollments"])