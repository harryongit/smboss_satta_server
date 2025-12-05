from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from collections import Counter
from app.core.database import get_db
from app.models.result import Result
from app.models.game import Game
from app.schemas.analysis import (
    JodiFrequencyItem,
    JodiAnalysisResponse,
    PanelFrequencyItem,
    PanelAnalysisResponse,
)

router = APIRouter()

@router.get("/jodi/{market_id}", response_model=JodiAnalysisResponse)
async def jodi_frequency(
    market_id: int,
    period_days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    market = db.query(Game).filter(Game.sr_no == market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")
    start_date = datetime.now().date() - timedelta(days=period_days)
    rows = db.query(Result).filter(
        Result.market_id == market_id,
        Result.result_date >= start_date,
    ).all()
    jodis = []
    for r in rows:
        parts = (r.result or "").split("-")
        if len(parts) >= 2:
            jodis.append(parts[1])
    total = len(jodis)
    counts = Counter(jodis)
    items = [
        JodiFrequencyItem(jodi=k, count=v, percentage=(v / total * 100 if total else 0.0))
        for k, v in counts.most_common()
    ]
    return JodiAnalysisResponse(
        market_id=market_id,
        period_days=period_days,
        total_results=total,
        jodi_analysis=items,
    )

@router.get("/panel/{market_id}", response_model=PanelAnalysisResponse)
async def panel_frequency(
    market_id: int,
    period_days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    market = db.query(Game).filter(Game.sr_no == market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")
    start_date = datetime.now().date() - timedelta(days=period_days)
    rows = db.query(Result).filter(
        Result.market_id == market_id,
        Result.result_date >= start_date,
    ).all()
    panels = []
    for r in rows:
        parts = (r.result or "").split("-")
        if len(parts) >= 1 and len(parts[0]) == 3:
            panels.append(parts[0])
        if len(parts) >= 3 and len(parts[2]) == 3:
            panels.append(parts[2])
    total = len(panels)
    counts = Counter(panels)
    items = [
        PanelFrequencyItem(panel=k, count=v, percentage=(v / total * 100 if total else 0.0))
        for k, v in counts.most_common()
    ]
    return PanelAnalysisResponse(
        market_id=market_id,
        period_days=period_days,
        total_results=total,
        panel_analysis=items,
    )

@router.get("/trends/{market_id}")
async def market_trends(
    market_id: int,
    period_days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    market = db.query(Game).filter(Game.sr_no == market_id).first()
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")
    start_date = datetime.now().date() - timedelta(days=period_days)
    rows = db.query(Result).filter(
        Result.market_id == market_id,
        Result.result_date >= start_date,
    ).all()
    by_day = Counter([r.result_date for r in rows])
    return {
        "status": "success",
        "market_id": market_id,
        "period_days": period_days,
        "days": [
            {"date": str(d), "count": c}
            for d, c in sorted(by_day.items())
        ],
        "total": len(rows),
    }

@router.get("/comparison")
async def compare_markets(
    period_days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    start_date = datetime.now().date() - timedelta(days=period_days)
    markets = db.query(Game).filter(Game.status == 1).all()
    out = []
    for m in markets:
        cnt = db.query(Result).filter(
            Result.market_id == m.sr_no,
            Result.result_date >= start_date,
        ).count()
        out.append({"market_id": m.sr_no, "market_name": m.game, "count": cnt})
    out.sort(key=lambda x: x["count"], reverse=True)
    return {
        "status": "success",
        "period_days": period_days,
        "markets": out,
    }

