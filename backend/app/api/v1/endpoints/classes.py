from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_classes():
    return {"message": "Classes endpoint - to be implemented"}