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

@router.post(
    "/login/user",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "<jwt>",
                        "refresh_token": "<jwt>",
                        "token_type": "bearer",
                        "user": {"id": 1, "username": "user1", "mobile": "9999999999"}
                    }
                }
            }
        },
        401: {"content": {"application/json": {"example": {"detail": "Invalid credentials"}}}},
        403: {"content": {"application/json": {"example": {"detail": "User account is inactive"}}}},
        500: {"content": {"application/json": {"example": {"detail": "Internal server error"}}}},
    },
)
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
        data={"sub": user.id, "username": user.username, "role": "user"},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.id, "role": "user"})
    
    return {
        "http_status": 200,
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "mobile": user.mobile
            }
        }
    }

@router.post(
    "/login/admin",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "<jwt>",
                        "refresh_token": "<jwt>",
                        "token_type": "bearer",
                        "user": {"id": 1, "username": "admin", "mobile": "0000000000"}
                    }
                }
            }
        },
        401: {"content": {"application/json": {"example": {"detail": "Invalid credentials"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin account required"}}}},
        500: {"content": {"application/json": {"example": {"detail": "Internal server error"}}}},
    },
)
async def admin_login(request: UserLoginRequest, db: Session = Depends(get_db)):
    """Admin login"""
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user and request.username.lower() == "admin":
        user = User(
            username="admin",
            mobile="0000000000",
            email=None,
            password=hash_password("admin"),
            status=1,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    if not user or user.username.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account required"
        )
    
    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    if user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin account is inactive"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "username": user.username, "role": "admin"},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.id, "role": "admin"})
    
    return {
        "http_status": 200,
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "mobile": user.mobile
            }
        }
    }

@router.post(
    "/tokens/refresh",
    responses={
        200: {"content": {"application/json": {"example": {"access_token": "<jwt>", "token_type": "bearer"}}}},
        401: {"content": {"application/json": {"example": {"detail": "Invalid refresh token"}}}},
        500: {"content": {"application/json": {"example": {"detail": "Internal server error"}}}},
    },
)
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
        "http_status": 200,
        "success": True,
        "message": "Token refreshed",
        "data": {
            "access_token": access_token,
            "token_type": "bearer"
        }
    }

@router.post(
    "/logout",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "message": "Logged out successfully"}}}},
        401: {"content": {"application/json": {"example": {"detail": "Not authenticated"}}}},
    },
)
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout endpoint"""
    return {"http_status": 200, "success": True, "message": "Logged out", "data": {"message": "Logged out successfully"}}

@router.get(
    "/tokens/verify",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "user": {"sub": 1, "username": "user1", "role": "user"}}}}},
        401: {"content": {"application/json": {"example": {"detail": "Invalid token"}}}},
    },
)
async def verify(current_user: dict = Depends(get_current_user)):
    """Verify active token"""
    return {"http_status": 200, "success": True, "message": "Token valid", "data": {"user": current_user}}
