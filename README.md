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
For the creation of the table we need type the below query:
```
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE "Components" (
    uuid VARCHAR(36) PRIMARY KEY DEFAULT (uuid_generate_v4()),
    part_name VARCHAR NOT NULL UNIQUE,
    manufacturer VARCHAR NOT NULL,
    description VARCHAR,
    library_ref VARCHAR NOT NULL UNIQUE,
    library_path VARCHAR NOT NULL UNIQUE,
    footprint_ref_1 VARCHAR NOT NULL UNIQUE,
    footprint_path_1 VARCHAR NOT NULL UNIQUE,
    footprint_ref_2 VARCHAR NOT NULL UNIQUE,
    footprint_path_2 VARCHAR NOT NULL UNIQUE,
    footprint_ref_3 VARCHAR NOT NULL UNIQUE,
    footprint_path_3 VARCHAR NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_edited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
For the generate test data in the created table we need to type the below query
```
INSERT INTO "Components" (
    uuid, part_name, manufacturer, description, 
    library_ref, library_path, 
    footprint_ref_1, footprint_path_1, 
    footprint_ref_2, footprint_path_2, 
    footprint_ref_3, footprint_path_3
)
SELECT 
    gen_random_uuid(),
    'Part_' || (seq + 1000),
    CASE (seq % 5) 
        WHEN 0 THEN 'Texas Instruments'
        WHEN 1 THEN 'STMicroelectronics'
        WHEN 2 THEN 'Infineon'
        WHEN 3 THEN 'NXP Semiconductors'
        WHEN 4 THEN 'Analog Devices'
    END,
    CASE (seq % 4)
        WHEN 0 THEN 'High-performance microcontroller'
        WHEN 1 THEN 'Power management IC'
        WHEN 2 THEN 'Voltage regulator'
        WHEN 3 THEN 'Digital signal processor'
    END,
    'LibRef_' || (seq + 2000),
    '/libraries/components/lib_' || (seq + 2000) || '.lib',
    'FootprintRef_' || (seq + 3000) || '_1',
    '/footprints/smd/fp_' || (seq + 3000) || '_1.pretty',
    'FootprintRef_' || (seq + 4000) || '_2', 
    '/footprints/tht/fp_' || (seq + 4000) || '_2.pretty',
    'FootprintRef_' || (seq + 5000) || '_3',
    '/footprints/bga/fp_' || (seq + 5000) || '_3.pretty'
FROM generate_series(0, 1000) AS seq;
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