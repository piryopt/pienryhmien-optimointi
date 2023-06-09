#!/bin/bash

export DATABASE_URL="postgresql://localhost:/piryopt?user=postgres&password=local_test"

pip3 install --no-cache-dir -r requirements.txt

python3 -m flask run
