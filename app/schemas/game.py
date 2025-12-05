"""Game/Market schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import time

class GameCreateRequest(BaseModel):
    game: str = Field(..., min_length=1, max_length=100)
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    status: int = 1
    days: Optional[int] = None

class GameResponse(BaseModel):
    sr_no: int
    game: str
    open_time: Optional[time]
    close_time: Optional[time]
    status: int
    days: Optional[int]
    
    class Config:
        from_attributes = True
