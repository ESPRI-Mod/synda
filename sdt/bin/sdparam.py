#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module print search-API parameters."""

import argparse
import re
import sdapp
import sddao
import sdnormalize
import sdcache
import sdconst
import sdtools
import sdi18n
from sdexception import SDException

def handle_negated_value(name):
    """If parameter is negated, his name end with '!' character. We need to strip this character before checking for name existency.

    For more infos on negated value, see: https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API
    """
    return re.sub('!$','',name)

def is_case_incorrect(value):
    if value in reversed_params:
        # if we are here, it means that value exist with that exact case, so the case is correct

        return False
    else:
        if value.upper() in ucvalue2value:
            # if we are here, it means value exist, but without another case

            return True
        else:
            # if we are here, value is likely to be incorrect, but the problem
            # is not related with a case problem. This will be handled by
            # sdcheckparam

            return False

def fix_value_case(value):
    return ucvalue2value[value.upper()]

def exists_parameter_name(name):
    name=handle_negated_value(name)

    if name in params:
        return True
    else:
        return False

def get_parameter_type(name):
    """Returns parameter type."""
    name=handle_negated_value(name)

    values_count=len(params[name])
    values=params[name]

    if values_count==1:

        if values[0] is None:
            return sdconst.PARAM_TYPE_FREE
        else:

            # obsolete
            #raise SDException("SYDPARAM-001","Incorrect predefined value for '%s' parameter (value must be 'None' when parameter have only one value)"%name)

            # When parameter have only one value, that value CAN be NON-None !
            # e.g. if an index have only one project and the 'project'
            # parameter is set to 'CORDEX', then 'project' have only one value which 
            # is non-None.

            # We return PARAM_TYPE_CONTROLLED here.

            return sdconst.PARAM_TYPE_CONTROLLED

    else:
        return sdconst.PARAM_TYPE_CONTROLLED

def exists_parameter_value(name,value):
    name=handle_negated_value(name)

    if get_parameter_type(name)==sdconst.PARAM_TYPE_FREE:
        # we don't check value for free parameters

        return True
    else:
        if value in params[name]:
            return True
        else:
            return False

def get_models_mapping(models):
    """This function return norm.=>non-norm. models mapping.

    Note
        Model list retrieved from search-API are not normalized.
    """
    di={}

    for non_normalized_model in models:
        normalized_model=sdnormalize.normalize_model_name(non_normalized_model)
        di[normalized_model]=non_normalized_model

    return di

def reverse_params(params):
    """Transform key/value dict to value/key dict."""
    di={}

    for name,values in params.iteritems():
        for v in values:
            if v in di:
                if name not in di[v]:
                    di[v].append(name)
            else:
                di[v]=[name]

    return di

def build_ucvalue_index(reversed_params):
    di={}

    for value in reversed_params.keys():

        # hack: exclude None value artefact
        if value is None:
            continue

        # collision are solved here by overwriting the previous entry (i.e.
        # several values with different case collide in the same ucvalue)
        #
        # this is not perfect as we end up with partial choice
        # (e.g. if cmIP5 and cMIp5 both exist as value, we randomly choose one)
        #
        # but sdinference is not able to solve this issue as well,
        # as sdinference except the case to be correct.
        #
        di[value.upper()]=value

    return di

def print_models_mapping(models,pattern=None):

    def print_models_mapping_line(norm_name,non_norm_name):
        print "%-40s %s"%(norm_name,non_norm_name)

    print "%-40s %s"%('Normalized','Not normalized')
    print
    for m in models:
        if pattern is None:
            print_models_mapping_line(m,models[m])
        else:
            if pattern in m:
                print_models_mapping_line(m,models[m])

def filter_and_print_name(li,pattern=None):
    li=sdtools.grep_light(li,pattern)

    if len(li)==1:
        v=li[0]
        print v
    elif len(li)>1:
        for v in li:
            print v
    else:
        sdtools.print_stderr("Parameter name not found")

def filter_and_print_value(li,columns=1,pattern=None):
    li=sdtools.grep_light(li,pattern)

    if len(li)==1:
        v=li[0]

        if v == None:
            sdtools.print_stderr('Free text parameter')
        else:
            print v

    elif len(li)>1:

        if columns>1:
            sdtools.multi_columns_listing(li)
        else:
            # mono-column version

            for v in li:
                print v
    else:
        sdtools.print_stderr("Parameter value not found")

def denormalize_models_list(models_list):
    new_models_list=[]

    for m in models_list:
        if m in models: 
            # the model is normalized

            denormalized_model=models[m]

            new_models_list.append(denormalized_model)
        else:
            # the model is already denormalized

            new_models_list.append(m)

    return new_models_list

def search_match_fast(value):
    """Same as 'search_match' func, but faster."""

    if value in reversed_params:
        return reversed_params[value]
    else:
        return []

def search_match(value):
    """Search name(s) matching the given value."""
    names=[]

    for name,values in params.iteritems():
        for v in values:
            if v == value: 
                names.append(name)

    return names

def get_name_from_value(value):
    """This method is used by sdinference module."""

    names=search_match_fast(value)

    if len(names)==0:
        raise SDException("SYDPARAM-002","Parameter name cannot be infered from '%s' value (value not found). %s"%(value,sdi18n.m0020))
    elif len(names)==1:
        return names[0]
    elif len(names)>1:

        # If we are here, it's because some parameter value are used by many parameter name.
        # To solve that, what we do here is select which name we want in priority.

        # item below is not used very often, so let's try without it
        if 'cmor_table' in names:
            names.remove('cmor_table')
            if len(names)==1:
                return names[0]

        # item below is not used very often, so let's try without it
        if 'source_id' in names:
            names.remove('source_id')
            if len(names)==1:
                return names[0]

        # item below is not used very often, so let's try without it
        if 'driving_model_ensemble_member' in names:
            names.remove('driving_model_ensemble_member')
            if len(names)==1:
                return names[0]

        # if still too many match, print a warning and return the first one
        sdtools.print_stderr("WARNING: '%s' value has been associated with '%s' facet."%(value,names[0]))
        return names[0]

        # if still too many match, let's raise exception
        #raise SDException("SYDPARAM-003","Parameter name cannot be infered from '%s' value (too many matches). To solve the problem, use 'name=value' syntax."%value)

def print_(args):
    p1=args.pattern1
    p2=args.pattern2

    if (p1 is None and p2 is None):
        filter_and_print_name(params.keys())
    elif (p1 is not None and p2 is None):
        if p1 in params:
            filter_and_print_value(params[p1],columns=args.columns)
        else:
            if p1 in mapping_keywords:
                print_models_mapping(models)
            else:
                filter_and_print_name(params.keys(),pattern=p1)

    elif (p1 is not None and p2 is not None):
        if p1 in params:
            filter_and_print_value(params[p1],columns=args.columns,pattern=p2)
        else:
            if p1 in mapping_keywords:
                print_models_mapping(models,p2)
            else:
                sdtools.print_stderr("Parameter not found")

# module init

params=sddao.fetch_parameters() # load parameters list in memory

# if params empty, cache need to be populated
if len(params)<1:
    sdtools.print_stderr('Retrieving parameters from ESGF..')
    sdcache.run(reload=True)
    params=sddao.fetch_parameters()

# data structure used for acceleration
reversed_params=reverse_params(params)

# load norm.=>non-norm. model mapping in memory
models=get_models_mapping(params['model'])

# data structure used by ignorecase mode
ucvalue2value=build_ucvalue_index(reversed_params)

mapping_keywords=('model_mapping','mapping')

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('pattern1',nargs='?',default=None)
    parser.add_argument('pattern2',nargs='?',default=None)
    parser.add_argument('-c','--columns',type=int,default=1)
    args = parser.parse_args(args=argv)

    print_(args)

if __name__ == '__main__':
    main(None)
