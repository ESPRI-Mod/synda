#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains url related routines."""

import sdconfig

def get_solr_output_format(output_format):
    return 'application%%2Fsolr%%2B%s'%output_format

def add_solr_output_format(url):
    if 'format=application' not in url:
        url+='&format=%s'%get_solr_output_format(sdconfig.searchapi_output_format)
    return url
