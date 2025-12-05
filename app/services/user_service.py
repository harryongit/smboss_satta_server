"""User business logic"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password, verify_password

class UserService:
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def create_user(db: Session, username: str, mobile: str, email: str, password: str):
        user = User(
            username=username,
            mobile=mobile,
            email=email,
            password=hash_password(password),
            status=0
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
