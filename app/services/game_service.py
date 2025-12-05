from typing import List, Optional
from datetime import datetime

from app.models.game import Game


_games: List[Game] = [
    Game(id=1, name="Morning Market", market="market-1", status="live", start_time=datetime.utcnow()),
    Game(id=2, name="Evening Market", market="market-2", status="scheduled", start_time=datetime.utcnow()),
]
_id_seq = 3


def _next_id() -> int:
    global _id_seq
    value = _id_seq
    _id_seq += 1
    return value


def list_games() -> List[Game]:
    return list(_games)


def get_game(game_id: int) -> Optional[Game]:
    return next((g for g in _games if g.id == game_id), None)


def add_game(name: str, market: str, start_time: Optional[str], status: str = "scheduled") -> Game:
    dt = datetime.fromisoformat(start_time) if start_time else None
    game = Game(id=_next_id(), name=name, market=market, start_time=dt, status=status)
    _games.append(game)
    return game


def update_game(game_id: int, **updates) -> Optional[Game]:
    game = get_game(game_id)
    if not game:
        return None
    for key, value in updates.items():
        if hasattr(game, key) and value is not None:
            setattr(game, key, value)
    return game

