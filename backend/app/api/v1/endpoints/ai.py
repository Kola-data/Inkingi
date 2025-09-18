from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_chat_sessions():
    return {"message": "AI endpoint - to be implemented"}