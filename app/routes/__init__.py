"""Routes package"""
from app.routes import (
    health,
    auth,
    markets,
    results,
    public,
    admin,
)

__all__ = ["health", "auth", "markets", "results", "public", "admin"]
