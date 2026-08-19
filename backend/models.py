from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from database import Base
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    __table_args__ = {'schema': 'private'}

    id:  Mapped[int] = mapped_column(primary_key=True)
    name = Column('name', String, unique=True, index=True, nullable=False)
    createdAt = Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

class Supplier(Base):
    __tablename__ = "suppliers"
    __table_args__ = {'schema': 'private'}

    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column('name', String, unique=True, index=True, nullable=False)
    createdAt = Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

class Table(Base):
    __tablename__ = "tables"
    __table_args__ = {'schema': 'private'}

    id: Mapped[int] = mapped_column(primary_key=True)
    name = Column('name', String, unique=True, nullable=False)
    createdAt = Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    elements = relationship("Element", back_populates="tableCategory")


class Element(Base):
    __tablename__ = "elements"
    __table_args__ = {'schema': 'private'}

    uuid = Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    partName = Column("part_name", String(256), nullable=False)

    manufacturer = Column(
        String(256), 
        ForeignKey("private.manufacturers.name", ondelete="SET NULL", onupdate="CASCADE"), 
        nullable=True
    )

    table = Column('table',
        String(256), 
        ForeignKey("private.tables.name", ondelete="CASCADE", onupdate="CASCADE"), 
        nullable=False
    )

    description = Column('description', String(256), nullable=True, default='')
    value = Column('value', String(256), nullable=True, default='')
    availability = Column('availability', String(256), nullable=True, default='')
    datasheet = Column(Boolean, nullable=False, default=False)
    
    libraryReference = Column('library_ref', String(1024), nullable=True, default='')
    libraryPath = Column('library_path', String(1024), nullable=True, default='')
    
    footprintReferenceNo1 = Column('footprint_reference_1', String(1024), nullable=True, default='')
    footprintPathNo1 = Column('footprint_path_1', String(1024), nullable=True, default='')
    
    footprintReferenceNo2 = Column('footprint_reference_2', String(1024), nullable=True, default='')
    footprintPathNo2 = Column('footprint_path_2', String(1024), nullable=True, default='')
    
    footprintReferenceNo3 = Column('footprint_reference_3', String(1024), nullable=True, default='')
    footprintPathNo3 = Column('footprint_path_3', String(1024), nullable=True, default='')
    
    suppliers = Column('suppliers', JSONB, default={})

    createdAt = Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    tableCategory = relationship("Table", back_populates="elements")
    manufacturerRel = relationship("Manufacturer")