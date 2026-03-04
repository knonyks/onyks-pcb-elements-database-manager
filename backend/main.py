from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
import schemas
import utils
import crud
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/elements/total", response_model = schemas.Element_Total_Response)
def read_total_elements(db: Session = Depends(get_db)):
    return schemas.Element_Total_Response(total = crud.total_elements(db = db))

@app.get("/tables/total", response_model = schemas.Table_Total_Response)
def read_total_tables(db: Session = Depends(get_db)):
    return schemas.Table_Total_Response(total=crud.total_tables(db = db))

@app.get("/manufacturers/total", response_model = schemas.Manufacturer_Total_Response)
def read_total_manufacturers(db: Session = Depends(get_db)):
    return schemas.Manufacturer_Total_Response(total=crud.total_manufacturers(db = db))

@app.get("/suppliers/total", response_model = schemas.Supplier_Total_Response)
def read_total_suppliers(db: Session = Depends(get_db)):
    return schemas.Supplier_Total_Response(total = crud.total_suppliers(db = db))

@app.get("/elements/last_added", response_model = schemas.Element_Last_Added_Response)
def read_last_added_element(db: Session = Depends(get_db)):
    return schemas.Element_Last_Added_Response(
        uuid = crud.last_added_element(db = db)["uuid"],
        part_name = crud.last_added_element(db = db)["part_name"],
        manufacturer = crud.last_added_element(db = db)["manufacturer"],
        created_at = crud.last_added_element(db = db)['created_at']
    )

@app.get("/repository/summary", response_model = schemas.Repository_Summary_Response)
def read_repository_summary(db: Session = Depends(get_db)):
    return schemas.Repository_Summary_Response(
        footprints_total=crud.repository_summary(db=db)["footprints_total"],
        symbols_total=crud.repository_summary(db=db)["symbols_total"],
        pcblibs_files_total=crud.repository_summary(db=db)["pcblibs_files_total"],
        schlibs_files_total=crud.repository_summary(db=db)["schlibs_files_total"]
    )

@app.get("/tables/amounts", response_model=schemas.Table_Amounts_Response)
def read_tables_amounts(db: Session = Depends(get_db)):
    return schemas.Table_Amounts_Response(tables = crud.tables_amounts(db=db))

@app.get("/manufacturers/amounts", response_model = schemas.Manufacturer_Amounts_Response)
def read_manufacturers_amounts(db: Session = Depends(get_db)):
    return schemas.Manufacturer_Amounts_Response(manufacturers = crud.manufacturers_amounts(db = db))

@app.get("/suppliers/amounts", response_model = schemas.Supplier_Amounts_Response)
def read_suppliers_amounts(db: Session = Depends(get_db)):
    return schemas.Supplier_Amounts_Response(suppliers = crud.suppliers_amounts(db = db))

###############################################################################################

@app.post("/suppliers/create", response_model = schemas.Supplier_Create_Response, status_code = status.HTTP_201_CREATED)
def write_suppliers_create(supplier: schemas.Supplier_Create, db: Session = Depends(get_db)):
    if utils.is_string_valid(supplier.name):
        db_supplier = crud.get_supplier_by_name(db, name = supplier.name)
        if db_supplier:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="The supplier already exists.")    
        return crud.create_supplier(db = db, supplier = supplier)
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Wrong a format of the name.")  

    
@app.get("/suppliers/", response_model=schemas.Supplier_Pagination_Response)
def read_items(params: schemas.Supplier_Pagination = Depends(), db: Session = Depends(get_db)):

    raw_items, total_count = crud.get_suppliers(
        db, 
        cursor=params.cursor, 
        limit=params.limit, 
        search_query=params.search_query, 
        search_columns=params.search_columns
    )

    next_cursor = None
    if len(raw_items) > params.limit:
        items_to_return = raw_items[:-1]
        next_cursor = items_to_return[-1].id
    else:
        items_to_return = raw_items

    return schemas.Supplier_Pagination_Response(
        suppliers=items_to_return,
        next_cursor=next_cursor,
        total_count=total_count
    )












