#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains file transfer functions for HTTP protocol (requests impl.)."""

import os
import sys
import time
import argparse
import shutil
import humanize
import requests

from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils import sdconfig
from sdt.bin.commons.utils import sdtrace
from sdt.bin.commons.utils.sdprogress import SDProgressDot
from sdt.bin.commons.utils.sdexception import SDException


def download_file(url, local_path, timeout=sdconst.DIRECT_DOWNLOAD_HTTP_TIMEOUT):
    # create folder if missing
    destdir = os.path.dirname(local_path)
    if not os.path.exists(destdir):
        os.makedirs(destdir)

    status = download_file_helper(url, local_path, timeout)

    return status


def download_file_helper(url, local_path, timeout, chunksize=1024):
    f = None
    socket = None
    downloaded_so_far = 0
    progressbar_size = 50
    start_of_download = time.time()
    last_display = False
    i = 0
    try:

        # Send request:
        with requests.get(url, timeout=timeout, verify=sdconfig.esgf_x509_proxy, stream=True) as socket:
            socket.raise_for_status()
            total_expected_size = int(socket.headers['content-length'])
            with open(local_path, 'wb') as f:
                for chunk in socket.iter_lines(chunk_size=chunksize, decode_unicode=False, delimiter=False):
                    if chunk:
                        downloaded_so_far += len(chunk)
                        progressbar_done = int(progressbar_size * downloaded_so_far / total_expected_size)
                        rate = (downloaded_so_far // (time.time() - start_of_download)) // 1024
                        f.write(chunk)
                    if downloaded_so_far == total_expected_size:
                        progressbar_done = progressbar_size
                        last_display = True
                    # i is index used to prevent redundant screen refresh
                    if i % 9 == 0 or last_display:
                        sys.stdout.write("\r[{}{}] {} KiB/s".format('=' * progressbar_done,
                                                                    ' ' * (progressbar_size - progressbar_done), rate))
                        sys.stdout.flush()
                    i += 1
        return 0
    except Exception as e:
        # remove the local file if something goes wrong
        if os.path.exists(local_path):
            os.unlink(local_path)
        raise
    finally:
        if f is not None:
            f.close()
        if socket is not None:
            socket.close()
