"""Admin endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.user import User
from app.models.game import Game
from app.models.result import Result
from app.models.rashi import Rashi
from app.models.starline import StarLine
from app.models.freefix import FreeFix
from app.models.auditlog import AuditLog
from app.schemas.user import UserRegisterRequest
from pydantic import BaseModel, Field
from typing import Optional
from app.jobs.sync_results import ResultSyncJob

router = APIRouter()

@router.get(
    "/dashboard",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "stats": {"total_users": 10, "total_markets": 5, "total_results": 100, "timestamp": "2025-12-06T12:00:00Z"}}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def admin_dashboard(
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Admin dashboard stats"""
    total_users = db.query(User).filter(User.status == 1).count()
    total_markets = db.query(Game).filter(Game.status == 1).count()
    total_results = db.query(Result).count()
    
    return {
        "http_status": 200,
        "success": True,
        "message": "OK",
        "data": {
            "stats": {
                "total_users": total_users,
                "total_markets": total_markets,
                "total_results": total_results,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    }

@router.get(
    "/users",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "users": [{"id": 1, "username": "user1", "mobile": "9999999999", "email": None, "status": 1, "created_at": "2025-12-01T12:00:00Z"}], "total": 1, "limit": 50, "offset": 0}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def list_users(
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    users = db.query(User).limit(limit).offset(offset).all()
    total = db.query(User).count()
    
    return {
        "http_status": 200,
        "success": True,
        "message": "Users fetched",
        "data": {
            "users": [
            {
                "id": u.id,
                "username": u.username,
                "mobile": u.mobile,
                "email": u.email,
                "status": u.status,
                "created_at": u.created_at.isoformat()
            }
            for u in users
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

class UserUpdateRequest(BaseModel):
    mobile: Optional[str] = Field(None, pattern="^[0-9]{10}$")
    email: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)
    status: Optional[int] = None

@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"content": {"application/json": {"example": {"status": "success", "user_id": 1}}}},
        400: {"content": {"application/json": {"example": {"detail": "Username already exists"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def create_user(
    request: UserRegisterRequest,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    existing_username = db.query(User).filter(User.username == request.username).first()
    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    if request.email:
        existing_email = db.query(User).filter(User.email == request.email).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    from app.core.security import hash_password
    user = User(
        username=request.username,
        mobile=request.mobile,
        email=request.email,
        password=hash_password(request.password),
        status=1
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"http_status": 201, "success": True, "message": "User created", "data": {"user_id": user.id}}

@router.put(
    "/users/{user_id}",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "message": "User updated"}}}},
        404: {"content": {"application/json": {"example": {"detail": "User not found"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def update_user(
    user_id: int,
    request: UserUpdateRequest,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if request.mobile is not None:
        user.mobile = request.mobile
    if request.email is not None:
        user.email = request.email
    if request.password is not None:
        from app.core.security import hash_password
        user.password = hash_password(request.password)
    if request.status is not None:
        user.status = request.status
    db.commit()
    return {"http_status": 200, "success": True, "message": "User updated", "data": {}}

@router.delete(
    "/users/{user_id}",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "message": "User deleted"}}}},
        404: {"content": {"application/json": {"example": {"detail": "User not found"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def delete_user(
    user_id: int,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return {"http_status": 200, "success": True, "message": "User deleted", "data": {}}

@router.get(
    "/markets",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "markets": [{"sr_no": 1, "game": "Market A", "open_time": "09:00:00", "close_time": "21:00:00", "status": 1}], "total": 1}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def list_markets(
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """List all markets"""
    markets = db.query(Game).all()
    
    return {
        "http_status": 200,
        "success": True,
        "message": "Markets fetched",
        "data": {
            "markets": [
            {
                "sr_no": m.sr_no,
                "game": m.game,
                "open_time": str(m.open_time) if m.open_time else None,
                "close_time": str(m.close_time) if m.close_time else None,
                "status": m.status
            }
            for m in markets
            ],
            "total": len(markets)
        }
    }

@router.post(
    "/users/{user_id}/activate",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "message": "User activated"}}}},
        404: {"content": {"application/json": {"example": {"detail": "User not found"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def activate_user(
    user_id: int,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Activate user"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.status = 1
    db.commit()
    
    return {"http_status": 200, "success": True, "message": "User activated", "data": {}}

@router.post(
    "/users/{user_id}/deactivate",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "message": "User deactivated"}}}},
        404: {"content": {"application/json": {"example": {"detail": "User not found"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def deactivate_user(
    user_id: int,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.status = 0
    db.commit()
    
    return {"http_status": 200, "success": True, "message": "User deactivated", "data": {}}

@router.get(
    "/rashi",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "results": [{"sr_no": 1, "rashi_name": "Aries", "result": "Lucky", "result_date": "2025-12-06"}], "total": 1, "limit": 50, "offset": 0}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def admin_get_rashi(
    target_date: Optional[date] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    query = db.query(Rashi)
    if target_date:
        query = query.filter(Rashi.result_date == target_date)
    items = query.order_by(Rashi.result_date.desc()).limit(limit).offset(offset).all()
    total = query.count()
    return {
        "http_status": 200,
        "success": True,
        "message": "Rashi fetched",
        "data": {
            "results": [
            {
                "sr_no": r.sr_no,
                "rashi_name": r.rashi_name,
                "result": r.result,
                "result_date": str(r.result_date)
            }
            for r in items
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

class RashiCreateRequest(BaseModel):
    rashi_name: str
    result: str
    result_date: date

@router.post(
    "/rashi",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"content": {"application/json": {"example": {"status": "success", "id": 1}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def admin_add_rashi(
    request: RashiCreateRequest,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    obj = Rashi(rashi_name=request.rashi_name, result=request.result, result_date=request.result_date, status=0)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"http_status": 201, "success": True, "message": "Rashi created", "data": {"id": obj.sr_no}}

@router.get(
    "/starline",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "results": [{"sr_no": 1, "market_id": 1, "number": "12", "result_date": "2025-12-06"}], "total": 1, "limit": 50, "offset": 0}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def admin_get_starline(
    market_id: Optional[int] = None,
    target_date: Optional[date] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    query = db.query(StarLine)
    if market_id:
        query = query.filter(StarLine.market_id == market_id)
    if target_date:
        query = query.filter(StarLine.result_date == target_date)
    items = query.order_by(StarLine.result_date.desc()).limit(limit).offset(offset).all()
    total = query.count()
    return {
        "http_status": 200,
        "success": True,
        "message": "Starline fetched",
        "data": {
            "results": [
            {
                "sr_no": s.sr_no,
                "market_id": s.market_id,
                "number": s.number,
                "result_date": str(s.result_date)
            }
            for s in items
        ],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }

class PredictionCreateRequest(BaseModel):
    market_id: int
    result: str
    added_date: date
    accuracy: Optional[int] = None

@router.post(
    "/predictions",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"content": {"application/json": {"example": {"status": "success", "id": 1}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def admin_add_prediction(
    request: PredictionCreateRequest,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    obj = FreeFix(
        market_id=request.market_id,
        result=request.result,
        added_date=request.added_date,
        accuracy=request.accuracy,
        status=0
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"http_status": 201, "success": True, "message": "Prediction created", "data": {"id": obj.sr_no}}

@router.post(
    "/sync",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "message": "Sync started"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def admin_sync_results(
    current_user: dict = Depends(get_current_admin)
):
    ResultSyncJob.sync_results()
    return {"http_status": 200, "success": True, "message": "Sync started", "data": {}}

@router.get(
    "/logs",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "logs": [{"sr_no": 1, "user_id": 1, "action": "update", "entity_type": "result", "entity_id": 10, "timestamp": "2025-12-06T12:00:00Z"}], "total": 1, "limit": 50, "offset": 0}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def admin_get_logs(
    user_id: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    query = db.query(AuditLog)
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    logs = query.order_by(AuditLog.timestamp.desc()).limit(limit).offset(offset).all()
    total = query.count()
    return {
        "http_status": 200,
        "success": True,
        "message": "Logs fetched",
        "data": {
            "logs": [
            {
                "sr_no": l.sr_no,
                "user_id": l.user_id,
                "action": l.action,
                "entity_type": l.entity_type,
                "entity_id": l.entity_id,
                "timestamp": l.timestamp.isoformat()
            }
            for l in logs
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    }
