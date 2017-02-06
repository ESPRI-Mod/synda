#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains dquery (aka deserialized query aka facets_group) related functions.

Notes
    - sddquery means 'SynDa Deserialized query'
    - A stream is a group of dquery
"""

import sdconst
import sdutils
from sdexception import SDException

def print_(dquery):

    verbose=get_scalar(dquery,'verbose',default=False,type_=bool) # we cast here as verbose can be str (set from parameter) or bool (set from '-v' option)

    if verbose:
        print dquery
    else:
        print dquery['url']

def set_scalar(dquery,name,value):

    if isinstance(value,list):
        raise SDException("SDDQUERY-003","Incorrect type (%s)"%(name,))

    if name in dquery:
        raise SDException("SDDQUERY-002","Key already exist (%s)"%(name,))

    # tricky code because scalar facet are stored as vector

    dquery[name]=[value]

def get_scalar(facets_group,name,default=None,type_=None):
    """
    Args
        type_: helper used to cast before returning the value.
    Returns
        value as scalar
    """

    # tricky code because scalar facet are stored as vector

    if name in facets_group:
        value=facets_group[name]


        if isinstance(value,list):

            if len(value)>1:
                raise SDException("SDDQUERY-001","Too much values for '%s' parameter (value='%s')"%(name,str(value)))

            v=value[0]

        else:

            v=value


        casted_value=sdutils.cast(v,type_)

        return casted_value
    else:
        return default

def get_list(facets_group,name,default=None):
    """
    Returns
        value as list
    """
    if name in facets_group:
        value=facets_group[name]

        if isinstance(value,list):
            return value
        else:
            return [value]
    else:
        return default

def is_empty(dquery):
    """This func return True if dquery if empty."""

    di=search_api_parameters(dquery)

    if len(di)==0:
        result=True
    elif len(di)==1:
        if 'limit' in dquery.keys():
            # if only this key, then consider empty

            result=True
        else:
            result=False
    elif len(di)>1:
        result=False

    return result

def search_api_parameters(facets_group):
    """Keeps only search-API parameters."""

    new_facets_group={}

    for k in facets_group:
        if k not in sdconst.SDSSP:
            new_facets_group[k]=facets_group[k]

    return new_facets_group

def synda_parameters(facets_group):
    """Keeps only Synda parameters."""
    new_facets_group={}

    for k in facets_group:
        if k in sdconst.SDSSP:
            new_facets_group[k]=facets_group[k]

    return new_facets_group

