from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any


@dataclass
class Result:
    id: int
    game_id: int
    data: Dict[str, Any]
    created_at: datetime = datetime.utcnow()

