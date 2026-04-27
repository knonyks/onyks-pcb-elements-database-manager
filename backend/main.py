from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
import models
import schemas
import utils
import crud
from database import engine, SessionLocal
from typing import List
import os
import database
import math

### OTHERS ###
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### REPOSITORY ###
@app.get('/repository/name')
def repository_name():
    return os.getenv("SVN_REPO_NAME", "!E!")

@app.get("/repository/list", response_model=List[schemas.SVNItem])
async def repository_list(path: str = Query("")):
    if path.lower().endswith(('.schlib', '.pcblib')):
        try:
            return [schemas.SVNItem(name=i["name"], type=i["type"]) for i in utils.repository_get_pcb_file_content("file:///local_svn", path, os.getenv('SVN_SERVER_USER', "!E!"), os.getenv('SVN_SERVER_PASSWORD', "!E!"))]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            return [schemas.SVNItem(name=i["name"], type=i["type"]) for i in utils.repository_get_folder_list("file:///local_svn", path, os.getenv('SVN_SERVER_USER', "!E!"), os.getenv('SVN_SERVER_PASSWORD', "!E!"))]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

### MANUFACTURER ###
@app.get("/manufacturer/total")
def manufacturer_total(db: Session = Depends(get_db)):
    return crud.manufacturer_total(db = db)

@app.post("/manufacturer/create", status_code = status.HTTP_201_CREATED)
def manufacturer_create(manufacturer: schemas.ManufacturerCreate, db: Session = Depends(get_db)):
    if utils.manufacturer_name_validation(manufacturer.name):
        db_manufacturer = crud.manufacturer_get_by_name(db, name = manufacturer.name)
        if db_manufacturer:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="The manufacturer already exists.")    
        return crud.manufacturer_create(db = db, manufacturer = manufacturer)
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Wrong a format of the name.")

@app.get("/manufacturer/list")
def manufacturer_list(page: int = 1, limit: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    items_list = crud.manufacturer_list(db, skip=skip, limit=limit)
    total_records = crud.manufacturer_total(db)    
    total_pages = math.ceil(total_records / limit) if limit > 0 else 0   
    return {
        "data": items_list,
        "meta": {
            "total_records": total_records,
            "current_page": page,
            "total_pages": total_pages,
            "limit": limit
        }
    }

### SUPPLIER ###
@app.get("/supplier/total")
def supplier_total(db: Session = Depends(get_db)):
    return crud.supplier_total(db = db)

@app.post("/supplier/create", status_code = status.HTTP_201_CREATED)
def supplier_create(supplier: schemas.SupplierCreate, db: Session = Depends(get_db)):
    if utils.supplier_name_validation(supplier.name):
        db_supplier = crud.supplier_get_by_name(db, name = supplier.name)
        if db_supplier:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="The supplier already exists.")    
        return crud.supplier_create(db = db, supplier = supplier)
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Wrong a format of the name.")

@app.get("/supplier/list")
def supplier_list(page: int = 1, limit: int = 50, db: Session = Depends(get_db)):
    skip = (page - 1) * limit
    items_list = crud.supplier_list(db, skip=skip, limit=limit)
    total_records = crud.supplier_total(db)    
    total_pages = math.ceil(total_records / limit) if limit > 0 else 0   
    return {
        "data": items_list,
        "meta": {
            "total_records": total_records,
            "current_page": page,
            "total_pages": total_pages,
            "limit": limit
        }
    }