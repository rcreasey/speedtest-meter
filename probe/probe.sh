#!/bin/bash

while true
do
    python probe.py
    sleep $TEST_INTERVAL
done
