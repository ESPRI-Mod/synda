#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains squeries func.

Notes
    - sdsqueries means 'SynDa Serialized queries'.
    - squeries are queries once url is built.
"""
import sdsquery

def print_(squeries):
    for squery in squeries:
        sdsquery.print_(squery)

def get_scalar(squeries,name,default=None,type_=None):
    """This func assume all squery have the same value for this parameter."""
    squery=squeries[0] 
    value=sdsquery.get_scalar(squery,name,default,type_)
    return value
