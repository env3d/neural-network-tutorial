CREATE DATABASE IF NOT EXISTS train;
CREATE TABLE IF NOT EXISTS training_data ( 
    id serial primary key,
    timestamp timestamptz default current_timestamp,
    data JSONB);