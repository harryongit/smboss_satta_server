"""Visitor counter model"""
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from app.models.base import BaseModel

class Counter(BaseModel):
    __tablename__ = "tbl_counter"
    
    sr_no = Column(Integer, primary_key=True, unique=True)
    count = Column(Integer, default=0)
    status = Column(Integer, default=1)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    class Config:
        from_attributes = True
