from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_fees():
    return {"message": "Fees endpoint - to be implemented"}