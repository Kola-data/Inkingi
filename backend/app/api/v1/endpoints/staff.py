from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_staff():
    return {"message": "Staff endpoint - to be implemented"}