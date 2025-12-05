from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.freefix import FreeFix

router = APIRouter()

@router.get("")
async def all_predictions(db: Session = Depends(get_db)):
    items = db.query(FreeFix).order_by(FreeFix.added_date.desc()).all()
    return {
        "status": "success",
        "results": [
            {
                "market_id": r.market_id,
                "result": r.result,
                "added_date": str(r.added_date),
                "accuracy": r.accuracy,
            }
            for r in items
        ],
        "count": len(items),
    }

@router.post("")
async def add_prediction(
    market_id: int,
    result: str,
    added_date: date,
    accuracy: int | None = None,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    obj = FreeFix(market_id=market_id, result=result, added_date=added_date, accuracy=accuracy, status=0)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"status": "success", "id": obj.sr_no}

@router.get("/today")
async def today_predictions(db: Session = Depends(get_db)):
    today = datetime.now().date()
    items = db.query(FreeFix).filter(FreeFix.added_date == today).all()
    return {
        "status": "success",
        "results": [
            {
                "market_id": r.market_id,
                "result": r.result,
                "added_date": str(r.added_date),
                "accuracy": r.accuracy,
            }
            for r in items
        ],
        "count": len(items),
        "date": str(today),
    }

