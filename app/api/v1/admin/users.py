from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import require_admin
from app.schemas.user import UserCreate, UserOut
from app.services import user_service


router = APIRouter(prefix="/admin/users")


@router.get("/list", response_model=list[UserOut])
def list_users(_: dict = Depends(require_admin)):
    return [
        UserOut(id=u.id, username=u.username, email=u.email, role=u.role)
        for u in user_service.list_users()
    ]


@router.post("/create", response_model=UserOut)
def create_user(data: UserCreate, _: dict = Depends(require_admin)):
    user = user_service.create_user(data.username, data.email, data.password, role=data.role)
    return UserOut(id=user.id, username=user.username, email=user.email, role=user.role)


@router.delete("/delete/{user_id}")
def delete_user(user_id: int, _: dict = Depends(require_admin)):
    if not user_service.delete_user(user_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"deleted": True}

