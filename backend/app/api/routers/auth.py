from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    # TODO: Implement actual authentication
    if credentials.email == "admin@example.com" and credentials.password == "admin":
        return TokenResponse(access_token="fake-jwt-token")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )


@router.post("/register")
async def register(user_data: dict):
    # TODO: Implement user registration
    return {"message": "Registration endpoint - to be implemented"}


@router.post("/refresh")
async def refresh_token():
    # TODO: Implement token refresh
    return {"message": "Token refresh endpoint - to be implemented"} 