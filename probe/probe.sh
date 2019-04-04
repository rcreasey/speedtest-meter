#!/bin/bash

while true
do
    python probe.py -s
    sleep $TEST_INTERVAL
done
