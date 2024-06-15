#!/bin/sh

locust --host $TARGET_URL --wait-time 5 --users ${WORKERS:-1}
