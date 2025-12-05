from fastapi import APIRouter


router = APIRouter()


@router.get("/offers")
def offers():
    return {"offers": ["welcome bonus", "daily special"]}

