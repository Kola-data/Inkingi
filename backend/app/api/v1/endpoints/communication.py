from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_messages():
    return {"message": "Communication endpoint - to be implemented"}