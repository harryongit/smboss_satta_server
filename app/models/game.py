from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Game:
    id: int
    name: str
    market: str
    start_time: Optional[datetime] = None
    status: str = "scheduled"

