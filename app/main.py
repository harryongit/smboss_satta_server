"""FastAPI main application"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime

# Import all routes
from app.routes import health, auth, markets, results, admin, public
from app.core.database import engine, Base, get_db
from app.core.exceptions import HTTPException, ValidationError, DatabaseError
from app.core.config import settings
from app.utils.logger import setup_logger
from app.jobs.scheduler import scheduler

# Setup logging
logger = setup_logger(__name__)

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting SMBOSS FastAPI Application")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    # Start background scheduler
    scheduler.start()
    logger.info("Background jobs scheduler started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SMBOSS Application")
    scheduler.shutdown()
    logger.info("Background jobs scheduler stopped")

# Create FastAPI app
app = FastAPI(
    title="SMBOSS API",
    description="Satta Matka Result Tracking System",
    version="2.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "yourdomain.com"]
)

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "http_status": exc.status_code,
            "success": False,
            "message": str(exc.detail),
            "data": {"error": str(exc.detail)}
        }
    )

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "http_status": 400,
            "success": False,
            "message": "Validation error",
            "data": {"error": str(exc.message)}
        }
    )

@app.exception_handler(DatabaseError)
async def database_error_handler(request: Request, exc: DatabaseError):
    logger.error(f"Database error: {exc.message}")
    return JSONResponse(
        status_code=500,
        content={
            "http_status": 500,
            "success": False,
            "message": "Database operation failed",
            "data": {"error": "Database operation failed"}
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "http_status": 500,
            "success": False,
            "message": "Internal server error",
            "data": {"error": "Internal server error"}
        }
    )

# Include all routes
app.include_router(health.router)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(markets.router, prefix="/markets", tags=["Markets"])
app.include_router(results.router, prefix="/results", tags=["Results"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(public.router, prefix="/public", tags=["Public"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
