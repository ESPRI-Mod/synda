#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module filters a list of files."""

from synda.sdt.sdexception import SDException
from synda.sdt import sdpipelineprocessing


def run(metadata, filter_name, filter_value, mode):

    if mode == 'keep':
        po = sdpipelineprocessing.ProcessingObject(
            keep_matching_files,
            filter_name,
            filter_value,
        )
        metadata = sdpipelineprocessing.run_pipeline(metadata, po)
    elif mode == 'remove':
        po = sdpipelineprocessing.ProcessingObject(remove_matching_files, filter_name, filter_value)
        metadata = sdpipelineprocessing.run_pipeline(metadata, po)
    elif mode == 'remove_substr':
        po = sdpipelineprocessing.ProcessingObject(remove_matching_files_substr, filter_name, filter_value)
        metadata = sdpipelineprocessing.run_pipeline(metadata, po)
    else:
        raise SDException("SDSIMPLF-002", "Incorrect mode (%s)" % mode)

    return metadata


def keep_matching_files(files, filter_name, filter_value):
    """Keeps files with an exact match.

    Note:
        - If filter name not found in file attributes, raises exception.
    """
    new_files = []
    for f in files:

        if filter_name not in f:
            raise SDException(
                "SDSIMPLF-001",
                "Filter name not found in file attributes (filter_name=%s)" % (filter_name,),
            )

        if f[filter_name] == filter_value:
            new_files.append(f)

    files = new_files

    return files


def remove_matching_files(files, filter_name, filter_value):
    """Remove files with an exact match.

    Note:
        If filter name not found in file attributes, raises exception.
    """
    new_files = []
    for f in files:

        if filter_name not in f:
            raise SDException(
                "SDSIMPLF-003",
                "Filter name not found in file attributes (filter_name=%s)" % (filter_name,),
            )

        if f[filter_name] != filter_value:
            new_files.append(f)

    files = new_files

    return files


def remove_matching_files_substr(files, filter_name, filter_value):
    """Remove files with a substring match.

    Note:
        If filter name not found in file attributes, raises exception.
    """
    new_files = []
    for f in files:

        if filter_name not in f:
            raise SDException(
                "SDSIMPLF-004",
                "Filter name not found in file attributes (filter_name=%s)" % (filter_name,),
            )

        if f[filter_name].find(filter_value) < 0:
            new_files.append(f)

    files = new_files

    return files
