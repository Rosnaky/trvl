#! /bin/bash

source env.sh

docker compose up -d
  
python ./api/run.py
