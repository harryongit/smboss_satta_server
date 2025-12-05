from fastapi import APIRouter, Depends

from app.core.dependencies import require_user
from app.services import game_service, result_service


router = APIRouter(prefix="/user/dashboard")


@router.get("/stats")
def stats(_: dict = Depends(require_user)):
    return {
        "assigned_games": len(game_service.list_games()),
        "uploads": len(result_service.list_results()),
    }

