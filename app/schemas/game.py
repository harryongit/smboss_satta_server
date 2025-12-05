from typing import Optional

from pydantic import BaseModel


class GameConfig(BaseModel):
    name: str
    market: str
    start_time: Optional[str] = None
    status: str = "scheduled"


class GameUpdate(GameConfig):
    pass


class GameOut(BaseModel):
    id: int
    name: str
    market: str
    status: str
    start_time: Optional[str] = None

