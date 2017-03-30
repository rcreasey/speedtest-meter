FROM ubuntu:trusty
MAINTAINER Ryan Creasey <ryan@infern.al>

RUN apt-get update && apt-get install -y curl python python-pip
RUN mkdir /app

WORKDIR /app

RUN curl -O https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py
RUN pip install influxdb

COPY probe.py /app/probe.py
COPY probe.sh /app/probe.sh

RUN chmod +x /app/probe.sh
CMD bash -c /app/probe.sh 
