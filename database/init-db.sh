#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    
    CREATE SCHEMA IF NOT EXISTS private;

    CREATE EXTENSION IF NOT EXISTS pgcrypto;
    
    -- TUTAJ MUSZĄ BYĆ BACKSLASHE PRZED DOLARAMI POSTGRESA
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

    -- TWOJE ZMIENNE Z DOCKERA (bez backslashy, bo to zmienne z .env)
    INSERT INTO private.users (login, password, email, rank)
    VALUES ('${SVN_SERVER_USER}', crypt('${SVN_SERVER_PASSWORD}', gen_salt('bf')), '${SVN_SERVER_EMAIL}', 'server');
EOSQL