from sqlalchemy.orm import Session
import models
import schemas

# DASHBOARD
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
        "table1": -100,
        "table2": -50,
        "table3": -30,
        "table4": -20,
    }

def manufacturers_amounts(db: Session):
    return {
        "manufacturer1": -100,
        "manufacturer2": -50,
        "manufacturer3": -30,
        "manufacturer4": -20,
    }

def suppliers_amounts(db: Session):
    return {
        "supplier1": -100,
        "supplier2": -50,
        "supplier3": -30,
        "supplier4": -20,
    }

# def create_supplier(db: Session, supplier: schemas.Supplier_Create):
#     db_supplier = models.Supplier(name=supplier.name)
#     db.add(db_supplier)
#     db.commit()
#     db.refresh(db_supplier)
#     return db_supplier

# def create_manufacturer(db: Session, manufacturer: schemas.Manufacturer_Create):
#     db_manufacturer = models.Manufacturer(name=manufacturer.name)
#     db.add(db_manufacturer)
#     db.commit()
#     db.refresh(db_manufacturer)
#     return db_manufacturer



# def create_supplier(db: Session, supplier: schemas.Supplier_Create):
#     db_supplier = models.Supplier(name=supplier.name)
#     db.add(db_supplier)
#     db.commit()
#     db.refresh(db_supplier)
#     return db_supplier

# def create_manufacturer(db: Session, manufacturer: schemas.Manufacturer_Create):
#     db_manufacturer = models.Manufacturer(name=manufacturer.name)
#     db.add(db_manufacturer)
#     db.commit()
#     db.refresh(db_manufacturer)
#     return db_manufacturer

# def get_suppliers(db: Session, skip: int = 0, limit: int = 100, response_model=schemas.Supplier):
#     temp = db.query(models.Supplier).offset(skip).limit(limit).all()
#     return [response_model.from_orm(supplier) for supplier in temp]


