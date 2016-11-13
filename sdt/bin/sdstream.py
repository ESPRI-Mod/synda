#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains stream (aka facets_groups) related functions.

Note
    A stream is a group of dquery
"""

import sddquery

def print_(dqueries):
    for dquery in dqueries:
        sddquery.print_(dquery)

def set_scalar(stream,name,value):
    """
    Note
        we assume all dquery have same value for that parameter.
    """
    for dquery in stream:
        sddquery.set_scalar(dquery,name,value)

def get_scalar(stream,name,default=None,type_=None):

    assert len(stream)>0 # stream must have at least one dquery inside when calling this func.

    dquery=stream[0] # note that stream can have more than one dquery inside, but then we assume all dquery have same value for that parameter.

    value=sddquery.get_scalar(dquery,name,default=default,type_=type_)

    return value

def get_facet_values(facets_groups,facet_name):
    """Merge and return facet values.

    Note
        This function gives informations about the whole facets_groups (i.e. not about just one facets_group).
    """
    li=[]
    for facets_group in facets_groups:
        if facet_name in facets_group:
            li.extend(facets_group[facet_name]) # we use extend, as facet value type is 'list'

    return li

def exists(stream,key,values):
    """Check if given values intersect with values from stream."""

    values_from_stream=get_facet_values(stream,key)

    if any(i in values for i in values_from_stream):
        return True
    else:
        return False

def is_empty(stream):
    """This func returns True if stream is empty."""
    li=[sddquery.is_empty(dquery) for dquery in stream]
    result=all(li)
    return result

def is_stream(o):
    """
    This func is used to tell if object is a parameter list or a stream (i.e. a
    facets_group list).
    """
    assert o is not None
    assert isinstance(o,list)


    if len(o)==0:

        # a stream contains at least one facets_group
        return False


    if isinstance(o[0],dict): # This test is based on the fact that stream contains only dict and parameter contains only str)
        # list contains dict, so it's a stream

        return True
    else:
        # list contains something different from dict, so we assume it's a parameter

        return False
