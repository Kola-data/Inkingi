from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def list_timetables():
    return {"message": "Timetable endpoints - to be implemented"}

@router.post("")
async def create_timetable(data: dict):
    return {"message": "Create timetable endpoint - to be implemented"} 