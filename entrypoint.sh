#!/bin/sh

CSV_FILE=${DATA_FILE:-/data/seed.csv}

if [[ -f $CSV_FILE && $HOST != "" ]]; then
    locust --host ${HOST:-http://localhost:8000} --wait-time 5 --users ${WORKERS:-1} --data $CSV_FILE
fi

echo host=$HOST, data=$CSV_FILE
# sleep instead of exit so that container continues to run
/bin/sleep 10000
