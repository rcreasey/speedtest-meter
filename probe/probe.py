import speedtest
import influxdb
import sys
import socket

probe = speedtest.Speedtest()

probe.get_best_server()

if not probe.results.server:
    sys.exit(1)
    
print("{0}: {1}".format(probe.results.server.get('sponsor'), probe.results.server.get('name')))

probe.download()
probe.upload()

db = influxdb.InfluxDBClient('db', 8086, 'admin', 'speedtest', 'speedtest')
db.create_database('speedtest')

download_in_mbs = probe.results.download / 1000000
upload_in_mbs = probe.results.upload / 1000000
hostname = socket.gethostname()

db.write_points([{'measurement': 'download', 'fields': {'host': hostname, 'value': download_in_mbs}},
                 {'measurement': 'upload', 'fields': {'host': hostname, 'value': upload_in_mbs}}])

print("Download: {0:.2f} Mb, Upload: {0:.2f}".format(download_in_mbs, upload_in_mbs))
print("-" * 25)
