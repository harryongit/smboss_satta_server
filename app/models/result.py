"""Result model - Normalized from game_[market] tables"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import BaseModel

class Result(BaseModel):
    __tablename__ = "game_results"
    
    sr_no = Column(Integer, primary_key=True, unique=True)
    market_id = Column(Integer, ForeignKey('game.sr_no'), nullable=False, index=True)
    result = Column(String(20), nullable=False)
    result_date = Column(Date, nullable=False, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(Integer, default=0)
    
    game = relationship("Game")
    
    __table_args__ = (
        UniqueConstraint('market_id', 'result_date', name='uq_market_date'),
        Index('idx_result_date', 'result_date'),
        Index('idx_market_status', 'market_id', 'status'),
    )
    
    class Config:
        from_attributes = True
