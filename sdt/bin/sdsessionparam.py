#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""'syndac' helper classes."""

import re
import sdconst
from sdexception import SDException
from sdtypes import SessionParam

def get_serialized_session_facets():
    """Return serialized search-api facets."""
    return ['%s=%s'%(name,sp.value) for name,sp in get_session_facets().iteritems()]

def get_session_facets():
    """Return search-api facets."""
    di={}
    for name,sp in session_params.iteritems():
        if sp.search_api_facet:
            di[name]=sp
    return di

def get_session_facets_as_facetsgroup(): # maybe rename this method
    di={}
    for name,sp in get_session_facets().iteritems():
        di[name]=[sp.value_to_string()] # TODO: currently, only one value is supported (i.e. not list). Try find a way to support multiple values.
    return di

def remove_session_param(name):
    sp=session_params.get(name)
    if sp.search_api_facet:
        if name not in ('type'): # those are search-api facets that can't be removed
            del session_params[name]
        else:
            print "This parameter can't be removed"
    else:
        print "This parameter can't be removed"

def set(pname,pvalue):

    # this is to accept space (e.g. set foo = bar)
    pname=pname.strip()
    pvalue=pvalue.strip()

    if pname in session_params:
        sp=session_params[pname]
        sp.set_value_from_string(pvalue)
    else:
        sp=SessionParam(pname,type_=str,search_api_facet=True,value=pvalue) # note that only parameter with 'str' type can be set (for now)
        session_params[pname]=sp

def print_search_api_facets():
    for name,sp in session_params.iteritems():
        if sp.search_api_facet:
            print '%s=%s'%(name,sp.value_to_string())

def print_options():
    for name,sp in session_params.iteritems():
        if not sp.search_api_facet:
            print '%s=%s'%(name,sp.value_to_string())

def print_session_params():
    if len(get_serialized_session_facets())>0: # if no session facets, no need for option header as only option are printed.
        print 'Options'
        print '======='

    print_options()

    if len(get_serialized_session_facets())>0:
        print ''
        print 'Facets'
        print '======'
        print_search_api_facets()

def print_session_param(name):
    if name in session_params:
        print '%s'%session_params.get(name).value_to_string()
    else:
        print 'No session parameter by that name'

def print_modified_session_params():
    # display session parameters that differ from default values
    for name,sp in session_params.iteritems():
        if sp.default_value!=sp.value:
            print '%s=%s'%(name,sp.value_to_string())

def get(name):
    if name in session_params:
        return session_params[name]
    else:
        raise SDException('SDSESSPA-001','Unknow parameter')

def get_value(name):
    """
    Note
        Returned type depend on the value
    """
    return get(name).value

def is_set(name):
    if get_value(name) is None:
        return False
    else:
        return True

def set_default():
    """Set sessions params to default."""
    global session_params
    session_params=get_default_session_params()

def get_default_session_params():
    session_params={}
    for (name,type_,default_value,search_api_facet,option) in sdconst.DEFAULT_SESSION_PARAMS:
        sp=SessionParam(name,type_=type_,default_value=default_value,search_api_facet=search_api_facet,value=default_value,option=option)
        session_params[name]=sp
    return session_params

# module init.

session_params=get_default_session_params()
