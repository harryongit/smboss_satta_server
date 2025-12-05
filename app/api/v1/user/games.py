from fastapi import APIRouter, Depends

from app.core.dependencies import require_user
from app.schemas.game import GameOut
from app.services import game_service


router = APIRouter(prefix="/user/games")


@router.get("/assigned", response_model=list[GameOut])
def assigned_games(_: dict = Depends(require_user)):
    return [
        GameOut(id=g.id, name=g.name, market=g.market, status=g.status, start_time=g.start_time.isoformat() if g.start_time else None)
        for g in game_service.list_games()
    ]


@router.get("/history", response_model=list[GameOut])
def game_history(_: dict = Depends(require_user)):
    return assigned_games()

