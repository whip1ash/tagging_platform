#!/usr/bin/env bash

python3 manage.py makemigrations
python3 manage.py makemigrations normal entity relation
python3 manage.py migrate