"""Star Line model"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel

class StarLine(BaseModel):
    __tablename__ = "tbl_star_line"
    
    sr_no = Column(Integer, primary_key=True, unique=True)
    market_id = Column(Integer, ForeignKey('game.sr_no'), nullable=False, index=True)
    number = Column(String(5), nullable=False)
    result_date = Column(Date, nullable=False, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(Integer, default=0)
    
    game = relationship("Game")
    
    __table_args__ = (
        Index('idx_starline_date', 'result_date'),
        Index('idx_starline_market', 'market_id'),
    )
    
    class Config:
        from_attributes = True
