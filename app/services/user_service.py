from typing import List, Optional

from app.core.security import create_access_token, get_password_hash, verify_password
from app.models.user import User


_users: List[User] = []
_id_seq = 1


def _next_id() -> int:
    global _id_seq
    value = _id_seq
    _id_seq += 1
    return value


def create_user(username: str, email: str, password: str, role: str = "user") -> User:
    user = User(id=_next_id(), username=username, email=email, hashed_password=get_password_hash(password), role=role)
    _users.append(user)
    return user


def authenticate(username: str, password: str) -> Optional[str]:
    user = next((u for u in _users if u.username == username), None)
    if user and verify_password(password, user.hashed_password):
        return create_access_token({"sub": user.username, "role": user.role})
    return None


def list_users() -> List[User]:
    return list(_users)


def delete_user(user_id: int) -> bool:
    global _users
    before = len(_users)
    _users = [u for u in _users if u.id != user_id]
    return len(_users) < before

