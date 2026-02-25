from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import schemas
import crud
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# DASHBOARD
@app.get("/elements/total", response_model=schemas.Total_Elements_Response)
def read_total_elements(db: Session = Depends(get_db)):
    return schemas.Total_Elements_Response(total=crud.total_elements(db=db))

@app.get("/tables/total", response_model=schemas.Total_Tables_Response)
def read_total_tables(db: Session = Depends(get_db)):
    return schemas.Total_Tables_Response(total=crud.total_tables(db=db))

@app.get("/manufacturers/total", response_model=schemas.Total_Manufacturers_Response)
def read_total_manufacturers(db: Session = Depends(get_db)):
    return schemas.Total_Manufacturers_Response(total=crud.total_manufacturers(db=db))

@app.get("/suppliers/total", response_model=schemas.Total_Suppliers_Response)
def read_total_suppliers(db: Session = Depends(get_db)):
    return schemas.Total_Suppliers_Response(total=crud.total_suppliers(db=db))

@app.get("/elements/last_added", response_model=schemas.Last_Added_Element_Response)
def read_last_added_element(db: Session = Depends(get_db)):
    return schemas.Last_Added_Element_Response(
        uuid=crud.last_added_element(db=db)["uuid"],
        part_name=crud.last_added_element(db=db)["part_name"]
    )

@app.get("/repository/summary", response_model=schemas.Repository_Summary_Response)
def read_repository_summary(db: Session = Depends(get_db)):
    return schemas.Repository_Summary_Response(
        footprints_total=crud.repository_summary(db=db)["footprints_total"],
        symbols_total=crud.repository_summary(db=db)["symbols_total"],
        pcblibs_files_total=crud.repository_summary(db=db)["pcblibs_files_total"],
        schlibs_files_total=crud.repository_summary(db=db)["schlibs_files_total"]
    )
    
@app.get("/tables/amounts", response_model=schemas.Tables_Amounts_Response)
def read_tables_amounts(db: Session = Depends(get_db)):
    return schemas.Tables_Amounts_Response(tables=crud.tables_amounts(db=db))

@app.get("/manufacturers/amounts", response_model=schemas.Manufacturers_Amounts_Response)
def read_manufacturers_amounts(db: Session = Depends(get_db)):
    return schemas.Manufacturers_Amounts_Response(manufacturers=crud.manufacturers_amounts(db=db))

@app.get("/suppliers/amounts", response_model=schemas.Suppliers_Amounts_Response)
def read_suppliers_amounts(db: Session = Depends(get_db)):
    return schemas.Suppliers_Amounts_Response(suppliers=crud.suppliers_amounts(db=db))




# @app.post("/manufacturers/create")
# def create_manufacturer_endpoint(db: Session = Depends(get_db), manufacturer: schemas.Manufacturer_Create = None):
#     return crud.create_manufacturer(db=db, manufacturer=manufacturer)

# @app.post("/suppliers/create")
# def create_supplier_endpoint(db: Session = Depends(get_db), supplier: schemas.Supplier_Create = None):
#     return crud.create_supplier(db=db, supplier=supplier)

# @app.post("/suppliers/download")
# def get(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
#     return crud.get_suppliers(db=db, skip=skip, limit=limit)

