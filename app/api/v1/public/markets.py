from fastapi import APIRouter

from app.services import game_service, result_service


router = APIRouter()


@router.get("/markets")
def list_markets():
    return {"markets": [g.market for g in game_service.list_games()]}


@router.get("/market-list")
def market_list():
    return {"games": [vars(g) for g in game_service.list_games()]}


@router.get("/live-results")
def live_results():
    return {"live": result_service.live_results()}

