FROM hypriot/rpi-influxdb
MAINTAINER Ryan Creasey <ryan@infern.al>

ENV ADMIN_USER admin
ENV INFLUXDB_INIT_PWD speedtest
ENV PRE_CREATE_DB speedtest

COPY influxdb.conf /etc/influxdb/influxdb.conf

EXPOSE 8083
EXPOSE 8086

VOLUME ["/data"]
