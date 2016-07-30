#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains network functions."""

import sys
import os
import traceback
import urllib2
import requests
import sdxml
import sdtypes
from sdexception import SDException
from sdtime import SDTimer
import sdlog
import sdconfig
import sdpoodlefix
import httplib

class HTTPSClientAuthHandler(urllib2.HTTPSHandler):
    """HTTP handler that transmits an X509 certificate as part of the request."""
    def __init__(self, key, cert):
            urllib2.HTTPSHandler.__init__(self)
            self.key = key
            self.cert = cert
    def https_open(self, req):
            return self.do_open(self.getConnection, req)
    def getConnection(self, host, timeout=300):
            return httplib.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)

def call_web_service(url,timeout):
    start_time=SDTimer.get_time()
    buf=HTTP_GET(url,timeout)
    elapsed_time=SDTimer.get_elapsed_time(start_time)

    # HACK
    #
    # This is to prevent fatal error when document contain mixed encodings
    #
    # e.g. http://esgf-data.dkrz.de/esg-search/search?distrib=true&fields=*&type=File&limit=100&title=sftgif_fx_IPSL-CM5A-LR_abrupt4xCO2_r0i0p0.nc&format=application%2Fsolr%2Bxml&offset=0
    #
    if sdconfig.fix_encoding:
        import sdencoding
        buf=sdencoding.fix_mixed_encoding_ISO8859_UTF8(buf)

    try:
        di=sdxml.parse_metadata(buf)
    except Exception,e:

        # If we are here, it's likely that they is a problem with the internet connection
        # (e.g. we are behind an HTTP proxy and have no authorization to use it)

        sdlog.info('SDNETUTI-001','XML parsing error (exception=%s). Most of the time, this error is due to a network error.'%str(e))

        # debug
        #
        # TODO: maybe always enable this
        #
        #traceback.print_exc(file=open(sdconfig.stacktrace_log_file,"a"))

        # debug
        #
        # (if the error is not due to a network error (e.g. internet connection
        # problem), raise the original exception below and set the debug mode
        # to see the stacktrace.
        #
        #raise

        raise SDException('SDNETUTI-008','Network error (see log for details)') # we raise a new exception 'network error' here, because most of the time, 'xml parsing error' is due to an 'network error'.

    return sdtypes.Response(call_duration=elapsed_time,**di)

def call_param_web_service(url,timeout):
    buf=HTTP_GET(url,timeout)

    try:
        params=sdxml.parse_parameters(buf)
    except:

        # If we are here, it's likely that they is a problem with the internet connection
        # (e.g. we are behind an HTTP proxy and have no authorization to use it)

        raise SDException('SDNETUTI-003','Network error')

    return params

def HTTP_GET_2(url,timeout=20,verify=True):
    """requests impl."""

    buf=None

    try:
        requests.packages.urllib3.disable_warnings()
        result=requests.get(url, timeout=timeout, verify=verify)
        buf=result.text
    except Exception, e:
        errmsg="HTTP query failed (url=%s,exception=%s,timeout=%d)"%(url,str(e),timeout)
        errcode="SDNETUTI-004"

        raise SDException(errcode,errmsg)

    return buf

def HTTP_GET(url,timeout=20):
    """urllib impl."""

    sock=None
    buf=None

    try:
        sdpoodlefix.start(url)

        sock=urllib2.urlopen(url, timeout=timeout)
        buf=sock.read()
    except Exception, e:
        errmsg="HTTP query failed (url=%s,exception=%s,timeout=%d)"%(url,str(e),timeout)
        errcode="SDNETUTI-002"

        raise SDException(errcode,errmsg)

    finally:
        if sock!=None:
            sock.close()

        sdpoodlefix.stop()

    return buf

def test_access():
    urlfile = urllib2.urlopen("http://www.google.com")

    data_list = []
    chunk = 4096
    while 1:
        data = urlfile.read(chunk)
        if not data:
            break
        data_list.append(data)
        #print "Read %s bytes"%len(data)
