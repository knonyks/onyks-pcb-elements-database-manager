from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
import models
import schemas
import utils
import crud
from database import engine, AsyncSessionLocal
from typing import List
import os
import shutil
import database
import math
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, Path
from sqlalchemy import select
import uuid
from sqlalchemy import select, func
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.staticfiles import StaticFiles
from pydantic import Json

app = FastAPI()

UPLOAD_DIR = "/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="datasheet")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

from sqlalchemy import text

@app.on_event("startup")
async def startup_db():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS private;"))
            await conn.run_sync(models.Base.metadata.create_all)
            await utils.dbCreateOrUpdateElementViews(conn)
    except Exception as e:
        print(f"❌❌❌ DB Startup Failed: {e}")
        raise e

# REPOSITORY
@app.get('/repository/name')
async def repositoryName():
    return os.getenv("SVN_REPO_NAME", "Error! Can't get the name of the repository!")

@app.get("/repository/list")
async def repositoryList(path: str):
    enterData = ["file:///local_svn", path]
    if path.lower().endswith(('.schlib', '.pcblib')):
        try:
            return utils.repositoryGetPCBFileContent(*enterData)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            return utils.repositoryGetFolderList(*enterData)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# ELEMENT
@app.post("/element/create")
async def elementCreate(
    element: str = Form(...),
    datasheet: UploadFile | None = File(default=None), 
    db = Depends(get_db)):
    if datasheet is not None and datasheet.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Datasheet must be a PDF file."
        )

    item_data = schemas.ElementBase.model_validate_json(element).model_dump(
        exclude={"isDatasheetSupposedToChange"}
    )
    item = models.Element(**item_data)
    item.datasheet = False
    db.add(item)
    pdf_path = None
    try:
        await db.flush()

        if datasheet is not None:
            pdf_path = os.path.join(UPLOAD_DIR, f"{item.uuid}.pdf")
            with open(pdf_path, "wb") as pdf_file:
                while chunk := await datasheet.read(1024 * 1024):
                    pdf_file.write(chunk)
            item.datasheet = True

        await db.commit()
        await db.refresh(item)
        return item
    except IntegrityError:
        await db.rollback()
        if pdf_path is not None:
            try:
                os.remove(pdf_path)
            except FileNotFoundError:
                pass
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid input data."
        )
    except Exception:
        await db.rollback()
        if pdf_path is not None:
            try:
                os.remove(pdf_path)
            except FileNotFoundError:
                pass
        raise

@app.post("/element/duplicate/{id}")
async def elementDuplicate(
    id: uuid.UUID,
    element: str = Form(...),
    datasheet: UploadFile | None = File(default=None),
    db = Depends(get_db)
):
    element_data = schemas.ElementBase.model_validate_json(element)
    change_mode = element_data.isDatasheetSupposedToChange

    if change_mode not in (0, 1, 2):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="isDatasheetSupposedToChange must be 0, 1 or 2."
        )
    if change_mode == 2 and datasheet is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A new datasheet is required."
        )
    if datasheet is not None and datasheet.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Datasheet must be a PDF file."
        )

    result = await db.execute(
        select(models.Element).where(models.Element.uuid == id)
    )
    source = result.scalar_one_or_none()
    if source is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="UUID doesn't exist!")

    data = element_data.model_dump()
    data.pop("isDatasheetSupposedToChange", None)
    data["uuid"] = uuid.uuid4()
    data["datasheet"] = False
    item = models.Element(**data)
    db.add(item)

    new_pdf_path = os.path.join(UPLOAD_DIR, f"{item.uuid}.pdf")
    old_pdf_path = os.path.join(UPLOAD_DIR, f"{source.uuid}.pdf")
    try:
        await db.flush()
        if change_mode == 0:
            if not source.datasheet or not os.path.isfile(old_pdf_path):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="The source element has no datasheet.")
            shutil.copyfile(old_pdf_path, new_pdf_path)
            item.datasheet = True
        elif change_mode == 2:
            with open(new_pdf_path, "wb") as pdf_file:
                while chunk := await datasheet.read(1024 * 1024):
                    pdf_file.write(chunk)
            item.datasheet = True

        await db.commit()
        await db.refresh(item)
        return item
    except IntegrityError:
        await db.rollback()
        if os.path.isfile(new_pdf_path):
            os.remove(new_pdf_path)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception:
        await db.rollback()
        if os.path.isfile(new_pdf_path):
            os.remove(new_pdf_path)
        raise

@app.get('/element/last-added')
async def elementLastAdded(db = Depends(get_db)):
    query = (
            select(models.Element)
            .order_by(models.Element.createdAt.desc())
            .limit(1)
        )
    
    result = await db.execute(query)
    
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The database is empty!"
        )
        
    return item

@app.get('/element/number')
async def elementNumber(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Element)
    result = await db.execute(query)
    totalCount = result.scalar()
    return totalCount

@app.get("/element/list")
async def elementList(limit: int = Query(default=10, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    db = Depends(get_db)):

    query = select(func.count()).select_from(models.Element)
    result = await db.execute(query)
    totalCount = result.scalar()
    
    queryEntries = select(models.Element).offset(skip).limit(limit)
    entriesResult = await db.execute(queryEntries)
    entries = []
    for item in entriesResult.scalars().all():
        entry = {
            key: value
            for key, value in vars(item).items()
            if key not in {"_sa_instance_state", "suppliers"}
        }
        suppliers = getattr(item, "suppliers", None)
        if isinstance(suppliers, dict):
            entry.update({f"supplier_{key}": value for key, value in suppliers.items()})
        entries.append(entry)
    
    return {"total": totalCount, "items": entries}

@app.delete('/element/delete/{id}')
async def elementDelete(id: uuid.UUID, db = Depends(get_db)):
    query = select(models.Element).where(models.Element.uuid == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UUID doesn't exist!"
        )

    pdf_path = os.path.join(UPLOAD_DIR, f"{id}.pdf")
    if os.path.isfile(pdf_path):
        os.remove(pdf_path)
    
    await db.delete(item)
    await db.commit()
    
    return id

@app.put('/element/edit/{id}')
async def elementEdit(id: uuid.UUID, element: str = Form(...), datasheet: UploadFile | None = File(default=None), db = Depends(get_db)):
    query = select(models.Element).where(models.Element.uuid == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UUID doesn't exist!"
        )
    
    update_data = schemas.ElementBase.model_validate_json(element).model_dump(exclude_unset=True)
    datasheet_change = update_data.pop('isDatasheetSupposedToChange', 0)
    if datasheet_change not in (0, 1, 2):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="isDatasheetSupposedToChange must be 0, 1, or 2."
        )
    if datasheet_change == 2:
        if datasheet is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Datasheet is required when replacing the datasheet."
            )
        if datasheet.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Datasheet must be a PDF file."
            )

    update_data['uuid'] = id
    update_data['createdAt'] = item.createdAt

    pdf_path = os.path.join(UPLOAD_DIR, f"{id}.pdf")
    for field, value in update_data.items():
        setattr(item, field, value)

    if datasheet_change == 2:
        try:
            with open(pdf_path, "wb") as pdf_file:
                while chunk := await datasheet.read(1024 * 1024):
                    pdf_file.write(chunk)
            item.datasheet = True
        except Exception:
            await db.rollback()
            raise
    elif datasheet_change == 1:
        if os.path.isfile(pdf_path):
            os.remove(pdf_path)
        item.datasheet = False
    
    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input data")

@app.get('/element/{id}')
async def elementID(id: uuid.UUID = Path(...), db = Depends(get_db)):
    query = select(models.Element).where(models.Element.uuid == id)
    
    result = await db.execute(query)
    
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UUID doesn't exist!"
        )
        
    return item

# MANUFACTURER
@app.get('/manufacturer/number')
async def manufacturerNumber(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Manufacturer)
    result = await db.execute(query)
    totalCount = result.scalar()
    return totalCount

@app.post('/manufacturer/create')
async def manufacturerCreate(manufacturer: schemas.ManufacturerBase, db = Depends(get_db)):
    query = select(models.Manufacturer).where(models.Manufacturer.name == manufacturer.name)
    existing = await db.execute(query)
    
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Manufacturer with this name already exists."
        )
    
    item = models.Manufacturer(**manufacturer.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid manufacturer data.")

@app.delete('/manufacturer/delete/{id}')
async def manufacturerDelete(id: int, db = Depends(get_db)):
    query = select(models.Manufacturer).where(models.Manufacturer.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )
    
    await db.delete(item)
    await db.commit()
    
    return id

@app.get("/manufacturer/list", response_model = schemas.ManufacturerList)
async def manufacturerList(limit: int = Query(default=10, ge=1, le=100), skip: int = Query(default=0, ge=0), db = Depends(get_db)):
    query = select(func.count()).select_from(models.Manufacturer)
    result = await db.execute(query)
    totalCount = result.scalar()
    
    queryEntries = select(models.Manufacturer).order_by(models.Manufacturer.id).offset(skip).limit(limit)
    entriesResult = await db.execute(queryEntries)
    entries = entriesResult.scalars().all()
    
    return {"total": totalCount, "items": entries}

@app.put('/manufacturer/edit/{id}')
async def manufacturerEdit(id: int, manufacturer: schemas.ManufacturerBase, db = Depends(get_db)):
    query = select(models.Manufacturer).where(models.Manufacturer.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )
    
    update_data = manufacturer.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(item, field, value)
    
    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a manufacturer with this name already exists.")

@app.get('/manufacturer/numbers')
async def manufacturerNumbers(db = Depends(get_db)):
    query = select(models.Manufacturer.name, func.count(models.Element.uuid)).select_from(models.Manufacturer).outerjoin(models.Element, models.Manufacturer.name == models.Element.manufacturer).group_by(models.Manufacturer.name)
    result = await db.execute(query)
    rows = result.all()
    
    data = {}
    for name, count in rows:
        data[name] = count
    
    return data

# SUPPLIER
@app.get('/supplier/number')
async def supplierNumber(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Supplier)
    result = await db.execute(query)
    totalCount = result.scalar()
    return totalCount

@app.get("/supplier/list", response_model = schemas.SupplierList)
async def supplierList(limit: int = Query(default=10, ge=1, le=100), skip: int = Query(default=0, ge=0), db = Depends(get_db)):
    query = select(func.count()).select_from(models.Supplier)
    result = await db.execute(query)
    totalCount = result.scalar()
    
    queryEntries = select(models.Supplier).offset(skip).limit(limit)
    entriesResult = await db.execute(queryEntries)
    entries = entriesResult.scalars().all()
    
    return {"total": totalCount, "items": entries}

@app.delete('/supplier/delete/{id}')
async def supplierDelete(id: int, db = Depends(get_db)):
    query = select(models.Supplier).where(models.Supplier.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )
    
    await db.delete(item)
    await db.commit()
    await utils.dbCreateOrUpdateElementViews(db)
    
    return id

@app.post('/supplier/create')
async def supplierCreate(supplier: schemas.SupplierBase, db = Depends(get_db)):
    item = models.Supplier(**supplier.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        await utils.dbCreateOrUpdateElementViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data or a supplier with this name already exists."
        )

@app.get('/supplier/{id}')
async def supplierID(id: int, db = Depends(get_db)):
    query = select(models.Supplier).where(models.Supplier.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )
    
    return item

@app.put('/supplier/edit/{id}')
async def supplierEdit(id: int, supplier: schemas.SupplierBase, db = Depends(get_db)):
    query = select(models.Supplier).where(models.Supplier.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )
    
    update_data = supplier.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(item, field, value)
    
    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        await utils.dbCreateOrUpdateElementViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a supplier with this name already exists.")

# TABLE
@app.get('/table/number')
async def tableNumber(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Table)
    result = await db.execute(query)
    totalCount = result.scalar()
    return totalCount

@app.get('/table/numbers')
async def tableNumbers(db = Depends(get_db)):
    query = select(models.Table.name, func.count(models.Element.uuid)).select_from(models.Table).outerjoin(models.Element, models.Table.name == models.Element.table).group_by(models.Table.name)
    result = await db.execute(query)
    rows = result.all()
    
    data = {}
    for name, count in rows:
        data[name] = count
    
    return data

@app.put('/table/edit/{id}')
async def tableEdit(id: int, table: schemas.TableBase, db = Depends(get_db)):
    query = select(models.Table).where(models.Table.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )
    
    update_data = table.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(item, field, value)
    
    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        await utils.dbCreateOrUpdateElementViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a table with this name already exists.")

@app.post('/table/create')
async def tableCreate(table: schemas.TableBase, db = Depends(get_db)):
    item = models.Table(**table.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        await utils.dbCreateOrUpdateElementViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a table with this name already exists.")

@app.delete('/table/delete/{id}')
async def tableDelete(id: int, db = Depends(get_db)):
    query = select(models.Table).where(models.Table.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )

    elements_query = select(func.count()).select_from(models.Element).where(
        models.Element.table == item.name
    )
    elements_result = await db.execute(elements_query)
    if elements_result.scalar() > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The table cannot be deleted while it contains elements."
        )
    
    await db.delete(item)
    await db.commit()
    await utils.dbCreateOrUpdateElementViews(db)
    return id

@app.get("/table/list", response_model = schemas.TableList)
async def tableList(limit: int = Query(default=10, ge=1, le=100), skip: int = Query(default=0, ge=0), db = Depends(get_db)):
    query = select(func.count()).select_from(models.Table)
    result = await db.execute(query)
    totalCount = result.scalar()
    
    queryEntries = select(models.Table).order_by(models.Table.id).offset(skip).limit(limit)
    entriesResult = await db.execute(queryEntries)
    entries = entriesResult.scalars().all()
    
    return {"total": totalCount, "items": entries}

@app.get('/table/{id}')
async def tableID(id: int, db = Depends(get_db)):
    query = select(models.Table).where(models.Table.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )
    
    count_query = select(func.count()).select_from(models.Element).where(models.Element.table == item.name)
    count_result = await db.execute(count_query)
    elements_count = count_result.scalar()
    
    return {
        "table": item,
        "numberOfItems": elements_count
    }

@app.get('/repository/statistics')
async def repositoryStatistics():
    data = {}
    data['symbols'] = 1
    data['footprints'] = 2
    data['schLibFiles'] = 3
    data['pcbLibFiles'] = 4
    return data

@app.get('/server/identity')
async def repositoryStatistics():
    return 'ONYKS Bloodstone'