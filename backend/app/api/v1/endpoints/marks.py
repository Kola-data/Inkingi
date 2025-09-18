from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_marks():
    return {"message": "Marks endpoint - to be implemented"}