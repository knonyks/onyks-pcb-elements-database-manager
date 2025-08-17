# Onyks PCB Elements Database Manager

A Web browser designed to manage multiple PCB schematics and footprints. 
Altium Designer SchLib (Schematic Library) and PcbLib (Footprints Library) are also compatible with KiCad. 

Web browser library informations are stored in database while SchLib and PcbLib are stored in SVN repository.

### Requirements
- Python 3.11
- installed postgreSQL: psqlodbc_x64.msi

### How to install and run

#### Example for Windows 11
```
cd server
python3.11 -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
#with default config config.json
python run.py
#with a custom config, for example: my_config.json
python run.py --config=my_config.json
```

Before running we need to set up a config file - config.json. It have to be filled by our input data for database and also for a SVN repository.

### Config file

Soon.

### Database

### PostgreSQL query for components data
```
CREATE TABLE "Components" (
    uuid VARCHAR PRIMARY KEY,
    part_name VARCHAR NOT NULL UNIQUE,
    category VARCHAR NOT NULL,
    value VARCHAR NOT NULL,
    description VARCHAR,
    available VARCHAR DEFAULT 'true',
    atributes VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    edited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indekses added in the model (index=True)
CREATE INDEX ix_Components_part_name ON "Components" (part_name);
CREATE INDEX ix_Components_category ON "Components" (category);
```

### What do they all mean?
```
uuid - universally unique identifier for every compontent,
part_name - a manufacturer name of the compontent,
category - a component type (Capacitor, Resistor etc.),
value - a component value (10uF, 10mH etc.),
description - essential basic information about the component,
available - availability of the component on the market,
atributes - link to the manufacturer datasheet,
created_at - a date when the component was created,
edited_at - a date when the last time the component was edited
```