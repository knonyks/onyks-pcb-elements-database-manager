from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from database import Base
from datetime import datetime
import uuid
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    __table_args__ = {'schema': 'private'}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Supplier(Base):
    __tablename__ = "suppliers"
    __table_args__ = {'schema': 'private'}
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable = False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Table(Base):
    __tablename__ = "tables"
    __table_args__ = {'schema': 'private'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    elements = relationship("Element", back_populates="table_category")


class Element(Base):
    __tablename__ = "elements"
    __table_args__ = {'schema': 'private'}

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    part_name = Column(String(256), nullable=False)
    
    table_name = Column(
        String(256), 
        ForeignKey("private.tables.name", ondelete="RESTRICT"), 
        nullable=False
    )
    description = Column(String(256), nullable=False)
    
    manufacturer = Column(
        String(256), 
        ForeignKey("private.manufacturers.name", ondelete="SET NULL"), 
        nullable=True
    )

    value = Column(String(256), nullable=True)
    datashet = Column(Boolean, nullable=True)
    availability = Column(String(256), nullable=True)
    suppliers_names = Column(JSONB, default={})
    library_ref = Column(String(256), nullable=True)
    library_path = Column(String(256), nullable=True)
    footprint_ref_1 = Column(String(256), nullable=True)
    footprint_path_1 = Column(String(256), nullable=True)
    footprint_ref_2 = Column(String(256), nullable=True)
    footprint_path_2 = Column(String(256), nullable=True)
    footprint_ref_3 = Column(String(256), nullable=True)
    footprint_path_3 = Column(String(256), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    table_category = relationship("Table", back_populates="elements")
    manufacturer_rel = relationship("Manufacturer")