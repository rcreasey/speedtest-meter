FROM python:alpine

RUN pip install influxdb speedtest-cli

ENV TEST_INTERVAL 300

WORKDIR /app
COPY fast.com/fast_com.py .
COPY probe.py .
COPY probe.sh .

RUN chmod +x /app/probe.sh

CMD ["sh", "/app/probe.sh"]