"""Result endpoints"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.result import Result
from app.models.game import Game
from app.schemas.result import ResultCreateRequest, ResultResponse
from app.services.result_service import ResultService

router = APIRouter()

@router.get("")
async def get_results_by_date(
    target_date: date = Query(None),
    db: Session = Depends(get_db)
):
    if not target_date:
        from datetime import datetime
        target_date = datetime.now().date()
    results = db.query(Result).filter(Result.result_date == target_date).all()
    return {
        "status": "success",
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

@router.get("/live")
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
            "status": "success",
            "message": [],
            "count": 0,
            "date": str(target_date)
        }
    
    return {
        "status": "success",
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

@router.get("/{market_id}/history")
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
        "status": "success",
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

@router.post("", response_model=dict)
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
    
    return {
        "status": "success",
        "message": "Result created successfully",
        "result_id": result.sr_no
    }

@router.put("/{result_id}", response_model=dict)
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
    
    return {"status": "success", "message": "Result updated successfully"}

@router.delete("/{result_id}", response_model=dict)
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
    
    return {"status": "success", "message": "Result deleted successfully"}
