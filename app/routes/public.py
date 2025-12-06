"""Public endpoints (no authentication required)"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.core.database import get_db
from app.models.result import Result
from app.models.game import Game
from app.models.rashi import Rashi
from app.models.offer import Offer

router = APIRouter()

@router.get(
    "/markets",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "markets": [{"sr_no": 1, "game": "Market A", "open_time": "09:00:00", "close_time": "21:00:00"}], "count": 1}}}},
        500: {"content": {"application/json": {"example": {"detail": "Internal server error"}}}},
    },
)
async def get_public_markets(db: Session = Depends(get_db)):
    """Get list of all markets (public)"""
    markets = db.query(Game).filter(Game.status == 1).all()
    
    return {
        "http_status": 200,
        "success": True,
        "message": "Markets retrieved",
        "data": {
            "markets": [
            {
                "sr_no": m.sr_no,
                "game": m.game,
                "open_time": str(m.open_time) if m.open_time else None,
                "close_time": str(m.close_time) if m.close_time else None,
            }
            for m in markets
            ],
            "count": len(markets)
        }
    }

@router.get(
    "/results",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "results": [{"market_id": 1, "result": "123-45-678", "result_date": "2025-12-06"}], "count": 1, "date": "2025-12-06"}}}},
        400: {"content": {"application/json": {"example": {"detail": "Invalid date"}}}},
        500: {"content": {"application/json": {"example": {"detail": "Internal server error"}}}},
    },
)
async def get_public_results(
    target_date: date = Query(None),
    db: Session = Depends(get_db)
):
    """Get public results"""
    if not target_date:
        from datetime import datetime
        target_date = datetime.now().date()
    
    results = db.query(Result).filter(Result.result_date == target_date).all()
    
    return {
        "http_status": 200,
        "success": True,
        "message": "Results retrieved",
        "data": {
            "results": [
            {
                "market_id": r.market_id,
                "result": r.result,
                "result_date": str(r.result_date)
            }
            for r in results
            ],
            "count": len(results),
            "date": str(target_date)
        }
    }

@router.get(
    "/rashi",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "results": [{"rashi_name": "Aries", "result": "Lucky", "result_date": "2025-12-06"}], "count": 1, "date": "2025-12-06"}}}},
        500: {"content": {"application/json": {"example": {"detail": "Internal server error"}}}},
    },
)
async def get_rashi_results(
    target_date: date = Query(None),
    db: Session = Depends(get_db)
):
    """Get Rashi results"""
    if not target_date:
        from datetime import datetime
        target_date = datetime.now().date()
    
    rashi_results = db.query(Rashi).filter(Rashi.result_date == target_date).all()
    
    return {
        "http_status": 200,
        "success": True,
        "message": "Rashi results retrieved",
        "data": {
            "results": [
            {
                "rashi_name": r.rashi_name,
                "result": r.result,
                "result_date": str(r.result_date)
            }
            for r in rashi_results
            ],
            "count": len(rashi_results),
            "date": str(target_date)
        }
    }

@router.get(
    "/offers",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "offers": [{"sr_no": 1, "title": "New Year Offer", "description": "Discounts", "valid_from": "2025-01-01", "valid_till": "2025-01-31"}], "count": 1}}}},
        500: {"content": {"application/json": {"example": {"detail": "Internal server error"}}}},
    },
)
async def get_public_offers(db: Session = Depends(get_db)):
    today = datetime.now().date()
    offers = db.query(Offer).filter(
        Offer.status == 1,
        Offer.valid_from <= today,
        Offer.valid_till >= today
    ).all()
    return {
        "http_status": 200,
        "success": True,
        "message": "Offers retrieved",
        "data": {
            "offers": [
            {
                "sr_no": o.sr_no,
                "title": o.title,
                "description": o.description,
                "valid_from": str(o.valid_from),
                "valid_till": str(o.valid_till)
            }
            for o in offers
            ],
            "count": len(offers)
        }
    }
