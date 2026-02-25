from fastapi import FastAPI

app = FastAPI()

# ELEMENTS
@app.get("/elements/total")
def read_total_elements():
    return {"value": 120}

@app.get("/elements/last_added")
def read_last_added_element():
    return {"last_added_element": {
        "uuid": "123e4567-e89b-12d3-a456-426614174000",
        "part_name": "Resistor 10kΩ",
    }}

# TABLES
@app.get("/tables/total")
def read_total_tables():
    return {"value": 15}

@app.get("/tables/amounts")
def read_tables_amounts():
    return {
        "Resistors": 50,
        "Capacitors": 30,
        "Inductors": 20
    }

# MANUFACTURERS
@app.get("/manufacturers/total")
def read_total_manufacturers():
    return {"value": 10}

@app.get("/manufacturers/amounts")
def read_manufacturers_amounts():
    return {
        "Texas Instruments": 15,
        "STMicroelectronics": 12,
        "Infineon": 8
    }

# SUPPLIERS
@app.get("/suppliers/total")
def read_total_suppliers():
    return {"value": 8}

@app.get("/suppliers/amounts")
def read_suppliers_amounts():
    return {
        "Digi-Key": 20,
        "Mouser": 18,
        "Arrow": 10
    }

# REPOSITORY
@app.get("/repository/total")
def read_total_schlib():
    return {"total_footprints": 200, "total_symbols": 150, "total_pcblibs": 100, "total_schlibs": 250}











