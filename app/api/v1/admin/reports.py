from fastapi import APIRouter, Depends

from app.core.dependencies import require_admin


router = APIRouter(prefix="/admin/reports")


@router.post("/generate")
def generate_report(_: dict = Depends(require_admin)):
    return {"report": "generated"}

