"""Custom exceptions"""
from fastapi import HTTPException as FastAPIHTTPException
from typing import Optional

class HTTPException(FastAPIHTTPException):
    """HTTP Exception wrapper"""
    pass

class ValidationError(Exception):
    """Validation error"""
    def __init__(self, message: str):
        self.message = message

class DatabaseError(Exception):
    """Database operation error"""
    def __init__(self, message: str):
        self.message = message

class UnauthorizedException(HTTPException):
    """Unauthorized access"""
    def __init__(self, detail: str = "Not authorized"):
        super().__init__(status_code=401, detail=detail)

class ForbiddenException(HTTPException):
    """Forbidden access"""
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(status_code=403, detail=detail)

class NotFoundException(HTTPException):
    """Resource not found"""
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)
