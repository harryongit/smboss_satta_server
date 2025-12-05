from fastapi import APIRouter

from app.api.v1.public import markets, results, rashi, starline, special
from app.api.v1.admin import auth as admin_auth, users as admin_users, results as admin_results, games as admin_games, reports as admin_reports, dashboard as admin_dashboard
from app.api.v1.user import auth as user_auth, results as user_results, games as user_games, dashboard as user_dashboard


api_router = APIRouter(prefix="/api")

# Public endpoints
api_router.include_router(markets.router, tags=["markets"])
api_router.include_router(results.router, tags=["results"])
api_router.include_router(rashi.router, tags=["rashi"])
api_router.include_router(starline.router, tags=["starline"])
api_router.include_router(special.router, tags=["special"])

# Admin endpoints
api_router.include_router(admin_auth.router, tags=["admin-auth"])
api_router.include_router(admin_users.router, tags=["admin-users"])
api_router.include_router(admin_results.router, tags=["admin-results"])
api_router.include_router(admin_games.router, tags=["admin-games"])
api_router.include_router(admin_reports.router, tags=["admin-reports"])
api_router.include_router(admin_dashboard.router, tags=["admin-dashboard"])

# User endpoints
api_router.include_router(user_auth.router, tags=["user-auth"])
api_router.include_router(user_results.router, tags=["user-results"])
api_router.include_router(user_games.router, tags=["user-games"])
api_router.include_router(user_dashboard.router, tags=["user-dashboard"])

