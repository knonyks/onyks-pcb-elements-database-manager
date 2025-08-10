# Onyks PCB Elements Database Manager

A web app designed for managing PCB components (mainly for Altium Designer) with database and SVN repository.

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
python run.py
```

Before running we need to set up a config file - config.json. It have to be filled by our input data for database and also for a SVN repository.

### Config file

Soon.

### Database

### PostgreSQL query for components data
```
CREATE TABLE Components (
    uuid TEXT PRIMARY KEY,
    part_name TEXT,
	created_at TIMESTAMPTZ DEFAULT NOW(),
    edited_at TIMESTAMPTZ DEFAULT NOW(),
);
```

### What do they all mean?
```
uuid - universally unique identifier for every compontent,
part_name - a manufacturer name of the compontent,
created_at - a date when the component was created,
edited_at - a date when the last time the component was edited
```


<!-- 

# Altium Designer Library ONYKS

A simple web-frontend for managing components in Altium Designer.  This is for you if you use database libraries, or SVNDBlib files, which use an external database to manage library components.

## Environment setup

Python requirement : 
- version 3.11 only
- pip install -r requirements.txt #this works better in pip < 10.0
- install **psqlodbc_x64.msi**
- database backend supported by SQLAlchemy
- SVN server (Visual SVN)
- SQL software (Postgres)

## Database requirements
The database can contain anything you want. The original author uses reflection to see what's in each table. Nonetheless the database MUST include certain fields, including at least the following:

    - uuid (must be the primary key)
    - part_name     #unique part number,tylko 
    - part_value    #=part_name jesli scalak a 100K jesli opornik/kondensator, =comment w altiumie
    - kategoria # ic,res,cap
    - description #  krótki opis
    - symbol_ref    #  wiadomo
    - footprint_ref # wiadomo
    - availability  #  duzo,malo brak
    - distributor_link   # link do lcsc,tme, mouser, cokolwiek
    - datasheet_ref # sciezka do pdfa na serwerze -->



<!-- # Altium Designer Library

A simple web-frontend for managing components in Altium Designer.  This is for you if you use database libraries, or SVNDBlib files, which use an external database to manage library components.

## Dependencies

   - pip install -r requirements.txt #this works better in pip < 10.0
    - A database backend supported by SQLAlchemy.
    - An SVN server, filled with your symbols and footprints
    
## Database requirements
The database can contain anything you want. The original author uses reflection to see what's in each table. Nonetheless the database MUST include certain fields, including at least the following:

    - uuid (must be the primary key)
    - part_name     #unique part number,tylko 
    - part_value    #=part_name jesli scalak a 100K jesli opornik/kondensator, =comment w altiumie
    - kategoria # ic,res,cap
    - description #  krótki opis
    - symbol_ref    #  wiadomo
    - footprint_ref # wiadomo
    - availability  #  duzo,malo brak
    - distributor_link   # link do lcsc,tme, mouser, cokolwiek
    - datasheet_ref # sciezka do pdfa na serwerze


r_0603_100K
ic_adc123

RES_0603


Both uuid and id will not be shown in any of the displays. You'll never know they're there. But if uuid is not the primary key, almost nothing will work right. Particularly the copy part/edit part features.
    
If you use a sqlite database, the process must have rw access to it. I usually chmod 644 it. If you put it in the altium directory, you can refer to it as sqlite:///database.sqlite, however there are probably lots of reasons to avoid doing this. In particular only one write at a time is supported by sqlite, so if you have a lot of users that's a bad idea.

## Running

    python3 main.py

## Credits

Thanks to Ryan Sturmer who wrote the original application.

Thanks to Michael Fogleman of http://michaelfogleman.com who developed the HelloFlask starting point from which this application is derived.
## COnnecting to database
### IF NO .DBLIB FILE
Install psqlodbc.msi_x64
Open ODBC Data Sources (64-bit) in Windows
Add...
PostgreSQL Unicode(x64)
![alt text](image.png)
instead of localhost, use the IP address of the server
Test connection
save
ok

Open altium designer
New > Library... > Database > Database Library
Create
Select Use Connection String
Paste this:
Provider=MSDASQL.1;Persist Security Info=False;User ID=postgres;Data Source=PostgreSQL35W;Initial Catalog=altium_lib;Option=2;
Advanced...
Put " in Left Quote Character 
and " in Right Quote Character
Click OK
Connect 
everything should be ok
### THEN
Open library preferences
Install
select .DbLib file
ok -->
