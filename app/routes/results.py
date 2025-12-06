"""Result endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.result import Result
from app.models.game import Game
from app.schemas.result import ResultCreateRequest
from app.services.result_service import ResultService

router = APIRouter()

@router.get(
    "",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "message": [{"market_id": 1, "result": "123-45-678", "result_date": "2025-12-06"}], "count": 1, "date": "2025-12-06"}}}},
        400: {"content": {"application/json": {"example": {"detail": "Invalid date"}}}},
    },
)
async def get_results_by_date(
    target_date: date = Query(None),
    db: Session = Depends(get_db)
):
    if not target_date:
        from datetime import datetime
        target_date = datetime.now().date()
    results = db.query(Result).filter(Result.result_date == target_date).all()
    return {
        "http_status": 200,
        "success": True,
        "message": "Results fetched",
        "data": {
            "message": [
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
    "/live",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "message": [{"market_id": 1, "result": "123-45-678", "result_date": "2025-12-06", "timestamp": "2025-12-06T12:00:00Z"}], "count": 1, "date": "2025-12-06"}}}},
    },
)
async def get_live_results(
    target_date: date = Query(None),
    db: Session = Depends(get_db)
):
    """Get live results for all markets"""
    if not target_date:
        from datetime import datetime
        target_date = datetime.now().date()
    
    results = ResultService.get_live_results(db, target_date)
    
    if not results:
        return {
            "http_status": 200,
            "success": True,
            "message": "Live results fetched",
            "data": {"message": [], "count": 0, "date": str(target_date)}
        }
    
    return {
        "http_status": 200,
        "success": True,
        "message": "Live results fetched",
        "data": {
            "message": [
            {
                "market_id": r.market_id,
                "result": r.result,
                "result_date": str(r.result_date),
                "timestamp": r.date.isoformat()
            }
            for r in results
            ],
            "count": len(results),
            "date": str(target_date)
        }
    }

@router.get(
    "/{market_id}/history",
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "market_id": 1, "market_name": "Market A", "message": [{"result": "123-45-678", "result_date": "2025-12-06", "timestamp": "2025-12-06T12:00:00Z"}], "count": 1}}}},
        404: {"content": {"application/json": {"example": {"detail": "Market not found"}}}},
    },
)
async def get_market_history(
    market_id: int,
    limit: int = Query(30, le=100),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """Get historical results for a market"""
    # Verify market exists
    market = db.query(Game).filter(Game.sr_no == market_id).first()
    if not market:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Market not found"
        )
    
    # Get results
    results = ResultService.get_market_history(db, market_id, limit)
    
    return {
        "http_status": 200,
        "success": True,
        "message": "Market history fetched",
        "data": {
            "market_id": market_id,
            "market_name": market.game,
            "message": [
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
        201: {"content": {"application/json": {"example": {"status": "success", "message": "Result created successfully", "result_id": 1}}}},
        404: {"content": {"application/json": {"example": {"detail": "Market not found"}}}},
        400: {"content": {"application/json": {"example": {"detail": "Result already exists for this date"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def create_result(
    request: ResultCreateRequest,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Create new result (admin only)"""
    # Verify market exists
    market = db.query(Game).filter(Game.sr_no == request.market_id).first()
    if not market:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Market not found"
        )
    
    # Check if result already exists
    existing = db.query(Result).filter(
        Result.market_id == request.market_id,
        Result.result_date == request.result_date
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Result already exists for this date"
        )
    
    # Create result
    result = ResultService.create_result(
        db,
        request.market_id,
        request.result,
        request.result_date
    )
    
    return {"http_status": 201, "success": True, "message": "Result created", "data": {"result_id": result.sr_no}}

@router.put(
    "/{result_id}",
    response_model=dict,
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "message": "Result updated successfully"}}}},
        404: {"content": {"application/json": {"example": {"detail": "Result not found"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def update_result(
    result_id: int,
    request: ResultCreateRequest,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Update result (admin only)"""
    result = db.query(Result).filter(Result.sr_no == result_id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )
    
    result.result = request.result
    db.commit()
    
    return {"http_status": 200, "success": True, "message": "Result updated", "data": {}}

@router.delete(
    "/{result_id}",
    response_model=dict,
    responses={
        200: {"content": {"application/json": {"example": {"status": "success", "message": "Result deleted successfully"}}}},
        404: {"content": {"application/json": {"example": {"detail": "Result not found"}}}},
        403: {"content": {"application/json": {"example": {"detail": "Admin privileges required"}}}},
    },
)
async def delete_result(
    result_id: int,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Delete result (admin only)"""
    result = db.query(Result).filter(Result.sr_no == result_id).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )
    
    db.delete(result)
    db.commit()
    
    return {"http_status": 200, "success": True, "message": "Result deleted", "data": {}}
