from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from collections import Counter
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.starline import StarLine
from app.models.game import Game

router = APIRouter()

@router.get("")
async def all_starline(db: Session = Depends(get_db)):
    items = db.query(StarLine).order_by(StarLine.result_date.desc()).all()
    return {
        "status": "success",
        "results": [
            {
                "market_id": r.market_id,
                "number": r.number,
                "result_date": str(r.result_date),
            }
            for r in items
        ],
        "count": len(items),
    }

@router.get("/{market_id}")
async def market_starline(market_id: int, db: Session = Depends(get_db)):
    items = db.query(StarLine).filter(StarLine.market_id == market_id).order_by(StarLine.result_date.desc()).all()
    return {
        "status": "success",
        "results": [
            {
                "market_id": r.market_id,
                "number": r.number,
                "result_date": str(r.result_date),
            }
            for r in items
        ],
        "count": len(items),
    }

@router.post("")
async def add_starline(
    market_id: int,
    number: str,
    result_date: date,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    market = db.query(Game).filter(Game.sr_no == market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")
    obj = StarLine(market_id=market_id, number=number, result_date=result_date, status=0)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"status": "success", "id": obj.sr_no}

@router.get("/trends")
async def starline_trends(
    period_days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    start_date = datetime.now().date() - timedelta(days=period_days)
    items = db.query(StarLine).filter(StarLine.result_date >= start_date).all()
    by_day = Counter([r.result_date for r in items])
    return {
        "status": "success",
        "days": [
            {"date": str(d), "count": c}
            for d, c in sorted(by_day.items())
        ],
        "total": len(items),
    }
