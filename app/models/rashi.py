"""Rashi/Astrology model"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Index
from datetime import datetime
from app.models.base import BaseModel

class Rashi(BaseModel):
    __tablename__ = "tbl_rashi"
    
    sr_no = Column(Integer, primary_key=True, unique=True)
    rashi_name = Column(String(50), nullable=False, index=True)
    result = Column(String(20), nullable=False)
    result_date = Column(Date, nullable=False, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(Integer, default=0)
    
    __table_args__ = (
        Index('idx_rashi_date', 'result_date'),
        Index('idx_rashi_name', 'rashi_name'),
    )
    
    class Config:
        from_attributes = True
