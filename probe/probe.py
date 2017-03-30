import influxdb
import logging
import os
import socket
import speedtest
import sys

log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

probe = speedtest.Speedtest()
probe.get_best_server()

if not probe.results.server:
    log.error('Unable to select best server from Speedtest.net; Aborting')
    sys.exit(1)
else:
    log.info("{0}: {1}".format(probe.results.server.get('sponsor'), probe.results.server.get('name')))

probe.download()
probe.upload()

download_in_mbs = probe.results.download / 1000000
upload_in_mbs = probe.results.upload / 1000000
hostname = os.environ.get('HOSTNAME', socket.gethostname())

log.info("Host: {host}, Download: {down:.2f} Mb/s, Upload: {up:.2f} Mb/s".format(host=hostname,
                                                                                 down=download_in_mbs,
                                                                                 up=upload_in_mbs))

try:
    db = influxdb.InfluxDBClient('db', 8086, 'admin', 'speedtest', 'speedtest')
except influxdb.exceptions.InfluxDBServerError as e:
    log.error("DB is offline; results not saved.")
    sys.exit(1)

db.create_database('speedtest')
db.write_points([{'measurement': 'download', 'fields': {'host': hostname, 'value': download_in_mbs}},
                 {'measurement': 'upload', 'fields': {'host': hostname, 'value': upload_in_mbs}}])

log.info("-" * 25)
