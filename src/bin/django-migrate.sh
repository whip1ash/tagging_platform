#!/usr/bin/env bash

python3 manage.py makemigrations
python3 manage.py makemigrations normal entity realtion
python3 manage.py migrate