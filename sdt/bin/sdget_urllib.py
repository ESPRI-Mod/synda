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

def run(url,full_local_path,checksum_type):

    status=download_file(url,full_local_path)

    if status==0:
        local_checksum=sdutils.compute_checksum(full_local_path,checksum_type)
    else:
        local_checksum=None

    return (status,local_checksum)

def download_file(url, local_path):

    try:

        # setup HTTP handler

        opener = urllib2.build_opener(HTTPSClientAuthHandler(sdconfig.esgf_x509_proxy,sdconfig.esgf_x509_proxy))
        opener.add_handler(urllib2.HTTPCookieProcessor())


        # prepare local file

        destdir=os.path.dirname(local_path)
        if not os.path.exists(destdir):
            os.makedirs(destdir)

        f=open(local_path, 'w')

        
        # download file

        socket=opener.open(url) # 'socket' name is arbitrary (maybe 'response' or 'urlfile' or 'o' or 'object' is better)

        # TODO
        # JRA: modify below to add checksum & huge file support (i.e. file that doesn't fit in memory)
        # https://gist.github.com/brianewing/994303
        # http://stackoverflow.com/questions/1517616/stream-large-binary-files-with-urllib2-to-file

        # basic way (without progress, without largefile support)
        f.write(socket.read())

        # advanced way (with progress, with largefile support)
        """
        chunk = 4096
        while 1:
            data = socket.read(chunk)

            if not data:
                #print "done."
                break

            f.write(data)

            SDProgressDot.print_char()
            #print "Read %s bytes"%len(data)
        """

        
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
