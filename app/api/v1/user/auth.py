from fastapi import APIRouter, HTTPException, status

from app.schemas.user import UserCreate, UserLogin, Token
from app.services import user_service


router = APIRouter(prefix="/user/auth")


@router.post("/register", response_model=dict)
def register(data: UserCreate):
    user_service.create_user(data.username, data.email, data.password, role=data.role)
    return {"message": "user registered"}


@router.post("/login", response_model=Token)
def login(data: UserLogin):
    token = user_service.authenticate(data.username, data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return Token(access_token=token)

