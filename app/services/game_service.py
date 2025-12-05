"""Game/Market business logic"""
from sqlalchemy.orm import Session
from app.models.game import Game

class GameService:
    @staticmethod
    def get_all_games(db: Session):
        return db.query(Game).filter(Game.status == 1).all()
    
    @staticmethod
    def get_game_by_id(db: Session, game_id: int):
        return db.query(Game).filter(Game.sr_no == game_id).first()
    
    @staticmethod
    def create_game(db: Session, game_name: str, open_time=None, close_time=None):
        game = Game(
            game=game_name,
            open_time=open_time,
            close_time=close_time,
            status=1
        )
        db.add(game)
        db.commit()
        db.refresh(game)
        return game
