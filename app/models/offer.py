"""Promotions/Offers model"""
from sqlalchemy import Column, Integer, String, DateTime, Date, Text
from datetime import datetime
from app.models.base import BaseModel

class Offer(BaseModel):
    __tablename__ = "tbl_offers"
    
    sr_no = Column(Integer, primary_key=True, unique=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    valid_from = Column(Date, nullable=False)
    valid_till = Column(Date, nullable=False)
    status = Column(Integer, default=1)
    
    class Config:
        from_attributes = True
