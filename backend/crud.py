# from sqlalchemy.orm import Session
# import models
# import schemas
# from sqlalchemy.orm import Session
# from sqlalchemy import or_, cast, String
# from typing import List, Tuple
# import utils

# ### MANUFACTURER ###
# def manufacturer_total(db: Session):
#     return db.query(models.Manufacturer).count()

# def manufacturer_get_by_name(db: Session, name: str):
#     return db.query(models.Manufacturer).filter(models.Manufacturer.name == name).first()

# def manufacturer_create(db: Session, manufacturer: schemas.ManufacturerCreate):
#     db_manufacturer = models.Manufacturer(name=manufacturer.name)
#     db.add(db_manufacturer)
#     db.commit()
#     db.refresh(db_manufacturer)
#     return db_manufacturer.name

# def manufacturer_list(db: Session, skip: int = 0, limit: int = 20):
#     return db.query(models.Manufacturer).offset(skip).limit(limit).all()

# ### SUPPLIER ###
# def supplier_total(db: Session):
#     return db.query(models.Supplier).count()

# def supplier_get_by_name(db: Session, name: str):
#     return db.query(models.Supplier).filter(models.Supplier.name == name).first()

# def supplier_create(db: Session, supplier: schemas.SupplierCreate):
#     db_supplier = models.Supplier(name=supplier.name)
#     db.add(db_supplier)
#     db.commit()
#     db.refresh(db_supplier)
#     return db_supplier

# def supplier_list(db: Session, skip: int = 0, limit: int = 20):
#     return db.query(models.Supplier).offset(skip).limit(limit).all()