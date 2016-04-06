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
import time
import traceback
import argparse
import urllib2
import shutil
import sdapp
import sdconfig
import sdutils
from sdnetutils import HTTPSClientAuthHandler
from sdprogress import SDProgressDot

def download_file(url,local_path,checksum_type):

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

    f.write(socket.read())

def socket2disk_largefile(socket,f):

    # notes
    #     - without progress

    shutil.copyfileobj(socket, f)

def socket2disk_progressbar(socket,f):
    chunksize=4096

    while 1:
        data = socket.read(chunksize)

        if not data:
            #print "done."
            break

        f.write(data)

        SDProgressDot.print_char()
        #print "Read %s bytes"%len(data)

def data_parts(socket,chunksize=1024):
    """
    Chunksize examples
        1024
        8192
        16*1024
        208*1024 (this one is to fit value in /proc/sys/net/core/rmem_default)
    """

    while True:
        data = socket.read(chunksize)

        if not data:
            break

        yield data

def socket2disk_progressbar_and_rate(socket,f):
    total_size = socket.headers.get('content-length')
    bytes_so_far = 0 # how much data have been downloaded
    progressbar_size=50
    start = time.time()
    i=0

    if total_size is None:
        # no content length header

        assert False # if happens, use size from ESGF metadata
    else:
        total_size=int(total_size)

        for data in data_parts(socket,chunksize=(16*1024)):
            f.write(data)

            # compute metrics
            bytes_so_far += len(data)
            progressbar_done = int(progressbar_size * bytes_so_far / total_size) # ratio reduced to progressbar_size
            rate=bytes_so_far//(time.time() - start)

            # human readable unit
            rate=rate//1024


            # display

            if i%9==0: # prevent too much screen refresh

                # progressbar
                # TODO: print full bar in the last display (i.e. instead of having the last sprite missing)
                sys.stdout.write("\r[%s%s] %s KiB/s" % ('=' * progressbar_done, ' ' * (progressbar_size - progressbar_done), rate))

                # prevent cursor from blinking
                sys.stdout.flush()

            i+=1

        print ''

def socket2disk_percent(socket,f):
    total_size = socket.headers.get('content-length')
    bytes_so_far = 0 # how much data have been downloaded
    start = time.time()
    i=0

    if total_size is None:
        # no content length header

        assert False # if happens, use size from ESGF metadata
    else:
        total_size=int(total_size)

        for data in data_parts(socket,chunksize=(16*1024)):
            f.write(data)

            # compute metrics
            bytes_so_far += len(data)
            percent = float(bytes_so_far) / total_size

            # human readable unit
            percent = round(percent*100, 2)


            # display

            if i%9==0: # prevent too much screen refresh

                # percent
                # TODO: print 100% in the last display (i.e. instead of having 99.98%)
                sys.stdout.write("Downloaded %d of %d Mebibytes (%0.2f%%)\r" % ((bytes_so_far // 1024 // 1024), (total_size // 1024 // 1024), percent))

                # prevent cursor from blinking
                sys.stdout.flush()

            i+=1

        print ''

def download_file_helper(url, local_path):
    f=None
    socket=None
    opener=None

    try:

        # setup HTTP handler

        opener = urllib2.build_opener(HTTPSClientAuthHandler(sdconfig.esgf_x509_proxy,sdconfig.esgf_x509_proxy))
        opener.add_handler(urllib2.HTTPCookieProcessor())


        # open local file

        f=open(local_path, 'wb') # TODO: rename f to fp


        # open socket

        socket=opener.open(url) # 'socket' name is arbitrary (maybe 'web_file' is better, as opener.open return a file-like object (from https://docs.python.org/2/library/urllib2.html#module-urllib2). Other candidate are  'response','urlfile','o','object')

        
        # download file

        # TODO
        # for better performance, add on-the-fly checksum using link below
        # https://gist.github.com/brianewing/994303 - TAG45H5K345H3

        #socket2disk_basic(socket,f)
        #socket2disk_largefile(socket,f)
        #socket2disk_progressbar(socket,f)
        socket2disk_progressbar_and_rate(socket,f)
        #socket2disk_percent(socket,f)

        return 0

    except Exception,e:

        # remove the local file if something goes wrong
        os.unlink(local_path)

        # TODO: re-raise exception here and print exception upstream
        traceback.print_exc(file=sys.stderr)

        return 1

    finally:

        if f is not None:
            f.close()
        if socket is not None:
            socket.close()
        if opener is not None:
            opener.close()

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    sys.exit(0)
