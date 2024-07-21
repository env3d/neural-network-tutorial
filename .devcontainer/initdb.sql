CREATE DATABASE train;
\c train;
CREATE TABLE IF NOT EXISTS training_data ( 
    id serial primary key,
    timestamp timestamptz default current_timestamp,
    data JSONB);