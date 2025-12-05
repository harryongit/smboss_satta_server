from dataclasses import dataclass
from datetime import datetime


@dataclass
class Admin:
    id: int
    username: str
    email: str
    hashed_password: str
    role: str = "admin"
    created_at: datetime = datetime.utcnow()

