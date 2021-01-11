#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import argparse
import urllib2
import shutil
import humanize
from sdnetutils import HTTPSClientAuthHandler
from sdprogress import SDProgressDot
from synda.source.config.file.certificate.x509.models import Config as SecurityFile
from synda.source.config.file.user.preferences.models import Config as Preferences


def download_file(url, local_path, timeout=Preferences().download_direct_http_timeout):

    # create folder if missing
    destdir = os.path.dirname(local_path)
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    status = download_file_helper(url, local_path, timeout)

    return status


def socket2disk_basic(socket, f):

    # notes
    #     - without progress
    #     - without largefile support (i.e. may be slow for file that doesn't fit in memory (i.e. swap))

    f.write(socket.read())


def socket2disk_largefile(socket, f):

    # notes
    #     - without progress

    shutil.copyfileobj(socket, f)


def socket2disk_progressbar(socket, f):
    chunksize = 4096

    while 1:
        data = socket.read(chunksize)

        if not data:
            # print "done."
            break

        f.write(data)

        SDProgressDot.print_char()
        # print "Read %s bytes"%len(data)


def data_parts(socket, chunksize=1024):
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


def socket2disk_progressbar_and_rate(socket, f):
    total_size = socket.headers.get('content-length')
    # how much data have been downloaded
    bytes_so_far = 0
    progressbar_size = 50
    start = time.time()
    last_display = False
    i = 0

    if total_size is None:
        # no content length header

        # if happens, use size from ESGF metadata
        assert False
    else:
        total_size = int(total_size)

        for data in data_parts(socket, chunksize=(16*1024)):
            f.write(data)

            # compute metrics
            bytes_so_far += len(data)
            # ratio reduced to progressbar_size
            progressbar_done = int(progressbar_size * bytes_so_far / total_size)
            rate = bytes_so_far//(time.time() - start)

            # human readable unit
            rate = rate//1024

            # print complete progressbar in the last display (i.e. prevent missing sprite in the end of the progressbar)
            if bytes_so_far == total_size:
                progressbar_done = progressbar_size
                last_display = True

            # display

            # prevent too much screen refresh
            if i % 9 == 0 or last_display:
                # progressbar
                sys.stdout.write(
                    "\r[%s%s] %s KiB/s" % ('=' * progressbar_done, ' ' * (progressbar_size - progressbar_done), rate),
                )

                # prevent cursor from blinking
                sys.stdout.flush()

            i += 1

        print ''


def socket2disk_percent(socket, f):
    total_size = socket.headers.get('content-length')
    # how much data have been downloaded
    bytes_so_far = 0
    start = time.time()
    last_display = False
    i = 0

    if total_size is None:
        # no content length header

        # if happens, use size from ESGF metadata
        assert False
    else:
        total_size = int(total_size)

        for data in data_parts(socket, chunksize=(16*1024)):
            f.write(data)

            # compute metrics
            bytes_so_far += len(data)
            percent = float(bytes_so_far) / total_size

            # human readable unit
            percent = round(percent*100, 2)
            human_total_size = humanize.naturalsize(total_size, gnu=False)
            human_bytes_so_far = humanize.naturalsize(bytes_so_far, gnu=False)

            # handle last display (i.e. print 100% in the last display instead of having 99.98%)
            if bytes_so_far == total_size:
                percent = 100
                last_display = True

            # display

            # prevent too much screen refresh
            if i % 9 == 0 or last_display:

                # percent
                sys.stdout.write(
                    "Downloaded %s of %s (%0.2f%%)\r" % (human_bytes_so_far, human_total_size, percent),
                )

                # prevent cursor from blinking
                sys.stdout.flush()

            i += 1

        print ''


def download_file_helper(url, local_path, timeout):

    fp = None
    socket = None
    opener = None

    try:

        esgf_x509_proxy = SecurityFile().get_credentials()

        # setup HTTP handler

        opener = urllib2.build_opener(
            HTTPSClientAuthHandler(
                esgf_x509_proxy,
                esgf_x509_proxy,
            ),
        )

        opener.add_handler(
            urllib2.HTTPCookieProcessor(),
        )

        # open local file

        fp = open(local_path, 'wb')

        # open socket

        # 'socket' name is arbitrary (maybe 'web_file' is better,
        # as opener.open return a file-like object
        # (from https://docs.python.org/2/library/urllib2.html#module-urllib2).
        # Other candidate are  'response','urlfile','o','object')

        socket = opener.open(url, timeout=timeout)
        
        # download file

        # socket2disk_basic(socket,fp)
        # socket2disk_largefile(socket,fp)
        # socket2disk_progressbar(socket,fp)
        socket2disk_progressbar_and_rate(socket, fp)
        # socket2disk_percent(socket,fp)

        return 0

    except Exception, e:

        # remove the local file if something goes wrong
        if os.path.exists(local_path):
            os.unlink(local_path)

        # debug
        # sdtrace.log_exception()

        raise
        # return 1

    finally:

        if fp is not None:
            fp.close()
        if socket is not None:
            socket.close()
        if opener is not None:
            opener.close()

# init.


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    sys.exit(0)
