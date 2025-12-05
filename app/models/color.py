"""Market color/styling model"""
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import BaseModel

class GameColor(BaseModel):
    __tablename__ = "tbl_game_back_color"
    
    sr_no = Column(Integer, primary_key=True, unique=True)
    market_id = Column(Integer, ForeignKey('game.sr_no'), nullable=False, unique=True, index=True)
    color = Column(String(7), nullable=False)
    status = Column(Integer, default=1)
    
    game = relationship("Game")
    
    class Config:
        from_attributes = True
