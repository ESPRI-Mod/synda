#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script removes incomplete/malformed files.

Description
    This module contains file rejection step 2 (file rejection step 1 is done
    by sdpostxptransform module).
"""

from sdt.bin.commons.utils import sdlog


def run(files):
    files = remove_incomplete_files(files)
    return files


def is_file_complete(file):
    filename = file.get("title")

    if file.get("dataset_id") is None:
        sdlog.error("SDREDUCE-002", "incorrect dataset_id (filename={})".format(filename))
        return False

    if file.get("url_http") is None:  # memo: 'url_<proto>' is renamed to 'url' in a downstream step (in sdprotocol)
        sdlog.error("SDREDUCE-001", "Incorrect url_http ({})".format(filename))
        return False
    return True


def remove_incomplete_files(files):
    new_files = []
    for f in files:
        if is_file_complete(f):
            new_files.append(f)

    return new_files
