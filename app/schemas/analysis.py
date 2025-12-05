"""Analysis schemas"""
from pydantic import BaseModel
from typing import List

class JodiFrequencyItem(BaseModel):
    jodi: str
    count: int
    percentage: float

class JodiAnalysisResponse(BaseModel):
    market_id: int
    period_days: int
    total_results: int
    jodi_analysis: List[JodiFrequencyItem]

class PanelFrequencyItem(BaseModel):
    panel: str
    count: int
    percentage: float

class PanelAnalysisResponse(BaseModel):
    market_id: int
    period_days: int
    total_results: int
    panel_analysis: List[PanelFrequencyItem]
