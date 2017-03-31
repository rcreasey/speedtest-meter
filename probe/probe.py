import influxdb
import logging
import os
import optparse
import socket
import sys

log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)


def speedtest(hostname):
    import speedtest

    download = 0.0
    upload = 0.0

    try:

        probe = speedtest.Speedtest()
        probe.get_best_server()

        if not probe.results.server:
            log.error('Unable to select best server from Speedtest.net; Aborting')
        else:
            log.info('{0}: {1}'.format(probe.results.server.get('sponsor'), probe.results.server.get('name')))

        probe.download()
        probe.upload()

        download = probe.results.download / 1000000
        upload = probe.results.upload / 1000000

    except:
        log.error('Unable to gather results from Speedtest.net')

    log.info('Host: {host}, Download: {down:.2f} Mb/s, Upload: {up:.2f} Mb/s'.format(host=hostname, down=down, up=up))

    return [{'measurement': 'download', 'fields': {'host': hostname, 'value': down}},
            {'measurement': 'upload', 'fields': {'host': hostname, 'value': up}}]


def fastdotcom(hostname):
    import fast_com

    download = 0.0

    try:
        download = fast_com.fast_com(maxtime=10)
    except:
        log.error('Unable to gather results from Fast.com')

    log.info('Host: {host}, Download: {down:.2f} Mb/s'.format(host=hostname, down=down))

    return [{'measurement': 'download', 'fields': {'host': hostname, 'value': down}}]


def main():
    parser = optparse.OptionParser(usage='usage: %prog [options]')
    parser.add_option('-s', '--speedtest', action='store_true', dest='speedtest', default=False,
                      help='Use speedtest.net to gather metrics (default)')
    parser.add_option('-f', '--fastdotcom', action='store_true', dest='fastdotcom', default=False,
                      help='Use fast.com to gather metrics (instead of speedtest)')

    (options, args) = parser.parse_args()

    if not options.speedtest and not options.fastdotcom:
        options.speedtest = True

    hostname = os.environ.get('HOSTNAME', socket.gethostname())

    if options.speedtest:
        data = speedtest(hostname)
    elif options.fastdotcom:
        data = fastdotcom(hostname)

    try:
        db = influxdb.InfluxDBClient('db', 8086, 'admin', 'speedtest', 'speedtest')
    except influxdb.exceptions.InfluxDBServerError as e:
        log.error('DB is offline; results not saved.')
        sys.exit(1)

    db.create_database('speedtest')
    db.write_points(data)

    log.info('-' * 25)


if __name__ == '__main__':
    main()
