#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains squery (aka serialized query) related functions.

Notes
    - sdsquery means 'SynDa Serialized query'
    - squery is query once url is built.
"""

import sdutils

def print_(squery):
    verbose=get_scalar(squery,'verbose',default=False,type_=bool)
    if verbose:
        print squery
    else:
        print squery['url']

def get_scalar(squery,name,default=None,type_=None):
    ap=squery.get('attached_parameters')
    value=ap.get(name,default)
    casted_value=sdutils.cast(value,type_)
    return casted_value
