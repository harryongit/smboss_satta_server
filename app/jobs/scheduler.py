"""Background job scheduler"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.jobs.sync_results import ResultSyncJob
from app.jobs.cache_warmer import CacheWarmer
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Create scheduler
scheduler = BackgroundScheduler()

# Add jobs
def configure_jobs():
    """Configure background jobs"""
    
    # Sync results daily at 9 PM
    scheduler.add_job(
        ResultSyncJob.sync_results,
        CronTrigger(hour=21, minute=0),
        id='sync_results_job',
        name='Sync Results Job',
        replace_existing=True
    )
    
    # Warm cache every hour
    scheduler.add_job(
        CacheWarmer.warm_cache,
        CronTrigger(minute=0),
        id='cache_warmer_job',
        name='Cache Warmer Job',
        replace_existing=True
    )
    
    logger.info("Background jobs configured")

# Configure on import
configure_jobs()
