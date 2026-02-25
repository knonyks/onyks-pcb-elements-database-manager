import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

POSTGRES_USER = os.getenv("POSTGRES_USER", "A")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "A")
POSTGRES_DB = os.getenv("POSTGRES_DB", "A")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "A")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@database:5432/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()