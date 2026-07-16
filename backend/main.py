from fastapi import FastAPI, Depends, APIRouter, HTTPException, status, Query
from sqlalchemy.orm import Session
import models
import schemas
import utils
import crud
from database import engine, AsyncSessionLocal
from typing import List
import os
import database
import math
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, Path
from sqlalchemy import select
import uuid
from sqlalchemy import select, func

app = FastAPI()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup_db():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS private;"))
            await conn.run_sync(models.Base.metadata.create_all)
    except Exception as e:
        print(f"❌❌❌: {e}")

@app.get('/repository/name')
async def repositoryName():
    return os.getenv("SVN_REPO_NAME", "Error! Can't get the name of the repository!")

@app.get("/repository/list")
async def repositoryList(path: str):
    enterData = ["file:///local_svn", path, os.getenv('SVN_SERVER_USER', "!E!"), os.getenv('SVN_SERVER_PASSWORD', "!E!")]
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

@app.get('/repository/statistics')
async def repositoryStatistics():
    data = {}
    data['symbols'] = 1
    data['footprints'] = 2
    data['schLibFiles'] = 3
    data['pcbLibFiles'] = 4
    return data

@app.post("/element/create")
async def elementCreate(element: schemas.ElementBase, db = Depends(get_db)):
    item = models.Element(**element.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

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

@app.get("/element/list", response_model = schemas.ElementList)
async def elementList(limit: int = Query(default=10, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    db = Depends(get_db)):

    query = select(func.count()).select_from(models.Element)
    result = await db.execute(query)
    totalCount = result.scalar()
    
    queryEntries = select(models.Element).offset(skip).limit(limit)
    entriesResult = await db.execute(queryEntries)
    entries = entriesResult.scalars().all()
    
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
    
    await db.delete(item)
    await db.commit()
    
    return id

@app.put('/element/edit/{id}')
async def elementEdit(id: uuid.UUID, element: schemas.ElementBase, db = Depends(get_db)):
    query = select(models.Element).where(models.Element.uuid == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UUID doesn't exist!"
        )
    
    update_data = element.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)








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

@app.get('/table/number')
async def tableNumber():
    return 6

@app.get('/table/numbers')
async def tableNumbers():
    data = {}
    data['Inductors'] = 2137
    data['ICs'] = 5012
    data['Transistors'] = 111
    data['Capacitors SMD'] = 1337
    return data

@app.get('/manufacturer/number')
async def manufacturerNumber():
    return 7

@app.get('/manufacturer/numbers')
async def manufacturerNumbers():
    data = {}
    data['ST'] = 2137
    data['Texas Instruments'] = 5012
    data['Analog Devices'] = 111
    data['AMD'] = 1337
    return data

@app.get('/supplier/number')
async def supplierNumber():
    return 8





@app.post('/manufacturer/create')
async def manufacturerCreate(manufacturer: schemas.ManufacturerCreate, db = Depends(get_db)):
    item = models.Manufacturer(**manufacturer.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@app.put('/manufacturer/edit/{id}')
async def manufacturerEdit(id: uuid.UUID, manufacturer: schemas.ManufacturerEdit, db = Depends(get_db)):
    query = select(models.Manufacturer).where(models.Manufacturer.uuid == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UUID doesn't exist!"
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@app.delete('/manufacturer/delete/{id}')
async def manufacturerDelete(id: uuid.UUID, db = Depends(get_db)):
    query = select(models.Manufacturer).where(models.Manufacturer.uuid == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UUID doesn't exist!"
        )
    
    await db.delete(item)
    await db.commit()
    
    return id

@app.post('/supplier/create')
async def supplierCreate(supplier: schemas.SupplierCreate, db = Depends(get_db)):
    item = models.Supplier(**supplier.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@app.put('/supplier/edit/{id}')
async def supplierEdit(id: uuid.UUID, supplier: schemas.SupplierEdit, db = Depends(get_db)):
    query = select(models.Supplier).where(models.Supplier.uuid == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UUID doesn't exist!"
        )
    
    update_data = supplier.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

@app.delete('/supplier/delete/{id}')
async def supplierDelete(id: uuid.UUID, db = Depends(get_db)):
    query = select(models.Supplier).where(models.Supplier.uuid == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UUID doesn't exist!"
        )
    
    await db.delete(item)
    await db.commit()
    
    return id