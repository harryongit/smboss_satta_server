from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, datetime
from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.rashi import Rashi

router = APIRouter()

@router.get("")
async def all_rashi(db: Session = Depends(get_db)):
    items = db.query(Rashi).order_by(Rashi.result_date.desc()).all()
    return {
        "status": "success",
        "results": [
            {
                "rashi_name": r.rashi_name,
                "result": r.result,
                "result_date": str(r.result_date),
            }
            for r in items
        ],
        "count": len(items),
    }

@router.get("/daily")
async def daily_rashi(db: Session = Depends(get_db)):
    today = datetime.now().date()
    items = db.query(Rashi).filter(Rashi.result_date == today).all()
    return {
        "status": "success",
        "results": [
            {
                "rashi_name": r.rashi_name,
                "result": r.result,
                "result_date": str(r.result_date),
            }
            for r in items
        ],
        "count": len(items),
        "date": str(today),
    }

@router.get("/{rashi_name}")
async def rashi_by_name(rashi_name: str, db: Session = Depends(get_db)):
    items = db.query(Rashi).filter(Rashi.rashi_name == rashi_name).order_by(Rashi.result_date.desc()).all()
    return {
        "status": "success",
        "results": [
            {
                "rashi_name": r.rashi_name,
                "result": r.result,
                "result_date": str(r.result_date),
            }
            for r in items
        ],
        "count": len(items),
    }

@router.post("")
async def add_rashi(
    rashi_name: str,
    result: str,
    result_date: date,
    current_user: dict = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    obj = Rashi(rashi_name=rashi_name, result=result, result_date=result_date, status=0)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"status": "success", "id": obj.sr_no}

