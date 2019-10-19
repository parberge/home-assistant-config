#!/usr/bin/env python3
import sys
import socket
import logging

log = logging.getLogger(__name__)

class PS4:
    #DDP_VERSION = '00010010'
    ddp_version = '00020020'
    port = 987

    def __init__(self, host):
        self.host = host
        self.state = None
        self.latest_response = ''
    
    def __repr__(self):
        return '{}@{}:{}'.format(self.__class__.__name__, self.host, self.port)

    def is_reachable(self):
        up = bool(self.query_ps4())
        log.debug('%s is_reachable: %s', self, up)
        return up

    def is_active(self):
        if not self.is_reachable():
            self.state = False
            return False
        res = '200 Ok' in self.latest_response
        self.state = res
        log.debug('%s is_active: %s', self, res)
        return res

    def query_ps4(self):
        """
        Send a special HTTP request over UDP(!)
        Response should be something like "HTTP/1.1 620 Server Standby" or
        "HTTP/1.1 200 Ok"
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(1)
        msg = (
            'SRCH * HTTP/1.1\n'
            'device-discovery-protocol-version:{}'.format(
                self.ddp_version
            )
        )
        try:
            log.debug('Sending:\n%s', msg)
            s.sendto(bytes(msg, 'utf-8'), (self.host, self.port))
        except socket.error as e:
            log.error(e)
            return False

        try:
            res_msg = s.recv(1024)
        except socket.timeout:
            log.warning('Timeout waiting for response from ps4')
            # Probably in transition between standby and on or vice versa
            res_msg = ''
        s.close()
        self.latest_response = str(res_msg)
        return self.latest_response


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('{} <host/IP of PS4>'.format(__file__))
        sys.exit(1)
    host = sys.argv[1]
    
    ps4 = PS4(host)
    
    if ps4.is_active():
        print('ON')
    else:
        print('OFF')

