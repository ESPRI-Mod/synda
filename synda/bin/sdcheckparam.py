#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module checks selection parameters.

Note
    Some processing done in this module overlap with sdinference module, but
    most don't, so both module are required.
"""

import sys
import json
import argparse
import sdapp
import sdlog
import sdparam
import sddquery
import sdconst
import sdconfig
import sdprint
import sddquery
import sdi18n
from sdtools import print_stderr
import sdexception

def run(facets_groups):
    facets_groups=check_parameters(facets_groups)
    facets_groups=check_coherency(facets_groups)
    facets_groups=check_search_api_scalar_parameter(facets_groups)
    facets_groups=check_replica_not_set_when_using_nearestpost(facets_groups)

    return facets_groups

def check_replica_not_set_when_using_nearestpost(facets_groups):
    """Do not continue if 'replica' has been set ('replica' must not be set, as we want to search for the nearest in all existing copies of the file)."""

    #msg="'replica' facet must not be set when using 'sdnearestpost' module"
    msg="'replica' facet must not be set when using 'nearest' mode"

    conflict_between_replica_and_nearest_flags=False

    for dquery in facets_groups:
        if sdconfig.nearest_schedule=='post':
            if sddquery.get_scalar(dquery,'nearest',False,bool):
                if 'replica' in dquery:
                    #raise sdexception.SDException('SYDCHECK-010',msg)
                    conflict_between_replica_and_nearest_flags=True

    if conflict_between_replica_and_nearest_flags:
        sdlog.warning("SYDCHECK-043",msg,stderr=True)

    return facets_groups

def check_search_api_scalar_parameter(facets_groups):
    """This func is an assert that prevent Search-API scalar keywords from
    being set multiple times.
    """
    for facets_group in facets_groups:
        for name in sdconst.SASP:
            if name in facets_group:
                value=facets_group[name]
                if len(value)>1:
                    raise sdexception.SDException("SYDCHECK-004","Too much values for '%s' parameter (value='%s')"%(name,str(value)))
        
    return facets_groups

def check_parameters(facets_groups):
    for facets_group in facets_groups:
        for name,values in sddquery.search_api_parameters(facets_group).iteritems():
            if not sdparam.exists_parameter_name(name):

                # obsolete
                #
                # do not raise fatal exception anymore here, as there are
                # plenty of search-api parameters that are not cached (e.g.
                # 'title' aka filename). So coming here IS regular.
                #
                #sdlog.info("SYDCHECK-001","Unknown parameter name (%s)"%(name,))

                # in fact it is better to raise exception here, else user is not informed
                # when typo occurs in parameter name (e.g. 'experiments' instead of 'experiment')
                raise sdexception.UnknownParameterNameException("SYDCHECK-008","Unknown parameter name: %s"%(name,))

            else:
                check_parameter_values(name,values)
    return facets_groups

def check_parameter_values(name,values):
    for value in values:
        if not sdparam.exists_parameter_value(name,value):

            msg="Unknown value '%s' for '%s' parameter. %s"%(value,name,sdi18n.m0021)

            if sdconfig.unknown_value_behaviour=='warning':
                print_stderr('WARNING: '+msg)
            else:
                raise sdexception.UnknownParameterValueException("SYDCHECK-002",msg)

def check_coherency(facets_groups):
    for facets_group in facets_groups:
        if 'time_frequency' in facets_group:
            if 'ensemble' in facets_group:
                if "fx" in facets_group['time_frequency']:
                    if "r0i0p0" not in facets_group['ensemble']:

                        # print a warning, because 'r0i0p0' is the only choice for fx frequency
                        sdlog.warning("SYDCHECK-003","'fx' frequency is used, but ensemble do not include 'r0i0p0'")

    return facets_groups

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    facets_groups=json.load(sys.stdin)
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
