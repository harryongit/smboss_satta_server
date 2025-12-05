"""Result business logic"""
from sqlalchemy.orm import Session
from datetime import date
from app.models.result import Result
from app.models.game import Game

class ResultService:
    @staticmethod
    def get_live_results(db: Session, target_date: date = None):
        if not target_date:
            from datetime import datetime
            target_date = datetime.now().date()
        
        return db.query(Result).filter(Result.result_date == target_date).all()
    
    @staticmethod
    def get_market_history(db: Session, market_id: int, limit: int = 30):
        return db.query(Result).filter(
            Result.market_id == market_id
        ).order_by(Result.result_date.desc()).limit(limit).all()
    
    @staticmethod
    def create_result(db: Session, market_id: int, result: str, result_date: date):
        result_obj = Result(
            market_id=market_id,
            result=result,
            result_date=result_date,
            status=0
        )
        db.add(result_obj)
        db.commit()
        db.refresh(result_obj)
        return result_obj
