#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module caches ESGF parameters in local database."""

import argparse
import sdapp
import sdutils
import sdprogress
import sddao
import sdlog
import sdindex
import sdsqlutils
import sddb
import sdnetutils
import sdremoteparam_light
import sdtools
from sdtypes import Request,Item
from sdexception import SDException

def run(host=None,reload=False,project=None):

    # default
    if host is None:
        host=sdindex.get_default_index()
    if project is None:
        project='CMIP5'

    if reload:
        sdsqlutils.truncate_table('param')

    parameters=get_parameters_from_searchapi(host,project)
    parameters=remove_unused_parameters(parameters)
    parameters=add_system_parameters(parameters) # overwrite occurs here, it's normal (e.g. for 'type' parameter)

    if reload:
        sdlog.info("SDDCACHE-001","Reloading parameters (index=%s)"%host)
        _reload_parameters(parameters)
    else:
        sdlog.info("SDDCACHE-002","Updating parameters (index=%s)"%host)
        _update_parameters(parameters)

def _reload_parameters(parameters):
    for pname,pvalues in parameters.iteritems():
        for i,item in enumerate(pvalues):

            if item is None:
                sddao.add_parameter_value(pname,None,commit=False)
            else:
                sddao.add_parameter_value(pname,item.name,commit=False)
    sddb.conn.commit()

def _update_parameters(parameters):
    for pname,pvalues in parameters.iteritems():
        if len(pvalues)==0:
            raise SDException("SYDCACHE-003","fatal error (pvalues=%s)"%str(pvalues))
        elif len(pvalues)==1:
            # This case means this is a parameter without value (e.g. 'title'). This is because a parameter with values have at least two values, else it's a constant...
            # We just add the parameter name if not exist.

            if not sddao.exists_parameter_name(pname):
                sdtools.print_stderr('Add new parameter: %s'%pname)
                sddao.add_parameter_value(pname,None) # value is always None in this case

        elif len(pvalues)>1:
            for item in pvalues:
                if not sddao.exists_parameter_value(pname,item.name):
                    sdtools.print_stderr('Add new value for %s parameter: %s'%(pname,item.name))
                    sddao.add_parameter_value(pname,item.name)

def add_system_parameters(parameters):
    """
    Note
      - overwrite pre-existing parameters if any.
    """
    parameters['replica']=[Item('true'),Item('false')]
    parameters['distrib']=[Item('true'),Item('false')]
    parameters['latest']=[Item('true'),Item('false')]
    parameters['type']=[Item('File'),Item('Dataset'),Item('Aggregation')]
    parameters['shards']=[None]
    parameters['query']=[None]
    parameters['limit']=[None]
    parameters['fields']=[None]

    return parameters

def remove_unused_parameters(parameters):
    """Remove unused parameters.

    Note
        If Those parameters are used in the future, remove this func.
    """

    if 'cf_standard_name' in parameters:
        del parameters['cf_standard_name']
    if 'variable_long_name' in parameters:
        del parameters['variable_long_name']

    return parameters

def get_parameters_from_searchapi(host,project,dry_run=False):
    """Method used to retrieve parameters list from search-API

    sample queries
        http://esg-datanode.jpl.nasa.gov/esg-search/search?facets=model&limit=0 
        http://esg-datanode.jpl.nasa.gov/esg-search/search?facets=*&limit=0

    Note: 
        for now, parameters based processing like parameters caching,
        parameters checking and parameters inference are not project aware
        (i.e. the url retrieve all parameters regardless of the project).
        There is a 'project' parameter in this func, but it's only used
        for the third query.
    """
    #sdtools.print_stderr("Using '%s' index"%host)

    #sdprogress.SDProgressDot.print_char()

    params={}

    # First pass to retrieve most parameters
    d=sdremoteparam_light.run(facets_group={'type':['Dataset']},dry_run=dry_run,host=host)
    params.update(d)

    #sdprogress.SDProgressDot.print_char()

    # Second pass needed as some parameters are missing when using 'facets=*' (currently, only for 'index_node' parameter)
    d=sdremoteparam_light.run(pname='index_node',facets_group={'type':['Dataset']},dry_run=dry_run,host=host)
    params.update(d)

    #sdprogress.SDProgressDot.print_char()

    # Third pass to fetch file attributes which can also be used as search criterias (e.g. title)
    #
    # Note:
    #   Those attributes are added without corresponding values 
    #   (i.e. it's only used for name checking, not for value checking)
    #
    # TODO: 
    #   Maybe do this for each project (to retrieve project specific attributes)
    #
    url='http://%s/esg-search/search?limit=1&project=%s&type=File&fields=*'%(host,project)
    request=Request(url=url,pagination=False)
    result=sdnetutils.call_web_service(request,60) # return Response object

    assert len(result.files)==1 # just in case

    for attribute_name in result.files[0]: # indice 0 is because we retrieve one file only (with 'limit=1')
        if attribute_name not in params:
            params[attribute_name]=[None]

    #sdprogress.SDProgressDot.print_char()
    #sdprogress.SDProgressDot.progress_complete()

    return params

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--index_host')
    parser.add_argument('-p','--project')
    parser.add_argument('-r','--reload',action='store_true',help='Recreate cache from scratch')
    args = parser.parse_args()

    answer=sdutils.query_yes_no('Retrieve parameters from ESGF ?', default="no")

    if answer:
        run(host=args.index_host,reload=args.reload,project=args.project)
        sdtools.print_stderr("Parameters are up-to-date.")
