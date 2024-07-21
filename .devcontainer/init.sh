#!/bin/bash

pip install tensorflow tensorflowjs keras flask psycopg[binary] gunicorn
psql -h localhost -f ./.devcontainer/initdb.sql postgres admin 