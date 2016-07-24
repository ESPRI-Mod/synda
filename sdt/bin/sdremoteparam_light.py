#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module builds and submit search-API *parameter* query.

Reference
    - https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API

Note
    This module do not contain model-denormalization. If you need
    model-denormalization, use 'sdremoteparam' module. model-denormalization has
    been removed here in order to prevent circular reference (i.e. sdcache use
    sdremoteparam use sddenormodel use sdparam use sdcache).
"""

import os
import argparse
import sdapp
import sdconst
import sddquery
import sdremotequtils
import sdnetutils
import sdindex
import sdi18n
import sdcliex

def run(pname=None,host=None,facets_group=None,dry_run=False):
    """
    Returns:
        Dict of list of 'Item' object
    """

    if facets_group is None:
        facets_group={}

    assert isinstance(facets_group,dict)

    # keep only search-API parameter
    facets_group=sddquery.search_api_parameters(facets_group)

    # set parameter name
    if pname is None:
        facets_group['facets']=['*']
    else:
        facets_group['facets']=[pname]

    # force 'limit' to 0
    facets_group['limit']=['0']

    # set default type
    if 'type' not in facets_group:
        facets_group['type']=['File']

    # force 'fields' to '*'
    facets_group['fields']=['*'] # TODO: maybe this is not needed to retrieve parameter (maybe we can set 'fields' only to 'id', or something like that)

    # set index host
    host=sdindex.get_default_index() if host is None else host

    # build url
    url=sdremotequtils.build_url(facets_group,host)

    if dry_run:
        print url
        return {}

    # retrieve parameters
    params=sdnetutils.call_param_web_service(url,60)

    return params

# init.

if __name__ == '__main__':
    prog=os.path.basename(__file__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog="""examples of use
%s
    """%sdcliex.search(prog))

    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)
    parser.add_argument('-H','--host',help='Index hostname')
    parser.add_argument('-n','--name',help='Parameter name to be retrieve')
    parser.add_argument('-y','--dry_run',action='store_true')
    args = parser.parse_args()

    import sdpipeline # BEWARE: keep it here because of circular dependency problem here: see TAG3434 tag in TODO file
    facets_groups=sdpipeline.prepare_param(parameter=args.parameter)
    facets_group=facets_groups[0]
    params=run(pname=args.name,facets_group=facets_group,dry_run=args.dry_run,host=args.host)

    if len(params)>0:
        for name,values in params.iteritems():
            for value in values:
                print '%s => %s'%(name, value.name)
