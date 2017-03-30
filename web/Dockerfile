FROM grafana/grafana:4.1.1
MAINTAINER Ryan Creasey <ryan@infern.al>

ENV GF_SERVER_ROOT http://localhost
ENV GF_AUTH_ANONYMOUS_ENABLED true

COPY grafana.db /var/lib/grafana/grafana.db
COPY home.json /usr/share/grafana/public/dashboards/home.json
