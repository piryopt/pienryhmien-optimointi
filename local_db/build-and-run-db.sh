#!/bin/bash

cp ../../schema.sql schema.sql

docker build . -t postgres

docker run -it -p 5432:5432 postgres
