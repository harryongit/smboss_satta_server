"""Cache warming job"""
from app.core.database import SessionLocal
from app.models.game import Game
from app.models.result import Result
from app.utils.logger import setup_logger
from datetime import datetime, date

logger = setup_logger(__name__)

class CacheWarmer:
    """Background job to warm cache"""
    
    @staticmethod
    def warm_cache():
        """Warm application cache"""
        db = SessionLocal()
        
        try:
            logger.info("Starting cache warming")
            
            # Get all active markets
            markets = db.query(Game).filter(Game.status == 1).all()
            logger.info(f"Cached {len(markets)} markets")
            
            # Get today's results
            today = datetime.now().date()
            results = db.query(Result).filter(Result.result_date == today).all()
            logger.info(f"Cached {len(results)} results for today")
            
            logger.info("Cache warming completed successfully")
            
        except Exception as e:
            logger.error(f"Error in cache warmer job: {str(e)}")
        finally:
            db.close()
