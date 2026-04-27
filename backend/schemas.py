from pydantic import BaseModel, ConfigDict, Field, constr, field_validator
from datetime import datetime
from typing import List, Optional, Generic, TypeVar
from fastapi import Query

T = TypeVar('T')

### REPOSITORY ###
class SVNItem(BaseModel):
    name: str
    type: str

class SVNListResponse(BaseModel):
    items: List[SVNItem]

### MANUFACTURER ###
class ManufacturerBase(BaseModel):
    name: str = constr(strip_whitespace=True, min_length=1, max_length=50)

class ManufacturerCreate(ManufacturerBase):
    pass

### SUPPLIER ###
class SupplierBase(BaseModel):
    name: str = constr(strip_whitespace=True, min_length=1, max_length=50)

class SupplierCreate(SupplierBase):
    pass
