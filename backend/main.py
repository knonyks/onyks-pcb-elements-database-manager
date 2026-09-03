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
from sqlalchemy import text
from utils import MyRepository, MyDatabase

app = FastAPI()

UPLOAD_DIR = "/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="datasheet")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup_db():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("CREATE SCHEMA IF NOT EXISTS private;"))
            await conn.run_sync(models.Base.metadata.create_all)
            await MyDatabase.updateElementsViews(conn)
    except Exception as e:
        print(f"❌❌❌ DB Startup Failed: {e}")
        raise e

# REPOSITORY
@app.get('/repository/info')
async def get_repository_info():
    repo_name = os.getenv("SVN_REPO_NAME")
    if not repo_name:
        raise HTTPException(status_code=500, detail="Error! Can't get the name of the repository!")
    return {'name': repo_name}

@app.get("/repository/content")
async def get_repository_content(path: str):
    enterData = ["file:///local_svn", path]
    if path.lower().endswith(('.schlib', '.pcblib')):
        try:
            return MyRepository.getPcbContent(*enterData)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            return MyRepository.getFolderList(*enterData)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# ELEMENTS
@app.get('/elements/count')
async def get_elements_count(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Element)
    result = await db.execute(query)
    totalCount = result.scalar()
    return {'count': totalCount}

@app.get('/elements/last-added')
async def get_elements_last_added(db = Depends(get_db)):
    query = (select(models.Element).order_by(models.Element.createdAt.desc()).limit(1))
    result = await db.execute(query)
    
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The database is empty!"
        )
        
    return item

# TABLES
@app.get('/tables/count')
async def get_tables_count(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Table)
    result = await db.execute(query)
    totalCount = result.scalar()
    return {'count': totalCount}

@app.get('/tables/counts')
async def get_tables_counts(db = Depends(get_db)):
    query = select(models.Table.name, func.count(models.Element.uuid)).select_from(models.Table).outerjoin(models.Element, models.Table.name == models.Element.table).group_by(models.Table.name)
    result = await db.execute(query)
    rows = result.all()
    
    data = {}
    for name, count in rows:
        data[name] = count
    
    return data

@app.get("/tables", response_model = schemas.PageResponse[schemas.TableFull])
async def get_tables_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    sortBy: str = Query("id"),
    sortDesc: bool = Query(False),
    db = Depends(get_db)
):
    limit = max(1, min(limit, 100))
    skip = (page - 1) * limit

    count_query = select(func.count()).select_from(models.Table)
    if search:
        search_term = f"%{search.strip()}%"
        count_query = count_query.where(models.Table.name.ilike(search_term))

    count_result = await db.execute(count_query)
    totalCount = count_result.scalar() or 0

    sort_column = getattr(models.Table, sortBy, None)
    if sort_column is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported sortBy value: {sortBy}"
        )

    queryEntries = select(models.Table)
    if search:
        search_term = f"%{search.strip()}%"
        queryEntries = queryEntries.where(models.Table.name.ilike(search_term))

    queryEntries = (
        queryEntries
        .order_by(sort_column.desc() if sortDesc else sort_column.asc())
        .offset(skip)
        .limit(limit)
    )
    entriesResult = await db.execute(queryEntries)
    entries = entriesResult.scalars().all()

    return schemas.PageResponse(items=entries, total=totalCount, page=page, limit=limit)

@app.delete('/tables/{id}')
async def delete_tables(id: int, db = Depends(get_db)):
    query = select(models.Table).where(models.Table.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )
    
    await db.delete(item)
    await db.commit()
    await MyDatabase.updateElementsViews(db)
    
    return id

@app.post('/tables')
async def post_tables(table: schemas.TableBase, db = Depends(get_db)):
    item = models.Table(**table.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data or a supplier with this name already exists."
        )

@app.get('/tables/{id}')
async def get_tables(id: int, db = Depends(get_db)):
    query = select(models.Table).where(models.Table.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )
    
    return item

@app.patch('/tables/{id}')
async def patch_tables(id: int, table: schemas.TableBase, db = Depends(get_db)):
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
        await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a supplier with this name already exists.")

# MANUFACTURERS
@app.get('/manufacturers/count')
async def get_manufacturers_count(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Manufacturer)
    result = await db.execute(query)
    totalCount = result.scalar()
    return {'count': totalCount}

@app.get('/manufacturers/counts')
async def get_manufacturers_counts(db = Depends(get_db)):
    query = select(models.Manufacturer.name, func.count(models.Element.uuid)).select_from(models.Manufacturer).outerjoin(models.Element, models.Manufacturer.name == models.Element.manufacturer).group_by(models.Manufacturer.name)
    result = await db.execute(query)
    rows = result.all()
    
    data = {}
    for name, count in rows:
        data[name] = count
    
    return data

@app.get("/manufacturers", response_model = schemas.PageResponse[schemas.ManufacturerFull])
async def get_manufacturers_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    sortBy: str = Query("id"),
    sortDesc: bool = Query(False),
    db = Depends(get_db)
):
    limit = max(1, min(limit, 100))
    skip = (page - 1) * limit

    count_query = select(func.count()).select_from(models.Manufacturer)
    if search:
        search_term = f"%{search.strip()}%"
        count_query = count_query.where(models.Manufacturer.name.ilike(search_term))

    count_result = await db.execute(count_query)
    totalCount = count_result.scalar() or 0

    sort_column = getattr(models.Manufacturer, sortBy, None)
    if sort_column is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported sortBy value: {sortBy}"
        )

    queryEntries = select(models.Manufacturer)
    if search:
        search_term = f"%{search.strip()}%"
        queryEntries = queryEntries.where(models.Manufacturer.name.ilike(search_term))

    queryEntries = (
        queryEntries
        .order_by(sort_column.desc() if sortDesc else sort_column.asc())
        .offset(skip)
        .limit(limit)
    )
    entriesResult = await db.execute(queryEntries)
    entries = entriesResult.scalars().all()

    return schemas.PageResponse(items=entries, total=totalCount, page=page, limit=limit)

@app.delete('/manufacturers/{id}')
async def delete_manufacturers(id: int, db = Depends(get_db)):
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
    await MyDatabase.updateElementsViews(db)
    
    return id

@app.post('/manufacturers')
async def post_manufacturers(manufacturer: schemas.ManufacturerBase, db = Depends(get_db)):
    item = models.Manufacturer(**manufacturer.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data or a supplier with this name already exists."
        )

@app.get('/manufacturers/{id}')
async def get_manufacturers(id: int, db = Depends(get_db)):
    query = select(models.Manufacturer).where(models.Manufacturer.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )
    
    return item

@app.patch('/manufacturers/{id}')
async def patch_manufacturers(id: int, manufacturer: schemas.ManufacturerBase, db = Depends(get_db)):
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
        await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a supplier with this name already exists.")

# SUPPLIERS
@app.get('/suppliers/count')
async def get_suppliers_count(db = Depends(get_db)):
    query = select(func.count()).select_from(models.Supplier)
    result = await db.execute(query)
    totalCount = result.scalar()
    return {'count': totalCount}

@app.get("/suppliers", response_model = schemas.PageResponse[schemas.SupplierFull])
async def get_suppliers_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    sortBy: str = Query("id"),
    sortDesc: bool = Query(False),
    db = Depends(get_db)
):
    limit = max(1, min(limit, 100))
    skip = (page - 1) * limit

    count_query = select(func.count()).select_from(models.Supplier)
    if search:
        search_term = f"%{search.strip()}%"
        count_query = count_query.where(models.Supplier.name.ilike(search_term))

    count_result = await db.execute(count_query)
    totalCount = count_result.scalar() or 0

    sort_column = getattr(models.Supplier, sortBy, None)
    if sort_column is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported sortBy value: {sortBy}"
        )

    queryEntries = select(models.Supplier)
    if search:
        search_term = f"%{search.strip()}%"
        queryEntries = queryEntries.where(models.Supplier.name.ilike(search_term))

    queryEntries = (
        queryEntries
        .order_by(sort_column.desc() if sortDesc else sort_column.asc())
        .offset(skip)
        .limit(limit)
    )
    entriesResult = await db.execute(queryEntries)
    entries = entriesResult.scalars().all()

    return schemas.PageResponse(items=entries, total=totalCount, page=page, limit=limit)

@app.delete('/suppliers/{id}')
async def delete_suppliers(id: int, db = Depends(get_db)):
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
    await MyDatabase.updateElementsViews(db)
    
    return id

@app.post('/suppliers')
async def post_suppliers(supplier: schemas.SupplierBase, db = Depends(get_db)):
    item = models.Supplier(**supplier.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data or a supplier with this name already exists."
        )

@app.get('/suppliers/{id}')
async def get_suppliers(id: int, db = Depends(get_db)):
    query = select(models.Supplier).where(models.Supplier.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )
    
    return item

@app.patch('/suppliers/{id}')
async def patch_suppliers(id: int, supplier: schemas.SupplierBase, db = Depends(get_db)):
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
        await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a supplier with this name already exists.")

# USERS
@app.get("/users", response_model = schemas.PageResponse[schemas.UserFull])
async def get_users_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    search: str | None = Query(None),
    sortBy: str = Query("id"),
    sortDesc: bool = Query(False),
    db = Depends(get_db)
):
    user_model = models.User
    limit = max(1, min(limit, 100))
    skip = (page - 1) * limit

    sort_column = getattr(user_model, sortBy, None)
    if sort_column is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported sortBy value: {sortBy}"
        )

    count_query = select(func.count()).select_from(user_model)
    query_entries = select(user_model)
    if search:
        search_term = f"%{search.strip()}%"
        search_filters = [
            column.ilike(search_term)
            for column in user_model.__table__.columns
            if getattr(column.type, "python_type", None) is str
        ]
        if search_filters:
            from sqlalchemy import or_
            search_filter = or_(*search_filters)
            count_query = count_query.where(search_filter)
            query_entries = query_entries.where(search_filter)

    count_result = await db.execute(count_query)
    total_count = count_result.scalar() or 0

    query_entries = (
        query_entries
        .order_by(sort_column.desc() if sortDesc else sort_column.asc())
        .offset(skip)
        .limit(limit)
    )
    entries_result = await db.execute(query_entries)
    entries = entries_result.scalars().all()

    return schemas.PageResponse(
        items=entries,
        total=total_count,
        page=page,
        limit=limit
    )

@app.delete('/users/{id}')
async def delete_users(id: int, db = Depends(get_db)):
    query = select(models.User).where(models.User.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )

    await db.delete(item)
    await db.commit()
    await MyDatabase.updateElementsViews(db)

    return id







@app.post('/users')
async def post_users(user: schemas.UserBase, db = Depends(get_db)):
    item = models.User(**user.model_dump())
    db.add(item)
    try:
        await db.commit()
        await db.refresh(item)
        await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data or a user with these details already exists."
        )

@app.get('/users/{id}')
async def get_users(id: int, db = Depends(get_db)):
    query = select(models.User).where(models.User.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )

    return item

@app.patch('/users/{id}')
async def patch_users(id: int, user: schemas.UserBase, db = Depends(get_db)):
    query = select(models.User).where(models.User.id == id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID doesn't exist!"
        )

    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    try:
        db.add(item)
        await db.commit()
        await db.refresh(item)
        await MyDatabase.updateElementsViews(db)
        return item
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid data or a user with these details already exists."
        )

# SERVER
@app.get('/server/info')
async def get_server_info():
    return {'name': 'ONYKS Bloodstone', 'version': 'v0.2.0-alpha'}

##############################################################



# ELEMENT
# do poprawy
# @app.post("/element/create")
# async def elementCreate(
#     element: str = Form(...),
#     datasheet: UploadFile | None = File(default=None), 
#     db = Depends(get_db)):
#     if datasheet is not None and datasheet.content_type != "application/pdf":
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Datasheet must be a PDF file."
#         )

#     item_data = schemas.ElementBase.model_validate_json(element).model_dump(
#         exclude={"isDatasheetSupposedToChange"}
#     )
#     item = models.Element(**item_data)
#     item.datasheet = False
#     db.add(item)
#     pdf_path = None
#     try:
#         await db.flush()

#         if datasheet is not None:
#             pdf_path = os.path.join(UPLOAD_DIR, f"{item.uuid}.pdf")
#             with open(pdf_path, "wb") as pdf_file:
#                 while chunk := await datasheet.read(1024 * 1024):
#                     pdf_file.write(chunk)
#             item.datasheet = True

#         await db.commit()
#         await db.refresh(item)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         if pdf_path is not None:
#             try:
#                 os.remove(pdf_path)
#             except FileNotFoundError:
#                 pass
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid input data."
#         )
#     except Exception:
#         await db.rollback()
#         if pdf_path is not None:
#             try:
#                 os.remove(pdf_path)
#             except FileNotFoundError:
#                 pass
#         raise

# # do poprawy
# @app.post("/element/duplicate/{id}")
# async def elementDuplicate(
#     id: uuid.UUID,
#     element: str = Form(...),
#     datasheet: UploadFile | None = File(default=None),
#     db = Depends(get_db)
# ):
#     element_data = schemas.ElementBase.model_validate_json(element)
#     change_mode = element_data.isDatasheetSupposedToChange

#     if change_mode not in (0, 1, 2):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="isDatasheetSupposedToChange must be 0, 1 or 2."
#         )
#     if change_mode == 2 and datasheet is None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="A new datasheet is required."
#         )
#     if datasheet is not None and datasheet.content_type != "application/pdf":
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Datasheet must be a PDF file."
#         )

#     result = await db.execute(
#         select(models.Element).where(models.Element.uuid == id)
#     )
#     source = result.scalar_one_or_none()
#     if source is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail="UUID doesn't exist!")

#     data = element_data.model_dump()
#     data.pop("isDatasheetSupposedToChange", None)
#     data["uuid"] = uuid.uuid4()
#     data["datasheet"] = False
#     item = models.Element(**data)
#     db.add(item)

#     new_pdf_path = os.path.join(UPLOAD_DIR, f"{item.uuid}.pdf")
#     old_pdf_path = os.path.join(UPLOAD_DIR, f"{source.uuid}.pdf")
#     try:
#         await db.flush()
#         if change_mode == 0:
#             if not source.datasheet or not os.path.isfile(old_pdf_path):
#                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                                     detail="The source element has no datasheet.")
#             shutil.copyfile(old_pdf_path, new_pdf_path)
#             item.datasheet = True
#         elif change_mode == 2:
#             with open(new_pdf_path, "wb") as pdf_file:
#                 while chunk := await datasheet.read(1024 * 1024):
#                     pdf_file.write(chunk)
#             item.datasheet = True

#         await db.commit()
#         await db.refresh(item)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         if os.path.isfile(new_pdf_path):
#             os.remove(new_pdf_path)
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
#     except Exception:
#         await db.rollback()
#         if os.path.isfile(new_pdf_path):
#             os.remove(new_pdf_path)
#         raise






# # do poprawy
# @app.get("/element/list")
# async def elementList(limit: int = Query(default=10, ge=1, le=100),
#     skip: int = Query(default=0, ge=0),
#     db = Depends(get_db)):

#     query = select(func.count()).select_from(models.Element)
#     result = await db.execute(query)
#     totalCount = result.scalar()
    
#     queryEntries = select(models.Element).offset(skip).limit(limit)
#     entriesResult = await db.execute(queryEntries)
#     entries = []
#     for item in entriesResult.scalars().all():
#         entry = {
#             key: value
#             for key, value in vars(item).items()
#             if key not in {"_sa_instance_state", "suppliers"}
#         }
#         suppliers = getattr(item, "suppliers", None)
#         if isinstance(suppliers, dict):
#             entry.update({f"supplier_{key}": value for key, value in suppliers.items()})
#         entries.append(entry)
    
#     return {"total": totalCount, "items": entries}

# # do poprawy
# @app.delete('/element/delete/{id}')
# async def elementDelete(id: uuid.UUID, db = Depends(get_db)):
#     query = select(models.Element).where(models.Element.uuid == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="UUID doesn't exist!"
#         )

#     pdf_path = os.path.join(UPLOAD_DIR, f"{id}.pdf")
#     if os.path.isfile(pdf_path):
#         os.remove(pdf_path)
    
#     await db.delete(item)
#     await db.commit()
    
#     return id

# # do poprawy
# @app.put('/element/edit/{id}')
# async def elementEdit(id: uuid.UUID, element: str = Form(...), datasheet: UploadFile | None = File(default=None), db = Depends(get_db)):
#     query = select(models.Element).where(models.Element.uuid == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="UUID doesn't exist!"
#         )
    
#     update_data = schemas.ElementBase.model_validate_json(element).model_dump(exclude_unset=True)
#     datasheet_change = update_data.pop('isDatasheetSupposedToChange', 0)
#     if datasheet_change not in (0, 1, 2):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="isDatasheetSupposedToChange must be 0, 1, or 2."
#         )
#     if datasheet_change == 2:
#         if datasheet is None:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Datasheet is required when replacing the datasheet."
#             )
#         if datasheet.content_type != "application/pdf":
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 detail="Datasheet must be a PDF file."
#             )

#     update_data['uuid'] = id
#     update_data['createdAt'] = item.createdAt

#     pdf_path = os.path.join(UPLOAD_DIR, f"{id}.pdf")
#     for field, value in update_data.items():
#         setattr(item, field, value)

#     if datasheet_change == 2:
#         try:
#             with open(pdf_path, "wb") as pdf_file:
#                 while chunk := await datasheet.read(1024 * 1024):
#                     pdf_file.write(chunk)
#             item.datasheet = True
#         except Exception:
#             await db.rollback()
#             raise
#     elif datasheet_change == 1:
#         if os.path.isfile(pdf_path):
#             os.remove(pdf_path)
#         item.datasheet = False
    
#     try:
#         db.add(item)
#         await db.commit()
#         await db.refresh(item)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input data")

# # do poprawy
# @app.get('/element/{id}')
# async def elementID(id: uuid.UUID = Path(...), db = Depends(get_db)):
#     query = select(models.Element).where(models.Element.uuid == id)
    
#     result = await db.execute(query)
    
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="UUID doesn't exist!"
#         )
        
#     return item

# # MANUFACTURER


# # do poprawy
# @app.post('/manufacturer/create')
# async def manufacturerCreate(manufacturer: schemas.ManufacturerBase, db = Depends(get_db)):
#     query = select(models.Manufacturer).where(models.Manufacturer.name == manufacturer.name)
#     existing = await db.execute(query)
    
#     if existing.scalar_one_or_none() is not None:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Manufacturer with this name already exists."
#         )
    
#     item = models.Manufacturer(**manufacturer.model_dump())
#     db.add(item)
#     try:
#         await db.commit()
#         await db.refresh(item)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid manufacturer data.")

# # do poprawy
# @app.delete('/manufacturer/delete/{id}')
# async def manufacturerDelete(id: int, db = Depends(get_db)):
#     query = select(models.Manufacturer).where(models.Manufacturer.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )
    
#     await db.delete(item)
#     await db.commit()
    
#     return id

# # do poprawy
# @app.get("/manufacturer/list", response_model = schemas.ManufacturerList)
# async def manufacturerList(limit: int = Query(default=10, ge=1, le=100), skip: int = Query(default=0, ge=0), db = Depends(get_db)):
#     query = select(func.count()).select_from(models.Manufacturer)
#     result = await db.execute(query)
#     totalCount = result.scalar()
    
#     queryEntries = select(models.Manufacturer).order_by(models.Manufacturer.id).offset(skip).limit(limit)
#     entriesResult = await db.execute(queryEntries)
#     entries = entriesResult.scalars().all()
    
#     return {"total": totalCount, "items": entries}

# @app.put('/manufacturer/edit/{id}')
# async def manufacturerEdit(id: int, manufacturer: schemas.ManufacturerBase, db = Depends(get_db)):
#     query = select(models.Manufacturer).where(models.Manufacturer.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )
    
#     update_data = manufacturer.model_dump(exclude_unset=True)

#     for field, value in update_data.items():
#         setattr(item, field, value)
    
#     try:
#         db.add(item)
#         await db.commit()
#         await db.refresh(item)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a manufacturer with this name already exists.")



# # SUPPLIER



# # TABLE




# @app.put('/table/edit/{id}')
# async def tableEdit(id: int, table: schemas.TableBase, db = Depends(get_db)):
#     query = select(models.Table).where(models.Table.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )
    
#     update_data = table.model_dump(exclude_unset=True)
    
#     for field, value in update_data.items():
#         setattr(item, field, value)
    
#     try:
#         db.add(item)
#         await db.commit()
#         await db.refresh(item)
#         await utils.dbCreateOrUpdateElementViews(db)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a table with this name already exists.")

# @app.post('/table/create')
# async def tableCreate(table: schemas.TableBase, db = Depends(get_db)):
#     item = models.Table(**table.model_dump())
#     db.add(item)
#     try:
#         await db.commit()
#         await db.refresh(item)
#         await utils.dbCreateOrUpdateElementViews(db)
#         return item
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid data or a table with this name already exists.")

# @app.delete('/table/delete/{id}')
# async def tableDelete(id: int, db = Depends(get_db)):
#     query = select(models.Table).where(models.Table.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )

#     elements_query = select(func.count()).select_from(models.Element).where(
#         models.Element.table == item.name
#     )
#     elements_result = await db.execute(elements_query)
#     if elements_result.scalar() > 0:
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="The table cannot be deleted while it contains elements."
#         )
    
#     await db.delete(item)
#     await db.commit()
#     await utils.dbCreateOrUpdateElementViews(db)
#     return id

# @app.get("/table/list", response_model = schemas.TableList)
# async def tableList(limit: int = Query(default=10, ge=1, le=100), skip: int = Query(default=0, ge=0), db = Depends(get_db)):
#     query = select(func.count()).select_from(models.Table)
#     result = await db.execute(query)
#     totalCount = result.scalar()
    
#     queryEntries = select(models.Table).order_by(models.Table.id).offset(skip).limit(limit)
#     entriesResult = await db.execute(queryEntries)
#     entries = entriesResult.scalars().all()
    
#     return {"total": totalCount, "items": entries}

# @app.get('/table/{id}')
# async def tableID(id: int, db = Depends(get_db)):
#     query = select(models.Table).where(models.Table.id == id)
#     result = await db.execute(query)
#     item = result.scalar_one_or_none()
    
#     if item is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="ID doesn't exist!"
#         )
    
#     count_query = select(func.count()).select_from(models.Element).where(models.Element.table == item.name)
#     count_result = await db.execute(count_query)
#     elements_count = count_result.scalar()
    
#     return {
#         "table": item,
#         "numberOfItems": elements_count
#     }