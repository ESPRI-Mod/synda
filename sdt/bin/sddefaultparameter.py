#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This filter is used to process default parameters."""

import sys
import argparse
import json
import re
import sdapp
import sdconst
import sdutils

def run(facets_groups):
    new_facets_groups=[]

    for facets_group in facets_groups:
        new_facets_group=process_default_parameters(facets_group)
        new_facets_groups.append(new_facets_group)

    return new_facets_groups

def process_default_parameters(facets_group):
    default_parameters=get_default_parameters(facets_group)
    non_default_parameters=get_non_default_parameters(facets_group)

    for name,value in default_parameters.iteritems():

        name=remove_prefix(name)

        if name not in non_default_parameters:
            non_default_parameters[name]=value

    return non_default_parameters

def get_default_parameters(facets_group):
    di={}
    for k,v in facets_group.iteritems():
        if is_default_parameter(k):
            di[k]=v

    return di

def get_non_default_parameters(facets_group):
    di={}
    for k,v in facets_group.iteritems():
        if not is_default_parameter(k):
            di[k]=v

    return di

def remove_prefix(name):
    name=re.sub('^%s'%parameter_name_prefix,'',name)
    return name

def is_default_parameter(pname):
    if pname.startswith(parameter_name_prefix):
        return True
    else:
        return False

# init.

parameter_name_prefix=None
