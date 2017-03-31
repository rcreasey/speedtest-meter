#!/bin/bash

while true
do
    python probe.py -f
    sleep $TEST_INTERVAL
done
