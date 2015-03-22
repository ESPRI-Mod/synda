#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdnetutils.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains network functions."""

import urllib2
#import requests
import sdxml
from sdtypes import Response
from sdexception import SDException
from sdtime import SDTimer
import sdlog
import sdpoodlefix

def call_web_service(request,timeout):
    start_time=SDTimer.get_time()
    buf=HTTP_GET(request.get_url(),timeout)
    elapsed_time=SDTimer.get_elapsed_time(start_time)

    try:
        result=sdxml.parse_metadata(buf)
    except Exception,e:

        # If we are here, it's likely that they is a problem with the internet connection
        # (e.g. we are behind an HTTP proxy and have no authorization to use it)

        sdlog.info('SDNETUTI-001','XML parsing error (exception=%s). Most of the time, this error is due to a network error.'%str(e))

        # debug
        # (if the error is not due to a network error (e.g. internet connection problem), raise the original exception below and set the debug mode to see the stacktrace.
        #raise

        raise SDException('SDNETUTI-008','Network error (see log for details)') # we raise a new exception 'network error' here, because most of the time, 'xml parsing error' is due to an 'network error'.

    return Response(call_duration=elapsed_time,**result)

def call_param_web_service(url,timeout):
    buf=HTTP_GET(url,timeout)

    try:
        params=sdxml.parse_parameters(buf)
    except:

        # If we are here, it's likely that they is a problem with the internet connection
        # (e.g. we are behind an HTTP proxy and have no authorization to use it)

        raise SDException('SDNETUTI-003','Network error')

    return params

def HTTP_GET(url,timeout=20):
    sock=None
    buf=None

    try:
        sdpoodlefix.start(url)

        # urllib2
        #
        sock=urllib2.urlopen(url, timeout=timeout)
        buf=sock.read()

        # requests
        #
        #response=requests.get(url, timeout=timeout)
        #buf=response.text

    except Exception, e:
        errmsg="HTTP query failed (url=%s,exception=%s)"%(url,str(e))
        errcode="SDNETUTI-002"

        raise SDException(errcode,errmsg)

    finally:
        if sock!=None:
            sock.close()

        sdpoodlefix.stop()


    return buf
