from pydantic import BaseModel, ConfigDict, Field, constr, field_validator
from datetime import datetime
from typing import List, Optional, Generic, TypeVar
from fastapi import Query

T = TypeVar('T')

class Element_Total_Response(BaseModel):
    total: int

class Table_Total_Response(BaseModel):
    total: int

class Manufacturer_Total_Response(BaseModel):
    total: int

class Supplier_Total_Response(BaseModel):
    total: int

class Element_Last_Added_Response(BaseModel):
    uuid: str
    part_name: str
    manufacturer: str
    created_at: str

class Repository_Summary_Response(BaseModel):
    symbols_total: int
    footprints_total: int
    pcblibs_files_total: int
    schlibs_files_total: int

class Table_Amounts_Response(BaseModel):
    tables: dict[str, int]

class Manufacturer_Amounts_Response(BaseModel):
    manufacturers: dict[str, int]

class Supplier_Amounts_Response(BaseModel):
    suppliers: dict[str, int]

class Supplier_Create(BaseModel):
    name: str = constr(strip_whitespace=True, min_length=1, max_length=50)

class Supplier_Create_Response(BaseModel):
    name: str

class Infinite_Scroll(BaseModel):
    cursor: Optional[str] = Field(None, description = "Base64")
    limit: int = Field(20, ge=1, le=100)

class Infinite_Scroll_Response(BaseModel, Generic[T]):
    items: List[T]
    next_cursor: Optional[str] = None
    has_more: bool
    total: Optional[int] = None

class Supplier_Infinite_Scroll_Response(BaseModel):
    name: str

class Manufacturer_Create(BaseModel):
    name: str = constr(strip_whitespace=True, min_length=1, max_length=50)

class Manufacturer_Infinite_Scroll_Response(BaseModel):
    name: str