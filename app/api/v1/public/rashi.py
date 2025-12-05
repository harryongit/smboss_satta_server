from fastapi import APIRouter

router = APIRouter()


@router.get("/rashi-result")
def rashi_result():
    return {"rashi": "aries", "value": "lucky"}


@router.get("/rashi-single-result")
def rashi_single():
    return {"rashi": "taurus", "value": "stable"}

