#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains poodle fix.

Synopsis
    This module fix the following error:
        <urlopen error [Errno 1] _ssl.c:491: error:14077410:SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake failure>

Description
    Python 2.6's urllib2 does not allow you to select the TLS dialect,
    and by default uses a SSLv23 compatibility negotiation implementation.
    The implementation doesn't work correctly, failing to connect to servers
    that respond only to TLS1.0+. This module help set up TLS support for
    urllib2.

Credit
    https://gist.github.com/flandr/74be22d1c3d7c1dfefdd
"""

import urllib2
import httplib
import ssl
import socket
import sdconfig

class TLS1Connection(httplib.HTTPSConnection):
    def __init__(self, host, **kwargs):
        httplib.HTTPSConnection.__init__(self, host, **kwargs)

    def connect(self):
        """Overrides HTTPSConnection.connect to specify TLS version."""

        sock = socket.create_connection((self.host, self.port), self.timeout)

        if getattr(self, '_tunnel_host', None):
            self.sock = sock
            self._tunnel()

        # This is the only difference (default wrap_socket uses SSLv23).
        self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)

class TLS1Handler(urllib2.HTTPSHandler):
    def __init__(self):
        urllib2.HTTPSHandler.__init__(self)

    def https_open(self, req):
        return self.do_open(TLS1Connection, req)

def _enable():
    urllib2.install_opener(urllib2.build_opener(TLS1Handler())) # Override default handler

def _disable():
    urllib2.install_opener(urllib2.build_opener()) # Restore default handler

def start(url):
    if sdconfig.poddlefix:
        if 'https' in url:
            _enable()

def stop():
    if sdconfig.poddlefix:
        _disable()
