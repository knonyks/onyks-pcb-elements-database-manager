#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    
    CREATE SCHEMA IF NOT EXISTS private;

    CREATE EXTENSION IF NOT EXISTS pgcrypto;
    
    DO \$body\$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_rank') THEN
            CREATE TYPE user_rank AS ENUM ('admin', 'editor', 'viewer', 'server');
        END IF;
    END
    \$body\$;

    CREATE TABLE IF NOT EXISTS private.users(
        id SERIAL PRIMARY KEY,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        expiration_time TIMESTAMP DEFAULT '1970-01-01 00:00:00',
        rank user_rank NOT NULL DEFAULT 'viewer'
    );

    CREATE TABLE IF NOT EXISTS private.manufacturers(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS private.suppliers(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS private.tables(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );


    CREATE TABLE IF NOT EXISTS private.elements(
        uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        part_name VARCHAR(256) NOT NULL,
        
        table_name VARCHAR(256) NOT NULL,
        CONSTRAINT fk_table
            FOREIGN KEY (table_name) 
            REFERENCES private.tables (name)
            ON DELETE RESTRICT,

        description VARCHAR(256) NOT NULL,
        
        manufacturer VARCHAR(256),
        CONSTRAINT fk_manufacturer
            FOREIGN KEY (manufacturer) 
            REFERENCES private.manufacturers (name)
            ON DELETE SET NULL,

        value VARCHAR(256)
        availability VARCHAR(256)
        suppliers_names JSONB
        library_ref VARCHAR(256)
        library_path VARCHAR(256)
        footprint_ref_1 VARCHAR(256)
        footprint_path_1 VARCHAR(256)
        footprint_ref_2 VARCHAR(256)
        footprint_path_2 VARCHAR(256)
        footprint_ref_3 VARCHAR(256)
        footprint_path_3 VARCHAR(256)
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );

    INSERT INTO private.users (login, password, email, rank)
    VALUES ('${SVN_SERVER_USER}', crypt('${SVN_SERVER_PASSWORD}', gen_salt('bf')), '${SVN_SERVER_EMAIL}', 'server');
EOSQL