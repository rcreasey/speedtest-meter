FROM ubuntu:trusty
MAINTAINER Ryan Creasey <ryan@infern.al>

RUN apt-get update && apt-get install -y curl python python-pip
RUN mkdir /app

WORKDIR /app

RUN pip install influxdb speedtest-cli fastdotcom

COPY fast_com.py /app/fast_com.py
COPY probe.py /app/probe.py
COPY probe.sh /app/probe.sh

RUN chmod +x /app/probe.sh
CMD bash -c /app/probe.sh 

ENV TEST_INTERVAL 5
