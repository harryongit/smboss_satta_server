"""Database connection and session management"""
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os
from app.core.config import settings
from app.models import Base

# Database URL
if settings.DATABASE_TYPE == "mysql":
    DATABASE_URL = (
        f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
else:
    raise ValueError(f"Unsupported database type: {settings.DATABASE_TYPE}")

# Create engine
engine = create_engine(
    DATABASE_URL,
    echo=settings.SQL_ECHO,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Database dependency
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check
def check_database_connection() -> bool:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

# Get table names
def get_table_names() -> list:
    inspector = inspect(engine)
    return inspector.get_table_names()

# Initialize database
def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
