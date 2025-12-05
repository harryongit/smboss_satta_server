"""Result schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class ResultCreateRequest(BaseModel):
    market_id: int
    result: str = Field(..., min_length=1, max_length=20)
    result_date: date

class ResultResponse(BaseModel):
    sr_no: int
    market_id: int
    result: str
    result_date: date
    status: int
    date: datetime
    
    class Config:
        from_attributes = True
