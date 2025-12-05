from fastapi import APIRouter


router = APIRouter()


@router.get("/star-line-result")
def star_line_result():
    return {"star_line": "result-feed"}


@router.get("/star-line-single-result")
def star_line_single():
    return {"star_line": "single", "value": "42"}

