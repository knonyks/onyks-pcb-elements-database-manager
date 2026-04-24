from sqlalchemy import Column, Integer, String
from database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable = False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)