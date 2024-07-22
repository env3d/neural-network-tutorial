#!/bin/bash

jupyter notebook --ip=0.0.0.0 --allow-root  --no-browser --IdentityProvider.token='' --ServerApp.password='' &
gunicorn --bind 0.0.0.0:5000 app:app 
