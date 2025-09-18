from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def list_users():
    return {"message": "Users endpoint - to be implemented"}


@router.post("")
async def create_user(user_data: dict):
    return {"message": "Create user endpoint - to be implemented"}


@router.patch("/{user_id}")
async def update_user(user_id: int, user_data: dict):
    return {"message": f"Update user {user_id} endpoint - to be implemented"} 