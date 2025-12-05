"""Market/Game endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.game import Game
from app.schemas.game import GameCreateRequest, GameResponse
from app.services.result_service import ResultService
from app.models.result import Result
from app.services.game_service import GameService

router = APIRouter()

@router.get("", response_model=list[GameResponse])
async def get_all_markets(db: Session = Depends(get_db)):
    """Get all active markets"""
    return GameService.get_all_games(db)

@router.get("/{market_id}", response_model=GameResponse)
async def get_market(market_id: int, db: Session = Depends(get_db)):
    """Get market details"""
    market = GameService.get_game_by_id(db, market_id)
    if not market:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Market not found"
        )
    return market

@router.get("/{market_id}/results")
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
        "status": "success",
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

@router.post("", response_model=dict)
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
    
    return {
        "status": "success",
        "message": "Market created successfully",
        "market_id": game.sr_no
    }

@router.put("/{market_id}", response_model=dict)
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
    
    return {"status": "success", "message": "Market updated successfully"}

@router.delete("/{market_id}", response_model=dict)
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
    
    return {"status": "success", "message": "Market deleted successfully"}
