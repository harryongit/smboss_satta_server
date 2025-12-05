"""Authentication routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.security import (
    hash_password, verify_password, create_access_token,
    create_refresh_token, verify_token, get_current_user
)
from app.models.user import User
from app.schemas.user import (
    UserRegisterRequest, UserLoginRequest, UserLoginResponse, UserResponse
)
from app.core.config import settings

router = APIRouter()

# Registration is disabled per requirements

@router.post("/login", response_model=UserLoginResponse)
async def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """User login"""
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user or not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    # Create tokens
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "username": user.username},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return UserLoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": user.id,
            "username": user.username,
            "mobile": user.mobile
        }
    )

@router.post("/refresh-token")
async def refresh_token(token: str):
    """Refresh access token"""
    payload = verify_token(token)
    
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    access_token = create_access_token(data={"sub": payload.get("sub")})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout endpoint"""
    return {"status": "success", "message": "Logged out successfully"}

@router.get("/verify")
async def verify(current_user: dict = Depends(get_current_user)):
    """Verify active token"""
    return {
        "status": "success",
        "user": current_user
    }
