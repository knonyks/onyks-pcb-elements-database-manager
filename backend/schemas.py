from pydantic import BaseModel

# Requests
class Manufacturer_Create(BaseModel):
    name: str

class Supplier_Create(BaseModel):
    name: str

class Table_Create(BaseModel):
    name: str

# Responses
class Total_Elements_Response(BaseModel):
    total: int

class Total_Tables_Response(BaseModel):
    total: int

class Total_Manufacturers_Response(BaseModel):
    total: int

class Total_Suppliers_Response(BaseModel):
    total: int

class Last_Added_Element_Response(BaseModel):
    uuid: str
    part_name: str

class Repository_Summary_Response(BaseModel):
    symbols_total: int
    footprints_total: int
    pcblibs_files_total: int
    schlibs_files_total: int

class Tables_Amounts_Response(BaseModel):
    tables: dict[str, int]

class Manufacturers_Amounts_Response(BaseModel):
    manufacturers: dict[str, int]

class Suppliers_Amounts_Response(BaseModel):
    suppliers: dict[str, int]

class Total_Manufacturers_Response(BaseModel):
    total: int

# class Create_Supplier_Response(BaseModel):
#     id: int
#     name: str

# class Create_Manufacturer_Response(BaseModel):
#     id: int
#     name: str

# class Supplier(BaseModel):
#     id: int
#     name: str
#     elements_amount: int
#     created_at: str

#     class Config:
#         orm_mode = True