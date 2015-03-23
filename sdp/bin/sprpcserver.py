#!/usr/bin/env python
# coding: utf-8

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sprpcserver.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12609 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

# Basic Auth code is from 
# http://code.google.com/p/pywebdav/source/browse/pywebdav/lib/AuthServer.py?r=50bf53a2c5041ea344890e21eec9e86b2786c7a3

import signal
import base64
import binascii
import splog
import spconfig
import pyjsonrpc
import BaseHTTPServer
import ssl
from spppnetapi import PostProcessingNetAPI

class AuthRequestHandler(PostProcessingNetAPI,pyjsonrpc.HttpRequestHandler):
    """
    Simple handler that can check for auth headers
    """

    DEFAULT_AUTH_ERROR_MESSAGE = """<head> <title>%(code)s - %(message)s</title> </head> <body> <h1>Authorization Required</h1> this server could not verify that you are authorized to access the document requested.  Either you supplied the wrong credentials (e.g., bad password), or your browser doesn't understand how to supply the credentials required.  </body> """
    DO_AUTH = True # False means no authentication

    def parse_request(self):
        if not BaseHTTPServer.BaseHTTPRequestHandler.parse_request(self):
            return False

        if self.DO_AUTH:
            authorization = self.headers.get('Authorization', '')
            if not authorization:
                self.send_autherror(401, "Authorization Required")
                return False
            scheme, credentials = authorization.split()
            if scheme != 'Basic':
                self.send_error(501)
                return False
            credentials = base64.decodestring(credentials)
            username, password = credentials.split(':', 2)
            if not self.get_userinfo(username, password, self.command):
                self.send_autherror(401, "Authorization Required")
                return False

        return True

    def send_autherror(self, code, message=None):
        """Send and log an auth error reply.

        Arguments are the error code, and a detailed message.
        The detailed message defaults to the short entry matching the
        response code.

        This sends an error response (so it must be called before any
        output has been generated), logs the error, and finally sends
        a piece of HTML explaining the error to the user.

        """
        try:
            short, long = self.responses[code]
        except KeyError:
            short, long = '???', '???'
        if message is None:
            message = short
        explain = long
        self.log_error("code %d, message %s", code, message)

        # using _quote_html to prevent Cross Site Scripting attacks (see bug #1100201)
        content = (self.DEFAULT_AUTH_ERROR_MESSAGE % {'code': code, 'message': self._quote_html(message), 'explain': explain})

        self.send_response(code, message)
        self.send_header('Content-Type', self.error_content_type)
        self.send_header('WWW-Authenticate', 'Basic realm="PyWebDAV"')
        self.send_header('Connection', 'close')
        self.end_headers()
        self.wfile.write(content)

    def _quote_html(self,html):
        return html.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def get_userinfo(self, username, password, command):
        """Checks if allowed to access.

        Return 1 or None depending on whether the password was
        ok or not. None means not authorized.
        """

        assert _password!='foobar'

        if username==_username and password==_password:
            return 1
        else:
            return None

def start():
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        splog.info('SPRPCSRV-001','http_server.serve_forever stopped by KeyboardInterrupt')
        http_server.shutdown()
    except SystemExit:
        splog.info('SPRPCSRV-002','http_server.serve_forever stopped by SystemExit')
        http_server.shutdown()

# init.

_port=spconfig.config.getint('daemon','port')
_host=spconfig.config.get('daemon','host')
_username=spconfig.config.get('rpcserver','username')
_password=spconfig.config.get('rpcserver','password')

http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = (_host, _port),
    RequestHandlerClass = AuthRequestHandler
)

# add a ssl wrapper
#   - This code use an ssl tricks from http://www.piware.de/2011/01/creating-an-https-server-in-python
#   - The certificate was created with this command: openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
http_server.socket = ssl.wrap_socket (http_server.socket, certfile=spconfig.certificate_file, server_side=True)

# start the server
if __name__=="__main__":

    # Code below is only used in standalone mode (i.e. not when used inside 'spdaemon')
    def terminate(signum, stackframe):
        print 'Stopping HTTP server ...'
        raise SystemExit()
    signal.signal(signal.SIGINT, terminate)
    signal.signal(signal.SIGTERM, terminate)


    start()

# TODO
#
#To handle server shutdown, this way seems better:
#
# <--
#import SimpleHTTPServer, BaseHTTPServer, httplib
#
#class StoppableHttpRequestHandler (SimpleHTTPServer.SimpleHTTPRequestHandler):
#    """http request handler with QUIT stopping the server"""
#
#    def do_QUIT (self):
#        """send 200 OK response, and set server.stop to True"""
#        self.send_response(200)
#        self.end_headers()
#        self.server.stop = True
#
#
#class StoppableHttpServer (BaseHTTPServer.HTTPServer):
#    """http server that reacts to self.stop flag"""
#
#    def serve_forever (self):
#        """Handle one request at a time until stopped."""
#        self.stop = False
#        while not self.stop:
#            self.handle_request()
#
#def stop_server (port):
#    """send QUIT request to http server running on localhost:<port>"""
#    conn = httplib.HTTPConnection("localhost:%d" % port)
#    conn.request("QUIT", "/")
#    conn.getresponse()
# -->
