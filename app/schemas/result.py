from typing import Dict, Any

from pydantic import BaseModel


class ResultUpload(BaseModel):
    game_id: int
    payload: Dict[str, Any]


class ResultOut(BaseModel):
    id: int
    game_id: int
    payload: Dict[str, Any]

