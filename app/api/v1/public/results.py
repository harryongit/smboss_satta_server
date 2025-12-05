from fastapi import APIRouter

from app.services import result_service


router = APIRouter()


@router.get("/jodi-markets-reports")
def jodi_reports():
    return {"reports": result_service.list_results()}


@router.get("/panel-markets-reports")
def panel_reports():
    return {"reports": result_service.list_results()}


@router.get("/free-fix-results")
def free_fix_results():
    return {"results": result_service.live_results()}

