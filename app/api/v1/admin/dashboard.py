from fastapi import APIRouter, Depends

from app.core.dependencies import require_admin
from app.services import admin_service


router = APIRouter(prefix="/admin/dashboard")


@router.get("/stats")
def stats(_: dict = Depends(require_admin)):
    return admin_service.dashboard_stats()

