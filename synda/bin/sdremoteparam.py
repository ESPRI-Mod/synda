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
"""

import os
import argparse
import sdapp
import sdconst
import sdi18n
import sdcliex
import sdpipeline
import sddenormodel
import sdremoteparam_light

def run(pname=None,host=None,facets_group=None,dry_run=False):
    """
    Args:
        facets_group: if present, only parameter matching facets_group filter are returned

    Returns:
        Dict of list of 'Item' object
    """

    if facets_group is None:
        facets_group={}

    assert isinstance(facets_group,dict)

    # denorm. model
    facets_groups=sddenormodel.run([facets_group])
    facets_group=facets_groups[0]

    params=sdremoteparam_light.run(pname=pname,host=host,facets_group=facets_group,dry_run=dry_run)

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

    facets_groups=sdpipeline.prepare_param(parameter=args.parameter)
    facets_group=facets_groups[0]
    params=run(pname=args.name,facets_group=facets_group,dry_run=args.dry_run,host=args.host)

    if len(params)>0:
        for name,values in params.iteritems():
            for value in values:
                print '%s => %s'%(name, value.name)
