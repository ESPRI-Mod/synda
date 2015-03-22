#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdsquery.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains squery (aka serialized query) related functions.

Notes
    - sdsquery means 'Synchro-Data Serialized query'
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
