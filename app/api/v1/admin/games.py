from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import require_admin
from app.schemas.game import GameConfig, GameUpdate, GameOut
from app.services import game_service


router = APIRouter(prefix="/admin/games")


@router.post("/config", response_model=GameOut)
def create_game(data: GameConfig, _: dict = Depends(require_admin)):
    game = game_service.add_game(data.name, data.market, data.start_time, data.status)
    return GameOut(id=game.id, name=game.name, market=game.market, status=game.status, start_time=data.start_time)


@router.put("/update/{game_id}", response_model=GameOut)
def update_game(game_id: int, data: GameUpdate, _: dict = Depends(require_admin)):
    game = game_service.update_game(game_id, name=data.name, market=data.market, start_time=data.start_time, status=data.status)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    return GameOut(id=game.id, name=game.name, market=game.market, status=game.status, start_time=data.start_time)

