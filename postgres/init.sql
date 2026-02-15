CREATE SCHEMA IF NOT EXISTS private;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'user_rank') THEN
        CREATE TYPE user_rank AS ENUM ('admin', 'editor', 'user');
    END IF;
END
$$;

CREATE TABLE IF NOT EXISTS private.users (
    id SERIAL PRIMARY KEY,
    login TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    expiration_time TIMESTAMP DEFAULT '1970-01-01 00:00:00',
    rank user_rank NOT NULL DEFAULT 'user'
);