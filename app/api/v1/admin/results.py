from fastapi import APIRouter, Depends

from app.core.dependencies import require_admin
from app.schemas.result import ResultUpload, ResultOut
from app.services import result_service


router = APIRouter(prefix="/admin/results")


@router.post("/upload", response_model=ResultOut)
def upload_result(data: ResultUpload, _: dict = Depends(require_admin)):
    result = result_service.upload_result(data.game_id, data.payload)
    return ResultOut(id=result.id, game_id=result.game_id, payload=result.data)


@router.get("/list", response_model=list[ResultOut])
def list_results(_: dict = Depends(require_admin)):
    return [ResultOut(id=r.id, game_id=r.game_id, payload=r.data) for r in result_service.list_results()]

