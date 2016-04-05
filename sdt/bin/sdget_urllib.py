#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains file transfer functions for HTTP protocol (urllib2 impl.)."""

import os
import sys
import traceback
import argparse
import urllib2
import sdapp
import sdconfig
import sdutils
from sdnetutils import HTTPSClientAuthHandler
from sdprogress import SDProgressDot

def run(url,local_path,checksum_type):

    # create folder if missing
    destdir=os.path.dirname(local_path)
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    status=download_file_helper(url,local_path)

    if status==0:
        local_checksum=sdutils.compute_checksum(local_path,checksum_type)
    else:
        local_checksum=None

    return (status,local_checksum)

def socket2disk_basic(socket,f):

    # notes
    #     - without progress
    #     - without largefile support (i.e. may be slow for file that doesn't fit in memory (i.e. swap))
    #
    f.write(socket.read())

def socket2disk_progress(socket,f):

    chunk = 4096
    while 1:
        data = socket.read(chunk)

        if not data:
            #print "done."
            break

        f.write(data)

        SDProgressDot.print_char()
        #print "Read %s bytes"%len(data)

def download_file_helper(url, local_path):

    try:

        # setup HTTP handler

        opener = urllib2.build_opener(HTTPSClientAuthHandler(sdconfig.esgf_x509_proxy,sdconfig.esgf_x509_proxy))
        opener.add_handler(urllib2.HTTPCookieProcessor())


        # prepare local file


        f=open(local_path, 'w')

        
        # download file

        socket=opener.open(url) # 'socket' name is arbitrary (maybe 'response' or 'urlfile' or 'o' or 'object' is better)

        # TODO
        # for better performance, add on-the-fly checksum using link below
        # https://gist.github.com/brianewing/994303 - TAG45H5K345H3

        socket2disk_basic(socket,f)
        #socket2disk_progress(socket,f)

        
        # cleanup

        f.close()
        socket.close()
        opener.close()

    except Exception,e:

        # remove the local file if something goes wrong
        os.unlink(local_path)

        # debug
        traceback.print_exc(file=sys.stderr)

        return 1

    return 0

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    sys.exit(0)
