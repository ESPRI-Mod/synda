#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains search-API query common routines.

Notes
    - 'sdremotequtils' means 'SynDa remote Query utils'
    - logic
      'OR' operator is used between the different values of the same facet
      'AND' operator is used between different facets
"""

from sdexception import SDException
import sdconst
import sdconfig
import sdurlutils

def serialize_parameters(facets):
    """Serialize parameters

    Example
        input
            {'variable':['tasmin','tasmax']}
        output
            "variable=tasmin&variable=tasmax"
    """
    filters=[]

    for k,v in facets.iteritems():

        if k in ['fields']:
            filters.append(serialize_parameter__mvpp(k,v))
        else:
            filters.append(serialize_parameter__ovpp(k,v))

    return "&".join(filters) # join between different parameters

def serialize_parameter__ovpp(name,values): # 'ovpp' means one value per parameter
    """Serialize one parameter

    Example
        input
            name="variable"
            values=["tasmin","tasmax"]
        output
            "variable=tasmin&variable=tasmax"
    """
    l=[]

    assert isinstance(values,list)

    for v in values:
        l.append(name+"="+v)

    if len(l)>0:
        return "&".join(l) # join between different values of same parameter
    else:
        return ""

def serialize_parameter__mvpp(name,values): # 'mvpp' means 'many values per parameter'
    """Serialize one parameter

    Example
        input
            name="fields"
            values=["instance_id","id"]
        output
            "fields=instance_id,id"
    """
    serialized_values=",".join(values)

    if len(serialized_values)>0:
        return "%s=%s"%(name,serialized_values)
    else:
        return ''

def build_url(facets,searchapi_host):
    serialized_parameters=serialize_parameters(facets)

    # as parameters can contain special char, we need to encode them 
    serialized_parameters=serialized_parameters.replace(" ","%20")
    #serialized_parameters=serialized_parameters.replace("|","%7C") # seems no need to encode this one (done automatically by the browser)

    fmt=sdurlutils.get_solr_output_format(sdconfig.searchapi_output_format)

    url="http://{0}/esg-search/search?{1}&format={2}".format(sdconst.IDXHOSTMARK,serialized_parameters,fmt)

    if len(url)>3500: # we limit buffer size as apache server doesnt support more than 4000 chars for HTTP GET buffer
        raise SDException("SDRQUUTI-001","url is too long (%i)"%len(url))

    if searchapi_host is not None:
        url=url.replace(sdconst.IDXHOSTMARK,searchapi_host)
    else:
        # we leave the fake index host (it will be replaced with the real host later)

        pass

    return url
