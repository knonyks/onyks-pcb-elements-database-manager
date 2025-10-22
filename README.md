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

### Config file description

Soon.

### Database

### PostgreSQL query for components data
For the creation of the table we need type the below query:
```
DO $$
DECLARE
    tbl_name TEXT;
    names TEXT[] := ARRAY[
            'Resistors', 
            'Capacitors', 
            'Inductors', 
            'ICs', 
            'Connectors',
            'Mechanical', 
            'Batteries', 
            'Diodes', 
            'Antennas', 
            'Modules'];
BEGIN
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    FOREACH tbl_name IN ARRAY names
    LOOP
        EXECUTE format(
            'CREATE TABLE IF NOT EXISTS %I (
                uuid VARCHAR(36) PRIMARY KEY DEFAULT uuid_generate_v4(),
                part_name VARCHAR NOT NULL,
                manufacturer VARCHAR,
                manufacturer_part_name VARCHAR,
                datasheet VARCHAR,
                description VARCHAR,
                value VARCHAR,
                availability VARCHAR,
                library_ref VARCHAR,
                library_path VARCHAR,
                footprint_ref_1 VARCHAR,
                footprint_path_1 VARCHAR,
                footprint_ref_2 VARCHAR,
                footprint_path_2 VARCHAR,
                footprint_ref_3 VARCHAR,
                footprint_path_3 VARCHAR,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );',
            tbl_name
        );
    END LOOP;
END $$;
```
For the generate test data in the created table we need to type the below query
```
DO $$
DECLARE
    tbl_name TEXT;
    names TEXT[] := ARRAY[
            'Resistors', 
            'Capacitors', 
            'Inductors', 
            'ICs', 
            'Connectors',
            'Mechanical', 
            'Batteries', 
            'Diodes', 
            'Antennas', 
            'Modules'];
    n_rows INT;
BEGIN
    FOREACH tbl_name IN ARRAY names
    LOOP

        n_rows := floor(random() * (1000 - 200 + 1) + 200)::INT;

        EXECUTE format($f$
            INSERT INTO %I (
                uuid, part_name, manufacturer, description, 
                library_ref, library_path, 
                footprint_ref_1, footprint_path_1, 
                footprint_ref_2, footprint_path_2, 
                footprint_ref_3, footprint_path_3
            )
            SELECT 
                gen_random_uuid(),
                'Part_' || (seq + 1000),
                CASE (seq %% 5) 
                    WHEN 0 THEN 'Texas Instruments'
                    WHEN 1 THEN 'STMicroelectronics'
                    WHEN 2 THEN 'Infineon'
                    WHEN 3 THEN 'NXP Semiconductors'
                    WHEN 4 THEN 'Analog Devices'
                END,
                CASE (seq %% 4)
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
            FROM generate_series(0, %s) AS seq;
        $f$, tbl_name, n_rows);
    END LOOP;
END $$;
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


```
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    family_name VARCHAR(80) NOT NULL,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO Users (name, family_name, username, email, password, is_admin)
VALUES ('Jan', 'Kowalski', 'admin', 'jan@example.com',
        '$2b$12$w6Qq.8zs9Go3LLtwwMgN6epxegZMnwtVC3/V/r59QyXh0wlU/j.0S',
            TRUE);

INSERT INTO Users (name, family_name, username, email, password, is_admin)
VALUES ('Zbyszek', 'Władywostok', 'user', 'zbyszek@example.com',
        '$2b$12$/Dpf4Rf/Ub992SaHYcD5VuBnjdn315i5c5ChLpDal0vZAR5hAGfMu',
            FALSE);
```





## Production server - instruction

### Gunicorn instruction
Assumption: Python 3.11 and systemd.

Tested on Ubuntu 24.04

1. Download the repository

2. Next, go to a directory ```server``` and create there a python environment: 

```
cd server
python -m venv .venv
```

3. Activate the python environment and install require packages:

```
source ./.venv/bin/activate
python3 -m pip install -r requirements.txt
```

4. If our python environment is ready, we can start creating the system service: 

```sudo nano /etc/systemd/system/onyks_pcb_element_database_manager_server.service```

5. We need to fill the system service file for our server like below:

```
[Unit]
Description=Onyks PCB Elements Database Manager
After=network.target

[Service]
User=user
Group=user
WorkingDirectory=/home/user/onyks-pcb-elements-database-manager/server
Environment="PATH=/home/user/onyks-pcb-elements-database-manager/server/.venv:/bin/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="FLASK_ENV=production"
Environment="ONYKS_CONFIG=my_config.json"
ExecStart=/home/user/onyks-pcb-elements-database-manager/server/.venv/bin/gunicorn -k eventlet -w 1 wsgi:app  --bind 127.0.0.1:5000
Restart=always
RestartSec=5s
StandardOutput=append:/var/log/onyks_pcb_element_database_manager_server.out.log
StandardError=append:/var/log/onyks_pcb_element_database_manager_server.err.log
SyslogIdentifier=onyks_pcb_element_database_manager_server

[Install]
WantedBy=multi-user.target
```

We need to adjust these lines to our machine:
* ```User=*``` - the user of the service;
* ```Group=*``` - the group of the user which we entered in ```User`` field;
* ```WorkingDirectory=*``` - the absolute path to the folder ```server```;
* ```Environment="PATH=*"``` - the line which contains absolute paths to bins where the service can get installed system packages and also our python environment;
* ```Environment="ONYKS_CONFIG=*"``` - a relative path to the config which we want to use; it's the relative path from ```server``` directory (where we created the ```.venv```);
* ```ExecStart=*``` - it contains the command which starts the server - it has to be filled with an absolute path to the gunicorn from ```.venv``` in folder ```server```;

6. Reload systemd: ```sudo systemctl daemon-reload```
7. Run the service: ```sudo systemctl start onyks_pcb_element_database_manager_server```
8. If we want to start the service everytime when the system turn on we need to type: ```sudo systemctl enable onyks_pcb_element_database_manager_server```
9. If we want to check the status of the service we need to type: ```sudo systemctl status onyks_pcb_element_database_manager_server```
10. To watch live the logs: ```journalctl -u onyks_pcb_element_database_manager_server -f```

### Nginx

Soon.

### WSGI

Soon.



```sudo nano /etc/systemd/system/onyks_pcb_element_database_manager_repository_worker.service```



```
[Unit]
Description=Onyks PCB Elements Database Manager Repository Worker
After=network.target

[Service]
User=zero-jedynkowy
Group=zero-jedynkowy
WorkingDirectory=/home/zero-jedynkowy/onyks-pcb-elements-database-manager/server
Environment="PATH=/home/zero-jedynkowy/onyks-pcb-elements-database-manager/server/.venv:/bin/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="FLASK_ENV=production"
Environment="ONYKS_CONFIG=my_config.json"
ExecStart=/home/zero-jedynkowy/onyks-pcb-elements-database-manager/server/.venv/bin/python repository_worker.py --config=$ONYKS_CONFIG
Restart=always
RestartSec=5s
StandardOutput=append:/var/log/onyks_pcb_element_database_manager_repository_worker.out.log
StandardError=append:/var/log/onyks_pcb_element_database_manager_repository_worker.err.log
SyslogIdentifier=onyks_pcb_element_database_manager_repository_worker

[Install]
WantedBy=multi-user.target
```