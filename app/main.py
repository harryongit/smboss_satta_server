# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMBOSS API",
    description="Satta Matka Result Management System",
    version="1.0.0"
)

# CORS Configuration (Allow all for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Public APIs (No auth needed)
from app.api.v1.public import markets, results, rashi, starline, special
app.include_router(markets.router, prefix="/api", tags=["public-markets"])
app.include_router(results.router, prefix="/api", tags=["public-results"])
app.include_router(rashi.router, prefix="/api", tags=["public-rashi"])
app.include_router(starline.router, prefix="/api", tags=["public-starline"])
app.include_router(special.router, prefix="/api", tags=["public-special"])

# Include Admin APIs (Auth required)
from app.api.v1.admin import auth as admin_auth, users, results as admin_results
from app.api.v1.admin import games, reports, dashboard
app.include_router(admin_auth.router, prefix="/admin/auth", tags=["admin-auth"])
app.include_router(users.router, prefix="/admin/users", tags=["admin-users"])
app.include_router(admin_results.router, prefix="/admin/results", tags=["admin-results"])
app.include_router(games.router, prefix="/admin/games", tags=["admin-games"])
app.include_router(reports.router, prefix="/admin/reports", tags=["admin-reports"])
app.include_router(dashboard.router, prefix="/admin/dashboard", tags=["admin-dashboard"])

# Include User APIs (Auth required)
from app.api.v1.user import auth as user_auth, results as user_results
from app.api.v1.user import games as user_games, dashboard as user_dashboard
app.include_router(user_auth.router, prefix="/user/auth", tags=["user-auth"])
app.include_router(user_results.router, prefix="/user/results", tags=["user-results"])
app.include_router(user_games.router, prefix="/user/games", tags=["user-games"])
app.include_router(user_dashboard.router, prefix="/user/dashboard", tags=["user-dashboard"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Run: uvicorn app.main:app --reload
