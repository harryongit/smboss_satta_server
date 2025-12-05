"""User model"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel

class User(BaseModel):
    __tablename__ = "tbl_register"
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    mobile = Column(String(10), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    status = Column(Integer, default=0)
    added_on = Column(Date, default=datetime.now)
    last_login = Column(DateTime, nullable=True)
    login_attempts = Column(Integer, default=0)
    account_locked_until = Column(DateTime, nullable=True)
    
    audit_logs = relationship("AuditLog", back_populates="user")
    
    class Config:
        from_attributes = True
