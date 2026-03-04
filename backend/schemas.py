from pydantic import BaseModel, ConfigDict, Field, constr, field_validator
from datetime import datetime
from typing import List, Optional
from fastapi import Query

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

########################################################################################

class Supplier_Create(BaseModel):
    name: str = constr(strip_whitespace=True, min_length=3, max_length=50)

class Supplier_Create_Response(BaseModel):
    name: str

class Supplier_Response(BaseModel):
    id: int
    name: str
    created_at: datetime
    class Config:
        from_attributes = True
        
    @field_validator('created_at', mode='before')
    @classmethod
    def fix_datetime_format(cls, value):
        if isinstance(value, str):
            value = value.replace(" ", "T")
            if value.endswith("+00"):
                value = value.replace("+00", "+00:00")
        return value

class Supplier_Pagination:
    def __init__(
        self,
        cursor: Optional[int] = Query(None, description="Last loaded ID supplier"),
        limit: int = Query(20, ge=1, le=100, description="How many entries to load"),
        search_query: Optional[str] = Query(None, description="What it's looking for"),
        search_columns: Optional[List[str]] = Query(None, description="Where it's looking for")):
        self.cursor = cursor
        self.limit = limit
        self.search_query = search_query
        self.search_columns = search_columns

class Supplier_Pagination_Response(BaseModel):
    suppliers: List[Supplier_Response]
    next_cursor: Optional[int] = None
    total_count: int


