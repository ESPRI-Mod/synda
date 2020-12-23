#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains translation routines."""

def translate_name(facets_group,rules):
    facets_group_new={}
    for k,v in facets_group.iteritems():
        new_k=rules[k] if k in rules else k
        facets_group_new[new_k]=v
    return facets_group_new

def translate_value(facets_group,rules):
    keys=facets_group.keys()
    for k in keys:
        d=rules.get(k,{})
        facets_group[k]=translate(facets_group[k],d)

def translate(values,d):
    """Translate values using dictionnary. Values not in dictionnary stay the same."""
    new_values=[]

    for v in values:
        new_v=d[v] if v in d else v
        new_values.append(new_v)

    return new_values
