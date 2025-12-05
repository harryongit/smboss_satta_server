"""Game/Market model"""
from sqlalchemy import Column, Integer, String, Time, Boolean, Index
from app.models.base import BaseModel

class Game(BaseModel):
    __tablename__ = "game"
    
    sr_no = Column(Integer, primary_key=True, unique=True)
    game = Column(String(100), unique=True, nullable=False, index=True)
    open_time = Column(Time, nullable=True)
    close_time = Column(Time, nullable=True)
    status = Column(Integer, default=1, index=True)
    days = Column(Integer)
    
    __table_args__ = (
        Index('idx_game_status', 'status'),
        Index('idx_game_name', 'game'),
    )
    
    class Config:
        from_attributes = True
