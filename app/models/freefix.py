"""Free Tips/Predictions model"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel

class FreeFix(BaseModel):
    __tablename__ = "free_fix_results"
    
    sr_no = Column(Integer, primary_key=True, unique=True)
    market_id = Column(Integer, ForeignKey('game.sr_no'), nullable=False, index=True)
    result = Column(String(20), nullable=False)
    added_date = Column(Date, nullable=False, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(Integer, default=0)
    accuracy = Column(Integer, nullable=True)
    
    game = relationship("Game")
    
    __table_args__ = (
        Index('idx_freefix_date', 'added_date'),
        Index('idx_freefix_market', 'market_id'),
    )
    
    class Config:
        from_attributes = True
