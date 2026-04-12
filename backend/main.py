from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
import models
import schemas
import utils
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

@app.post("/suppliers/create", response_model = schemas.Supplier_Create_Response, status_code = status.HTTP_201_CREATED)
def write_suppliers_create(supplier: schemas.Supplier_Create, db: Session = Depends(get_db)):
    if utils.is_supplier_name_valid(supplier.name):
        db_supplier = crud.get_supplier_by_name(db, name = supplier.name)
        if db_supplier:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="The supplier already exists.")    
        return crud.create_supplier(db = db, supplier = supplier)
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Wrong a format of the name.")  

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

@app.post("/manufacturers/create", response_model = schemas.Manufacturer_Infinite_Scroll_Response, status_code = status.HTTP_201_CREATED)
def write_manufacturers_create(manufacturer: schemas.Manufacturer_Create, db: Session = Depends(get_db)):
    if utils.is_manufacturer_name_valid(manufacturer.name):
        db_manufacturer = crud.get_manufacturer_by_name(db, name = manufacturer.name)
        if db_manufacturer:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail="The manufacturer already exists.")    
        return crud.create_manufacturer(db = db, manufacturer = manufacturer)
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



import os
import subprocess
import xml.etree.ElementTree as ET
from typing import List, Optional
from pydantic import BaseModel

# Model danych wyjściowych
class SVNItem(BaseModel):
    name: str
    type: str

def list_svn_path(path: str) -> List[SVNItem]:
    
    
    
    # 1. Baza - ścieżka z "volumes" w Twoim docker-compose
    BASE_URL = "file:///local_svn" 
    
    # 2. Bezpieczne łączenie ścieżek
    if path:
        full_url = f"{BASE_URL.rstrip('/')}/{path.strip('/')}"
    else:
        full_url = BASE_URL
    
    # 3. Podstawowa komenda (BEZ wywoływania os.getenv w środku!)
    command = ["svn", "list", "--xml", "--non-interactive", full_url]
    
    # 4. Bezpieczne pobieranie zmiennych środowiskowych
    # (Zostawiłem literówkę PASSOWRD, upewnij się, że w pliku .env masz dokładnie tak samo)
    user = os.getenv("SVN_SERVER_USER")
    password = os.getenv("SVN_SERVER_PASSWORD")
    
    # 5. Doklejanie haseł TYLKO wtedy, gdy faktycznie istnieją (to blokuje błąd NoneType)
    if user and password:
        command.extend([
            "--username", user, 
            "--password", password, 
            "--trust-server-cert",
            "--no-auth-cache"
        ])
    
    try:
        # Pokaże w logach Dockera co dokładnie odpalamy
        print(f"DEBUG: Wykonuję komendę: {' '.join(command)}")
        
        # Wywołujemy proces
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Parsujemy XML
        root = ET.fromstring(result.stdout)
        items = []
        
        for entry in root.findall(".//entry"):
            kind = entry.get("kind")
            
            # Zabezpieczenie przed brakiem nazwy
            name_elem = entry.find("name")
            name = name_elem.text if name_elem is not None else "unknown"
            
            size = None
            if kind == "file":
                size_elem = entry.find("size")
                size = int(size_elem.text) if size_elem is not None else 0
                
            items.append(SVNItem(
                name=name,
                kind=kind,
                size=size
            ))
            
        return items

    except subprocess.CalledProcessError as e:
        # Obsługa błędów samego SVN (np. "brak dostępu")
        error_msg = e.stderr.strip() if e.stderr else "Nieznany błąd SVN"
        print(f"BŁĄD SVN: {error_msg}")
        raise HTTPException(status_code=400, detail=f"SVN Error: {error_msg}")
        
    except Exception as e:
        # Obsługa błędów Pythona/Systemu
        print(f"BŁĄD KRYTYCZNY: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/repository/list", response_model=List[SVNItem])
async def get_svn_list(path: str = Query("", description="Ścieżka wewnątrz repozytorium"),):
    if path.lower().endswith(('.schlib', '.pcblib')):
        try:
            return [SVNItem(name=i["name"], type=i["type"]) for i in utils.svn_get_altium_content("file:///local_svn", path, os.getenv("SVN_SERVER_USER"), os.getenv("SVN_SERVER_PASSWORD"))]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            return [SVNItem(name=i["name"], type=i["type"]) for i in utils.svn_get_folder_list("file:///local_svn", path, os.getenv("SVN_SERVER_USER"), os.getenv("SVN_SERVER_PASSWORD"))]
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
