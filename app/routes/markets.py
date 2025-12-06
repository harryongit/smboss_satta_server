"""Market/Game endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.game import Game
from app.schemas.game import GameCreateRequest
from app.services.result_service import ResultService
from app.services.game_service import GameService

router = APIRouter()

@router.get(
    "",
    response_model=dict,
    responses={
        200: {"content": {"application/json": {"example": [{"sr_no": 1, "game": "Market A", "open_time": "09:00:00", "close_time": "21:00:00", "status": 1, "days": None}]}}},
        500: {"content": {"application/json": {"example": {"detail": "Internal server error"}}}},
    },
)
async def get_all_markets(db: Session = Depends(get_db)):
    """Get all active markets"""
    items = GameService.get_all_games(db)
    return {"http_status": 200, "success": True, "message": "Markets fetched", "data": items}

@router.get(
    "/{market_id}",
    response_model=dict,
    responses={
        200: {"content": {"application/json": {"example": {"sr_no": 1, "game": "Market A", "open_time": "09:00:00", "close_time": "21:00:00", "status": 1, "days": None}}}},
        404: {"content": {"application/json": {"example": {"detail": "Market not found"}}}},
    },
)
async def get_market(market_id: int, db: Session = Depends(get_db)):
    """Get market details"""
    market = GameService.get_game_by_id(db, market_id)
    if not market:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Market not found"
        )
    return {"http_status": 200, "success": True, "message": "Market fetched", "data": market}

@router.get(
    "/{market_id}/results",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "market_id": 1, "market_name": "Market A", "results": [{"result": "123-45-678", "result_date": "2025-12-06", "timestamp": "2025-12-06T12:00:00Z"}], "count": 1}}}},
        404: {"content": {"application/json": {"example": {"detail": "Market not found"}}}},
    },
)
async def get_market_results(
    market_id: int,
    limit: int = 30,
    db: Session = Depends(get_db)
):
    """Get public market results (latest first)"""
    market = GameService.get_game_by_id(db, market_id)
    if not market:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Market not found"
        )
    results = ResultService.get_market_history(db, market_id, limit)
    return {
        "http_status": 200,
        "success": True,
        "message": "Results fetched",
        "data": {
            "market_id": market_id,
            "market_name": market.game,
            "results": [
            {
                "result": r.result,
                "result_date": str(r.result_date),
                "timestamp": r.date.isoformat()
            }
            for r in results
            ],
            "count": len(results)
        }
    }

@router.post(
    "",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"content": {"application/json": {"example": {"status": "success", "message": "Market created successfully", "market_id": 1}}}},
        400: {"content": {"application/json": {"example": {"detail": "Market already exists"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def create_market(
    request: GameCreateRequest,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create new market (admin only)"""
    existing = db.query(Game).filter(Game.game == request.game).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Market already exists"
        )
    
    game = GameService.create_game(
        db,
        request.game,
        request.open_time,
        request.close_time
    )
    
    return {"http_status": 201, "success": True, "message": "Market created", "data": {"market_id": game.sr_no}}

@router.put(
    "/{market_id}",
    response_model=dict,
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "message": "Market updated successfully"}}}},
        404: {"content": {"application/json": {"example": {"detail": "Market not found"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def update_market(
    market_id: int,
    request: GameCreateRequest,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update market (admin only)"""
    market = GameService.get_game_by_id(db, market_id)
    if not market:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Market not found"
        )
    
    market.game = request.game
    market.open_time = request.open_time
    market.close_time = request.close_time
    market.status = request.status
    
    db.commit()
    
    return {"http_status": 200, "success": True, "message": "Market updated", "data": {}}

@router.delete(
    "/{market_id}",
    response_model=dict,
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "message": "Market deleted successfully"}}}},
        404: {"content": {"application/json": {"example": {"detail": "Market not found"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def delete_market(
    market_id: int,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete market (admin only)"""
    market = GameService.get_game_by_id(db, market_id)
    if not market:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Market not found"
        )
    
    db.delete(market)
    db.commit()
    
    return {"http_status": 200, "success": True, "message": "Market deleted", "data": {}}
