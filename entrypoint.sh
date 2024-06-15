#!/bin/sh

locust --host ${HOST:-http://localhost:8000} --wait-time 5 --users ${WORKERS:-1}
