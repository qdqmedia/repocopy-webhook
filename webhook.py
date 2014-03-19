#!/usr/bin/python -tt

import sys
import argparse
import json
import logging
import logging.handlers
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


WEBHOOK_NAME = 'untitled'  # Please give your webhook a name


class Webhook(BaseHTTPRequestHandler):

    def do_POST(self):
        """
        Handle POST data
        """

        message = 'OK'
        self.rfile._sock.settimeout(5)
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.send_header("Content-type", "text")
        self.send_header("Content-length", str(len(message)))
        self.end_headers()
        self.wfile.write(message)

        # parse data
        data = json.loads(data_string)

        # Process here sent data
        print data

    def log_message(self, formate, *args):
        """
        Disable printing to stdout/stderr for every post
        """
        return


if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser(description='{} Webhook'.format(WEBHOOK_NAME))

    # Prepare settings
    default_port = 8000  # Webhook server port
    default_log_max_size = 50 * 1048576  # 50 MB
    default_log_level = logging.INFO
    default_backup_count = 4  # Number of historical data logs

    parser.add_argument('-l', '--log', help='Specify a log file otherwise stdout will be used', required=False)

    args = parser.parse_args()

    log = logging.getLogger('webhook_log')
    log.setLevel(args.log_level)
    if args.log:
        log_handler = logging.handlers.RotatingFileHandler(args.log_file,
                                                           maxBytes=args.log_max_size,
                                                           backupCount=args.backup_count)
    else:
        log_handler = logging.StreamHandler(sys.stdout)
    f = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(message)s",
                          "%B %d %H:%M:%S")
    log_handler.setFormatter(f)
    log.addHandler(log_handler)

    # Launch server
    try:
        server = HTTPServer(('', args.server_port), Webhook)
        log.info('Starting webhook server ({})...'.format(WEBHOOK_NAME))
        server.serve_forever()
    except KeyboardInterrupt:
        log.info('CTRL-C pressed, closing webhook...')
        server.socket.close()
