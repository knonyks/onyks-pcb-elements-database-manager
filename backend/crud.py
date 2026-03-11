from sqlalchemy.orm import Session
import models
import schemas
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String
from typing import List, Tuple
import utils

def total_elements(db: Session):
    return -20

def total_tables(db: Session):
    return -21

def total_manufacturers(db: Session):
    return db.query(models.Manufacturer).count()

def total_suppliers(db: Session):
    return db.query(models.Supplier).count()

def last_added_element(db: Session):
    return {
        "uuid": "-123e4567-e89b-12d3-a456-426614174000",
        "part_name": "-Resistor 10kΩ",
        "manufacturer": "Texas Instruments",
        "created_at": "14:30:321, 01.01.1970"
    }

def repository_summary(db: Session):
    return {
        "footprints_total": -200,
        "symbols_total": -150,
        "pcblibs_files_total": -100,
        "schlibs_files_total": -250
    }

def tables_amounts(db: Session):
    return {
        "Inductors": -100,
        "Transistors": -50,
        "Mechanical": -30,
        "Capacitors": -20,
        "ICs": -20,
    }

def manufacturers_amounts(db: Session):
    return {
        "manufacturer1": -100,
        "manufacturer2": -50,
        "manufacturer3": -30,
        "manufacturer4": -20,
        "manufacturer5": -20,
    }

def suppliers_amounts(db: Session):
    return {
        "supplier1": -100,
        "supplier2": -50,
        "supplier3": -30,
        "supplier4": -20,
    }

def get_supplier_by_name(db: Session, name: str):
    return db.query(models.Supplier).filter(models.Supplier.name == name).first()

def create_supplier(db: Session, supplier: schemas.Supplier_Create):
    db_supplier = models.Supplier(name=supplier.name)
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def get_infinite_sorted_suppliers_items(db: Session, cursor_str: str = None, limit: int = 20):
    query = db.query(models.Supplier)

    total_count = None
    if not cursor_str:
        total_count = query.count()

    cursor_data = utils.decode_cursor(cursor_str)

    if cursor_data:
        query = query.filter(models.Supplier.id > cursor_data["id"])

    query = query.order_by(models.Supplier.id.asc())

    items = query.limit(limit + 1).all()

    has_more = len(items) > limit
    if has_more:
        items = items[:-1]

    next_cursor = None
    if items:
        last_item = items[-1]
        next_cursor = utils.encode_cursor({"name" : last_item.name, "id" : last_item.id})

    return items, next_cursor, has_more, total_count

def get_manufacturer_by_name(db: Session, name: str):
    return db.query(models.Manufacturer).filter(models.Manufacturer.name == name).first()

def create_manufacturer(db: Session, manufacturer: schemas.Manufacturer_Create):
    db_manufacturer = models.Manufacturer(name=manufacturer.name)
    db.add(db_manufacturer)
    db.commit()
    db.refresh(db_manufacturer)
    return db_manufacturer

def get_infinite_sorted_manufacturers_items(db: Session, cursor_str: str = None, limit: int = 20):
    query = db.query(models.Manufacturer)

    total_count = None
    if not cursor_str:
        total_count = query.count()

    cursor_data = utils.decode_cursor(cursor_str)

    if cursor_data:
        query = query.filter(models.Manufacturer.id > cursor_data["id"])

    query = query.order_by(models.Manufacturer.id.asc())

    items = query.limit(limit + 1).all()

    has_more = len(items) > limit
    if has_more:
        items = items[:-1]

    next_cursor = None
    if items:
        last_item = items[-1]
        next_cursor = utils.encode_cursor({"name" : last_item.name, "id" : last_item.id})

    return items, next_cursor, has_more, total_count