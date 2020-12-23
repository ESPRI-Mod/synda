#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains post-processing proxy.

Note
    sdppproxy means 'SynDa Post-Processing proxy'
"""

import urllib2
import pyjsonrpc
from pyjsonrpc.rpcerror import MethodNotFound,InternalError
import argparse
import sdlog
import sdconfig
import sdtrace
import sdnetutils
from sdexception import RemoteException

def event(events):
    try:
        sdlog.info("SDPPPROX-001","Push events to postprocessing")
        serialized_events=[e.__dict__ for e in events] # transform list of event to list of dict (needed, because custom class cannot be serialized to JSON)
        get_service().event(serialized_events) # send events
        sdlog.info("SDPPPROX-002","%i events successfully transmitted to postprocessing"%len(serialized_events))
    except urllib2.URLError,e:
        sdlog.error("SDPPPROX-010","Network error occured (url=%s,port=%s,%s)"%(url,port,str(e)))
        raise RemoteException("SDPPPROX-100","Network error occured")
    except MethodNotFound,e:
        sdlog.error("SDPPPROX-012","Method not found ('event')")
        raise
    except InternalError,e:
        sdlog.error("SDPPPROX-016","Server internal error (see %s file for more details)"%sdconfig.stacktrace_log_file)

        # print 'server side' exception stack
        sdtrace.log_message(e.data)

        # TODO: find a way to also print it on the server side

        raise RemoteException("SDPPPROX-120","Server internal error")
    except Exception,e:
        sdlog.error("SDPPPROX-003","Error occured when passing events to postprocessing (%s,%s)"%(e.__class__.__name__,str(e)))
        raise

def get_service():
    """
    TODO: add retry mecanism for when service is unreachable
    """
    global service

    if service is None:
        service=pyjsonrpc.HttpClient(url=url, username=username, password=password, timeout=timeout)

    return service

# module init.

sdnetutils.allow_self_signed_certificate()

host=sdconfig.config.get('post_processing','host')
port=sdconfig.config.get('post_processing','port')
username=sdconfig.config.get('post_processing','username')
password=sdconfig.config.get('post_processing','password')

url='https://%s:%s/jsonrpc'%(host,port)
timeout=3
service=None

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v','--verbose',action='store_true')
    args = parser.parse_args()

    if args.verbose:
        print url
        print username

    try:
        print get_service().test1(1,2)
        print "Connection test successfully completed"
    except urllib2.URLError as e:
        raise RemoteException("SDPPPROX-101","Network error occured (%s)"%str(e))
