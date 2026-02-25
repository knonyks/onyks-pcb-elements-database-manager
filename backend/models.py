from sqlalchemy import Column, Integer, String
from database import Base

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(String, index=True)

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(String, index=True)