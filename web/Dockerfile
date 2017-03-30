FROM fg2it/grafana-armhf:v4.1.1

ENV GF_SERVER_ROOT http://localhost
ENV GF_AUTH_ANONYMOUS_ENABLED true

COPY grafana.db /var/lib/grafana/grafana.db
COPY home.json /usr/share/grafana/public/dashboards/home.json
