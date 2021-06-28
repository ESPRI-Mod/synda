#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from synda.sdt import sddquery
from synda.sdt import sdremotequtils
from synda.sdt import sdnetutils
from synda.sdt import sdindex
from synda.sdt import sdi18n
from synda.sdt import sdcliex


def run(pname=None, host=None, facets_group=None, dry_run=False, fields=None):
    """
    Returns:
        Dict of list of 'Item' object
    """

    if facets_group is None:
        facets_group = {}

    assert isinstance(facets_group, dict)

    # keep only search-API parameter
    facets_group = sddquery.search_api_parameters(facets_group)

    # set parameter name
    if pname is None:
        facets_group['facets'] = ['*']
    else:
        facets_group['facets'] = [pname]

    # force 'limit' to 0
    facets_group['limit'] = ['0']

    # set default type
    if 'type' not in facets_group:
        facets_group['type'] = ['File']

    # force 'fields' to '*'
    # TODO: maybe this is not needed to retrieve parameter (maybe we can set 'fields' only to 'id',
    #  or something like that)

    if not fields:
        facets_group['fields'] = ['*']
    else:
        facets_group['fields'] = fields
    # set index host
    host = sdindex.get_default_index() if host is None else host

    # build url
    url = sdremotequtils.build_url(facets_group, host)

    if dry_run:
        print(url)
        return {}

    # retrieve parameters
    params = sdnetutils.call_param_web_service(url, 60)

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

    from synda.sdt import sdpipeline # BEWARE: keep it here because of circular dependency problem here: see TAG3434 tag in TODO file
    facets_groups=sdpipeline.prepare_param(parameter=args.parameter)
    facets_group=facets_groups[0]
    params=run(pname=args.name,facets_group=facets_group,dry_run=args.dry_run,host=args.host)

    if len(params)>0:
        for name,values in params.items():
            for value in values:
                print('%s => %s'%(name, value.name))
