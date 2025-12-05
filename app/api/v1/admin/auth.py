from fastapi import APIRouter, HTTPException, status

from app.schemas.user import UserCreate, UserLogin, Token
from app.services import admin_service


router = APIRouter(prefix="/admin/auth")


@router.post("/register", response_model=dict)
def register(data: UserCreate):
    admin_service.register_admin(data.username, data.email, data.password)
    return {"message": "admin registered"}


@router.post("/login", response_model=Token)
def login(data: UserLogin):
    token = admin_service.login_admin(data.username, data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return Token(access_token=token)

