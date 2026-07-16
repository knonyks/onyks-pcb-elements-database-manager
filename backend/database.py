import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

POSTGRES_USER = os.getenv("POSTGRES_USER", "A")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "A")
POSTGRES_DB = os.getenv("POSTGRES_DB", "A")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "A")
DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@database:5432/{POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass