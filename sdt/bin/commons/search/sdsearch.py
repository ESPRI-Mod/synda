#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright œ(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""
ESGF files discovery

This script parses selection files, applies some filters, builds search-api
queries, executes queries, applies some filters and prints the result.

Notes
 - processes only one selection file (aka template) at a time
"""

import json

from sdt.bin.commons.utils import sdlog
from sdt.bin.commons.utils import sdconfig
from sdt.bin.commons.utils import sdtools
from sdt.bin.commons.utils.sdprogress import ProgressThread
from sdt.bin.commons.utils.sdexception import SDException

from sdt.bin.commons.pipeline import sdpipeline
from sdt.bin.commons.search import sdrun
from sdt.bin.commons.search import sdsqueries
from sdt.bin.commons.search import sdadddsattr
from sdt.bin.commons.search import sdbatchtimestamp
from sdt.bin.models import sdtypes


def run(stream=None,
        selection=None,
        path=None,
        parameter=None,
        post_pipeline_mode='file',
        parallel=sdconfig.metadata_parallel_download,
        index_host=None,
        dry_run=False,
        load_default=None,
        playback=None,
        record=None):
    """
    Note
        squeries means 'Serialized queries'
    """

    if parameter is None:
        parameter = []

    squeries = sdpipeline.build_queries(stream=stream, path=path, parameter=parameter, selection=selection,
                                        parallel=parallel, index_host=index_host, dry_run=dry_run,
                                        load_default=load_default)

    action = sdsqueries.get_scalar(squeries, 'action', None)

    # we cast here as progress can be str (set from parameter) or bool (set programmaticaly)
    progress = sdsqueries.get_scalar(squeries, 'progress', False, type_=bool)
    # Prevent use of 'limit' keyword ('limit' keyword can't be used in this module because it interfere
    # with the pagination system)
    for q in squeries:
        if sdtools.url_contains_limit_keyword(q['url']):
            raise SDException('SDSEARCH-001',
                              "'limit' facet is not supported in this mode. Use 'sdquicksearch' module instead.")

    if dry_run:
        sdsqueries.print_(squeries)
        return sdtypes.Metadata()
    else:
        if progress:
            # sdtools.print_stderr(sdi18n.m0003(ap.get('searchapi_host'))) # waiting message
            ProgressThread.start(sleep=0.1, running_message='', end_message='Search completed.')  # spinner start

        metadata = _get_files(squeries, parallel, post_pipeline_mode, action, playback, record)

        if progress:
            ProgressThread.stop()  # spinner stop

        return metadata


def execute_queries(squeries, parallel, post_pipeline_mode, action):
    """This func serializes received metadata on-disk to prevent memory overload."""

    sdlog.info("SDSEARCH-580", "Retrieve metadata from remote service")
    metadata = sdrun.run(squeries, parallel)
    sdlog.info("SDSEARCH-584", "Metadata successfully retrieved (%d files)" % metadata.count())

    sdlog.info("SDSEARCH-590", "Metadata processing begin")
    metadata = sdpipeline.post_pipeline(metadata, post_pipeline_mode)
    sdlog.info("SDSEARCH-594", "Metadata processing end")

    # moving code below inside sdfilepipeline module is not straightforward,
    # because all datasets are retrieved in one row, so we don't want it
    # to happen for each chunk (i.e. lowmem mecanism).
    # so better keep it here for now.
    # if this is also needed for, e.g. "synda dump" operation,
    # just duplicate the code below at the right place.

    sdlog.info("SDSEARCH-620", "Retrieve timestamps begins")
    metadata = fill_dataset_timestamp(squeries, metadata, parallel, action)  # complete missing info
    sdlog.info("SDSEARCH-634", "Retrieve timestamps ends")

    if sdconfig.copy_ds_attrs:
        sdlog.info("SDSEARCH-624", "Retrieve datasets attrs begins")
        metadata = copy_dataset_attrs(squeries, metadata, parallel, action)
        sdlog.info("SDSEARCH-644", "Retrieve datasets attrs ends")

    return metadata


def _get_files(squeries, parallel, post_pipeline_mode, action, playback, record):
    """
    TODO: maybe move this code inside sdmts module (e.g. metadata.dump(path))
    """

    if playback is not None:
        with open(playback, 'r') as fh:
            metadata = sdtypes.Metadata(files=json.load(fh))  # warning: load full list in memory

    else:

        metadata = execute_queries(squeries, parallel, post_pipeline_mode, action)

        if record is not None:
            with open(record, 'w') as fh:
                json.dump(metadata.get_files(), fh, indent=4)  # warning: load full list in memory

    return metadata


def fill_dataset_timestamp(squeries, metadata, parallel, action):
    # HACK
    #
    # second run to retrieve dataset timestamps in one row
    #
    # MEMO: when action is 'install', type is always 'File' (i.e. this code gets executed only for type=File)
    #
    if action is not None:
        if action == 'install':
            metadata = sdbatchtimestamp.run(squeries, metadata, parallel)

    return metadata


def copy_dataset_attrs(squeries, metadata, parallel, action):
    # HACK
    #
    # retrieve dataset attrs in one row
    #
    # MEMO: when action is 'install', type is always 'File' (i.e. this code gets executed only for type=File)
    #
    if action is not None:
        if action == 'install':
            metadata = sdadddsattr.run(squeries, metadata, parallel)

    return metadata
