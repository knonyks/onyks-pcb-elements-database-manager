from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from database import Base
from datetime import datetime, timezone
import uuid
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    __table_args__ = {'schema': 'private'}
    id = Column('id', Integer, primary_key=True, index=True)
    name = Column('name', String, unique=True, index=True)
    createdAt = Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

class Supplier(Base):
    __tablename__ = "suppliers"
    __table_args__ = {'schema': 'private'}
    id = Column('id', Integer, primary_key=True, index=True)
    name = Column('name', String, unique=True, index=True)
    createdAt = Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

# class Table(Base):
#     __tablename__ = "tables"
#     __table_args__ = {'schema': 'private'}
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String, unique=True, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
#     elements = relationship("Element", back_populates="table_category")


# class Element(Base):
#     __tablename__ = "elements"
#     __table_args__ = {'schema': 'private'}

#     uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     part_name = Column(String(256), nullable=False)
    
#     table_name = Column(
#         String(256), 
#         ForeignKey("private.tables.name", ondelete="RESTRICT"), 
#         nullable=False
#     )
#     description = Column(String(256), nullable=False)
    
#     manufacturer = Column(
#         String(256), 
#         ForeignKey("private.manufacturers.name", ondelete="SET NULL"), 
#         nullable=True
#     )

#     value = Column(String(256), nullable=True)
#     datashet = Column(Boolean, nullable=True)
#     availability = Column(String(256), nullable=True)
#     suppliers_names = Column(JSONB, default={})
#     library_ref = Column(String(256), nullable=True)
#     library_path = Column(String(256), nullable=True)
#     footprint_ref_1 = Column(String(256), nullable=True)
#     footprint_path_1 = Column(String(256), nullable=True)
#     footprint_ref_2 = Column(String(256), nullable=True)
#     footprint_path_2 = Column(String(256), nullable=True)
#     footprint_ref_3 = Column(String(256), nullable=True)
#     footprint_path_3 = Column(String(256), nullable=True)

#     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

#     table_category = relationship("Table", back_populates="elements")
#     manufacturer_rel = relationship("Manufacturer")


class Element(Base):
    __tablename__ = "elements"
    __table_args__ = {'schema': 'private'}
    uuid = Column('uuid', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    partName = Column("part_name", String(256), nullable=False)
    description = Column('description', String(256), nullable=True, default='Undefined')
    value = Column('value', String(256), nullable=True, default='Undefined')
    availability = Column('availability', String(256), nullable=True, default='Undefined')
    libraryReference = Column('library_ref', String(1024), nullable=True, default='Undefined')
    libraryPath = Column('library_path', String(1024), nullable=True, default='Undefined')
    footprintReferenceNo1 = Column('footprint_reference_1', String(1024), nullable=True, default='Undefined')
    footprintPathNo1 = Column('footprint_path_1', String(1024), nullable=True, default='Undefined')
    footprintReferenceNo2 = Column('footprint_reference_2', String(1024), nullable=True, default='Undefined')
    footprintPathNo2 = Column('footprint_path_2', String(1024), nullable=True, default='Undefined')
    footprintReferenceNo3 = Column('footprint_reference_3', String(1024), nullable=True, default='Undefined')
    footprintPathNo3 = Column('footprint_path_3', String(1024), nullable=True, default='Undefined')
    createdAt = Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)