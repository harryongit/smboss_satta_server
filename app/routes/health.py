"""Health check endpoints"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db, check_database_connection

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "http_status": 200,
        "success": True,
        "message": "OK",
        "data": {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "2.0.0"
        }
    }

@router.get("/health/database")
async def db_health_check(db: Session = Depends(get_db)):
    """Database health check"""
    is_connected = check_database_connection()
    return {
        "http_status": 200,
        "success": True,
        "message": "OK",
        "data": {
            "status": "healthy" if is_connected else "unhealthy",
            "database": "connected" if is_connected else "disconnected",
            "timestamp": datetime.utcnow().isoformat()
        }
    }

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "http_status": 200,
        "success": True,
        "message": "OK",
        "data": {
            "message": "SMBOSS API v2.0.0",
            "timestamp": datetime.utcnow().isoformat()
        }
    }
