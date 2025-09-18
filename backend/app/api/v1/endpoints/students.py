from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_students():
    return {"message": "Students endpoint - to be implemented"}