from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_items():
    return {"message": f"{module} endpoint - to be implemented"}
