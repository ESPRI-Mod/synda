#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
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
import sdremoteparam_light
import sdtools
import sdproxy_ra
from sdtypes import Request,Item
from sdexception import SDException

def run(host=None,reload=False,project=None):

    # default
    if host is None:
        host=sdindex.get_default_index()

    if reload:
        sdsqlutils.truncate_table('param')

    parameters=get_parameters_from_searchapi(host,project)
    parameters=remove_unused_parameters(parameters)
    parameters=add_system_parameters(parameters) # overwrite occurs here, it's normal (e.g. for 'type' parameter)
    add_special_parameters(parameters)

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
            # This case means this is a parameter without any associated value.

            # It is likely to be a NON-free parameter which is present in solar
            # parameters, but not used by any dataset (TBC).
            # e.g. 'realm' and 'driving_ensemble' in the query below are of that kind
            # https://esg-devel.nsc.liu.se/esg-search/search?limit=0&facets=*&type=Dataset&fields=*&format=application%2Fsolr%2Bxml
            #
            # When we are here, items likely come from TAG4353453453 step
            #
            # We DON'T add the parameter name as it seems not to be used
            # (another reason we don't store this parameter is that currently,
            # non-free parameter can only be added in param table if they are
            # associated with at least two values. If they are associated with
            # only one value, it has to be None, and it means it's a free parameter.
            # Maybe we can associate 'non-free parameter without value' with
            # NULL or '', but it's a hacky way to solve this issue. Maybe best
            # is to redesign 'param' table from scratch)

            pass
        elif len(pvalues)==1:
            # This case means this is a free parameter (i.e. without predefined
            # value choices) e.g. 'title'. This is because a NON-free parameter
            # have at least two values (e.g. true or false), else it's free
            # parameter aka a constant...
            #
            # When we are here, items likely come from TAG543534563 step
            #
            # We add the parameter name if not exist.

            if not sddao.exists_parameter_name(pname):
                sdtools.print_stderr('Add new parameter: %s'%pname)
                sddao.add_parameter_value(pname,None) # value is always None in this case

        elif len(pvalues)>1:
            # This case means this is a NON-free parameter (i.e. with predefined
            # value choices) e.g. 'experiment'.
            #
            # When we are here, items likely come from TAG4353453453 step
            #
            # We add the parameter name if not exist.

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

def add_special_parameters(parameters):

    # we add url here to prevent this error:
    #
    #<--
    #$ synda search url=http://esgf2.dkrz.de/thredds/fileServer/cmip5/output1/ICHEC/EC-EARTH/decadal1965/mon/seaIce/OImon/r8i1p1/v20120801/sic/sic_OImon_EC-EARTH_decadal1965_r8i1p1_196511-197610.nc
    #*** Error occured at 2016-05-03 21:50:01.029034 ***
    #==================
    #*   Error code   *
    #==================
    #SYDCHECK-008
    #=====================
    #*   Error message   *
    #=====================
    #Unknown parameter name: url
    #-->
    #
    # we need to insert it manually, because 'url' doesn't appear in file's attributes nor in search-api parameter
    # but it CAN be as a search key e.g. http://esgf-data.dkrz.de/esg-search/search?url=http://esgf2.dkrz.de/thredds/fileServer/cmip5/output1/ICHEC/EC-EARTH/decadal1965/mon/seaIce/OImon/r8i1p1/v20120801/sic/sic_OImon_EC-EARTH_decadal1965_r8i1p1_196511-197610.nc|application/netcdf|HTTPServer&fields=*&distrib=true&limit=100&type=File&format=application%2Fsolr%2Bxml&offset=0
    #
    parameters['url']=[None]

    return parameters

def remove_unused_parameters(parameters):
    """Remove unused parameters.

    Note
        If those parameters are used in the future, you may remove this func,
        but note that duplicates will occur because of that.

        e.g.
        sqlite> select * from param where value='wind_speed';
        cf_standard_name|wind_speed
        variable|wind_speed
        
        and this will show the warning below as a consequence

        $ synda search CMIP5 wind_speed| more
        WARNING: 'wind_speed' value has been associated with 'cf_standard_name' facet.
    """

    if 'cf_standard_name' in parameters:
        del parameters['cf_standard_name']
    if 'variable_long_name' in parameters:
        del parameters['variable_long_name']

    return parameters

def select_project(project_list):
    project_names=[item.name for item in project_list]
    if 'CMIP5' in project_names:
        # default to 'CMIP5'

        return 'CMIP5'
    else:
        # if 'CMIP5' doesn't exists, return the first project in the list

        return project_names[0]

def get_parameters_from_searchapi(host,project,dry_run=False):
    """Method used to retrieve parameters list from search-API

    Sample queries
        http://esg-datanode.jpl.nasa.gov/esg-search/search?facets=model&limit=0 
        http://esg-datanode.jpl.nasa.gov/esg-search/search?facets=*&limit=0

    Note
        for now, parameters based processing like parameters caching,
        parameters checking and parameters inference are not project aware
        (i.e. the url retrieve all parameters regardless of the project).
        There is a 'project' parameter in this func, but it's only used
        for the third query.

    TODO
        maybe run the third query for every project, so to have the full list
        of parameter.
    """
    #sdtools.print_stderr("Using '%s' index"%host)

    #sdprogress.SDProgressDot.print_char()

    params={}

    # First pass to retrieve most parameters. TAG4353453453
    d=sdremoteparam_light.run(facets_group={'type':['Dataset']},dry_run=dry_run,host=host)
    params.update(d)

    #sdprogress.SDProgressDot.print_char()

    # Second pass needed as some parameters are missing when using 'facets=*' (currently, only for 'index_node' parameter)
    d=sdremoteparam_light.run(pname='index_node',facets_group={'type':['Dataset']},dry_run=dry_run,host=host)
    params.update(d)

    #sdprogress.SDProgressDot.print_char()

    if project is None:
        if 'project' in params:
            assert isinstance(params['project'],list)
            if len(params['project'])>0:
                project=select_project(params['project'])

    # Hack
    #
    # 'version' have many predefined values from above queries, but shouldn't.
    # This is because of the way solar query works (TBC).
    #
    # To fix the problem, we remove 'version' (fetched from previous queries).
    # 'version' will be added by the get_one_file() method below as a FREE-parameter.
    #
    # Note: the same problem may occur for other search-api parameter
    #
    try:
        del params['version']
    except:
        pass

    # Third pass to fetch file attributes which can also be used as search criterias (e.g. title). TAG543534563
    #
    # Note:
    #   Those attributes are added without corresponding values 
    #   (i.e. it's only used for name checking, not for value checking)
    #
    # TODO: 
    #   Maybe do this for each project (to retrieve project specific attributes)
    #
    file_=sdproxy_ra.get_one_file(host,project)

    assert file_ is not None # just in case


    # WARNING
    #
    # This code does not work for all parameters (e.g. url), as:
    #     - type issue in the xml returned by search-api (i.e. some parameter
    #       are not scalar (e.g. url))
    #     - call_web_service() method returns not the exact search-api xml, but
    #       altered result (e.g. url_http is returned instead of url)


    for attribute_name in file_:
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
