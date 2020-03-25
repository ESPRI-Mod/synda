#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright œ(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains squeries func.

Notes
    - sdsqueries means 'SynDa Serialized queries'.
    - squeries are queries once url is built.
"""
from sdt.bin.commons.utils import sdutils


def print_(squeries):
    for squery in squeries:
        print_single_squery(squery)


def get_scalar(squeries, name, default=None, type_=None):
    """This func assume all squery have the same value for this parameter."""
    squery = squeries[0]
    value = get_scalar_single_squery(squery, name, default, type_)
    return value


def print_single_squery(squery):
    verbose = get_scalar(squery, 'verbose', default=False, type_=bool)
    if verbose:
        print(squery)
    else:
        print(squery['url'])


def get_scalar_single_squery(squery, name, default=None, type_=None):
    ap = squery.get('attached_parameters')
    value = ap.get(name, default)
    casted_value = sdutils.cast(value, type_)
    return casted_value
