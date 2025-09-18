from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_timetables():
    return {"message": "Timetable endpoint - to be implemented"}