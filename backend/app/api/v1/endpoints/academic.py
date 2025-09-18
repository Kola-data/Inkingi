from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_academic_years():
    return {"message": "Academic years endpoint - to be implemented"}