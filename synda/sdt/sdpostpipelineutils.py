#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
 
"""This module contains post pipeline generic functions. """

from synda.sdt.sdexception import SDException

from synda.source.config.api.esgf_search.constants import STRUCTURE as SEARCH_API_STRUCTURE


def exists_attached_parameter(file_, name):
    if 'attached_parameters' in file_:
        if name in file_['attached_parameters']:
            return True
        else:
            return False
    else:
        return False


def get_attached_parameter(file_, name, default=None):
    if 'attached_parameters' in file_:
        return file_['attached_parameters'].get(name, default)
    else:
        return default


def get_attached_parameter__global(files, name):
    """This function assumes all files have the same value for the <name> attribute."""
    if len(files) > 0:
        # retrieve first file's (arbitrary)
        file_ = files[0]
        return get_attached_parameter(file_, name)
    else:
        return None

# the two methods below is to have some abstration over file type


def get_functional_identifier_value(f):
    name = get_functional_identifier_name(f)

    if name in f:
        functional_id = f[name]
    else:
        raise SDException('SYDUTILS-020', 'Incorrect identifier (%s)' % name)

    return functional_id


def get_functional_identifier_name(f):

    if f["type"] == SEARCH_API_STRUCTURE['type']['file']:
        functional_id = 'file_functional_id'
    elif f["type"] == SEARCH_API_STRUCTURE['type']['dataset']:
        functional_id = 'dataset_functional_id'
    else:
        raise SDException('SYDUTILS-028', 'Incorrect type (%s)' % f["type"])

    return functional_id
