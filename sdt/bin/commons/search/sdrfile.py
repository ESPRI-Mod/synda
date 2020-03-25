#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains *remote* file search and display routines."""

import humanize
from tabulate import tabulate

from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.search import sdquicksearch
from sdt.bin.commons.param import sddeferredbefore
from sdt.bin.models.sdtypes import File


def get_files(stream=None, parameter=None, post_pipeline_mode='file', dry_run=False):
    # TODO: maybe remove parameter argument everywhere as there is a mess in get_selection_
    # file_buffer, because of default/forced parameter (i.e. len(parameter) is non-zero
    # even if non parameter args set on CLI !)

    if parameter is None:
        parameter = []

    assert (stream is None) or (len(parameter) < 1)  # this is to prevent using stream and parameter together

    if len(parameter) > 0:
        sddeferredbefore.add_forced_parameter(parameter, 'type', 'File')
    elif stream is not None:
        sddeferredbefore.add_forced_parameter(stream, 'type', 'File')

    result = sdquicksearch.run(stream=stream, parameter=parameter, post_pipeline_mode=post_pipeline_mode,
                               dry_run=dry_run)
    return result.get_files()


def get_file(stream=None, parameter=None, dry_run=False):
    if parameter is None:
        parameter = []

    files = get_files(stream=stream, parameter=parameter, dry_run=dry_run)
    if len(files) == 0:
        f = None
    else:
        f = files[0]

    return f


def print_list(files):
    li = [[f['status'], humanize.naturalsize(f['size'], gnu=False), f['file_functional_id']] for f in files]
    print(tabulate(li, tablefmt="plain"))


def print_replica_list(files):
    li = [[f['file_functional_id'], f['data_node']] for f in files]
    print(tabulate(li, tablefmt="plain"))


def print_details(f):
    f = File(**f)

    print("file: %s" % f.file_functional_id)
    print("status: %s" % f.status)
    print("size: %s (%s)" % (f.size, humanize.naturalsize(f.size, gnu=False)))
    print("checksum: %s" % f.checksum)
    print("url: %s" % f.url)

    local_path_label = 'local path' if f.status in (sdconst.TRANSFER_STATUS_DELETE, sdconst.TRANSFER_STATUS_DONE) \
        else 'local path (once downloaded)'
    print("%s: %s" % (local_path_label, f.get_full_local_path()))

    print("replica: %s" % f.replica)
    print("data_node: %s" % f.data_node)
