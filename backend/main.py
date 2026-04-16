from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
import models
import schemas
import utils
import crud
from database import engine, SessionLocal
from typing import List
import os

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

### COMPLETE
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/repository/name')
def get_repository_name():
    return {"name":  os.getenv("SVN_REPO_NAME")}

@app.get("/repository/list", response_model=List[schemas.SVNItem])
async def get_svn_list(path: str = Query("")):
    if path.lower().endswith(('.schlib', '.pcblib')):
        try:
            return [schemas.SVNItem(name=i["name"], type=i["type"]) for i in utils.svn_get_altium_content("file:///local_svn", path, os.getenv("SVN_SERVER_USER"), os.getenv("SVN_SERVER_PASSWORD"))]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            return [schemas.SVNItem(name=i["name"], type=i["type"]) for i in utils.svn_get_folder_list("file:///local_svn", path, os.getenv("SVN_SERVER_USER"), os.getenv("SVN_SERVER_PASSWORD"))]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/manufacturers/total", response_model = schemas.ManufacturerTotalResponse)
def read_total_manufacturers(db: Session = Depends(get_db)):
    return schemas.ManufacturerTotalResponse(total=crud.total_manufacturers(db = db))

@app.get("/suppliers/total", response_model = schemas.SupplierTotalResponse)
def read_total_suppliers(db: Session = Depends(get_db)):
    return schemas.SupplierTotalResponse(total = crud.total_suppliers(db = db))












@app.post("/manufacturers/create", response_model = schemas.Manufacturer_Infinite_Scroll_Response, status_code = status.HTTP_201_CREATED)
def write_manufacturers_create(manufacturer: schemas.ManufacturerCreate, db: Session = Depends(get_db)):
    if utils.is_manufacturer_name_valid(manufacturer.name):
        db_manufacturer = crud.get_manufacturer_by_name(db, name = manufacturer.name)
        if db_manufacturer:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="The manufacturer already exists.")    
        return crud.create_manufacturer(db = db, manufacturer = manufacturer)
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Wrong a format of the name.")  



@app.post("/suppliers/create", response_model = schemas.Supplier_Create_Response, status_code = status.HTTP_201_CREATED)
def write_suppliers_create(supplier: schemas.Supplier_Create, db: Session = Depends(get_db)):
    if utils.is_supplier_name_valid(supplier.name):
        db_supplier = crud.get_supplier_by_name(db, name = supplier.name)
        if db_supplier:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="The supplier already exists.")    
        return crud.create_supplier(db = db, supplier = supplier)
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Wrong a format of the name.")  





@app.get("/manufacturers/", response_model=schemas.Infinite_Scroll_Response[schemas.Manufacturer_Infinite_Scroll_Response])
def read_manufacturers(params: schemas.Infinite_Scroll = Depends(), db: Session = Depends(get_db)):
    items, next_cursor, has_more, total_count = crud.get_infinite_sorted_manufacturers_items(
        db=db, 
        cursor_str=params.cursor, 
        limit=params.limit
    )
    return {
        "items": items,
        "next_cursor": next_cursor,
        "has_more": has_more,
        "total": total_count
    }


### UNFINISHED



@app.get("/elements/total", response_model = schemas.Element_Total_Response)
def read_total_elements(db: Session = Depends(get_db)):
    return schemas.Element_Total_Response(total = crud.total_elements(db = db))

@app.get("/tables/total", response_model = schemas.Table_Total_Response)
def read_total_tables(db: Session = Depends(get_db)):
    return schemas.Table_Total_Response(total=crud.total_tables(db = db))



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


@app.get("/suppliers/", response_model=schemas.Infinite_Scroll_Response[schemas.Supplier_Infinite_Scroll_Response])
def read_suppliers(params: schemas.Infinite_Scroll = Depends(), db: Session = Depends(get_db)):
    items, next_cursor, has_more, total_count = crud.get_infinite_sorted_suppliers_items(
        db=db, 
        cursor_str=params.cursor, 
        limit=params.limit
    )
    return {
        "items": items,
        "next_cursor": next_cursor,
        "has_more": has_more,
        "total": total_count
    }
















    






