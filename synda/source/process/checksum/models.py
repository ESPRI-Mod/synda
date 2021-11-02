# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import hashlib

from synda.source.config.file.user.preferences.decorators import print_elapsed_time

DEFAULT_CHUNK_SIZE = 1024*64


def read_chunks(file_handle, chunk_size=DEFAULT_CHUNK_SIZE):
    while True:
        data = file_handle.read(chunk_size)
        if not data:
            break
        yield data


def _calc_checksum(file_handle, checksum_type):

    if checksum_type == "md5":
        hasher = hashlib.md5()
    elif checksum_type == "sha256":
        hasher = hashlib.sha256()
    else:
        hasher = None

    if hasher:
        for chunk in read_chunks(file_handle):
            hasher.update(chunk)
        checksum = hasher.hexdigest()
    else:
        checksum = ""
    return checksum


@print_elapsed_time()
def calc_checksum(filename, checksum_type):
    try:
        with open(filename, 'rb') as fh:
            checksum = _calc_checksum(fh, checksum_type)
    except IOError as e:
        checksum = ""
    return checksum
