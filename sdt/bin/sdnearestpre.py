#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This filter select the nearest replica using geolocation routines.

Notes
    - This module is called 'sdnearestpre' as it operates pre-call (i.e. after the search-API call).
    - 'sdnearestpre' and 'sdnearestpost' modules are independant but also mutually exclusive (don't see any reason of using both at the same time).
"""

import os
import argparse
import json
import sdconfig
import sdremoteparam
from sdexception import SDException
import sdi18n
import sdcliex
import sdpipeline
import sdnearestutils

def run(facets_groups,show_candidate=False,dry_run=False):
    for facets_group in facets_groups:

        nearest=facets_group.get('nearest','false')
        if nearest=='true':

            if 'data_node' not in facets_group: # do not find the nearest if 'data_node' has been set by user (i.e. trust user choice)

                # be sure to remove 'replica' as we want to search for the nearest in all existing copies of the file.
                if 'replica' in facets_group:
                    del facets_group['replica']

                li=get_datanode_list(facets_group,dry_run=dry_run)

                if show_candidate:
                    print "Candidate datanodes list:"
                    for dn in li:
                        print dn

                if len(li)>0:
                    data_node=get_nearest_datanode(li)
                    facets_group['data_node']=data_node

            else:
                # if 'data_node' already set, do nothing

                pass

    return facets_groups

def get_datanode_list(facets_group,dry_run=False):
    params=sdremoteparam.run(pname='data_node',facets_group=facets_group,dry_run=dry_run)
    items=params.get('data_node',[])
    return [i.name for i in items]

def get_nearest_datanode(datanodes):
    client_place=sdnearestutils.get_client_place() # our location

    # init min distance with the first datanode (arbitrary)
    nearest_datanode=datanodes[0]
    datanode_place=sdnearestutils.get_datanode_place(nearest_datanode)
    min_distance=sdnearestutils.compute_distance(client_place,datanode_place)

    for datanode in datanodes:
        datanode_place=sdnearestutils.get_datanode_place(datanode)
        distance=sdnearestutils.compute_distance(client_place,datanode_place)

        if distance<min_distance:
            nearest_datanode=datanode

    return nearest_datanode

if __name__ == '__main__':
    prog=os.path.basename(__file__)
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, epilog="""examples of use
  %s -d %s
%s
    """%(prog,'esg-datanode.jpl.nasa.gov',sdcliex.search(prog)))

    parser.add_argument('parameter',nargs='*',default=[],help=sdi18n.m0001)
    parser.add_argument('-d', '--datanode',help='e.g. esgnode2.nci.org.au')
    parser.add_argument('-s', '--show_candidate',action='store_true')
    parser.add_argument('-y', '--dry_run',action='store_true')
    args = parser.parse_args()

    if args.datanode is not None:
        # compute distance between us and the datanode

        client_place=sdnearestutils.get_client_place() # our location
        datanode_place=sdnearestutils.get_datanode_place(args.datanode)
        distance=sdnearestutils.compute_distance(client_place,datanode_place)

        print "The datanode is %i km from your location (%s)"%(distance,sdnearestutils.get_client_country())
    else:
        # choose the nearest datanode for given parameters

        if len(args.parameter)>0:
            facets_groups=sdpipeline.prepare_param(parameter=args.parameter)

            # enable nearest
            for facets_group in facets_groups:
                facets_group['nearest']='true'

            facets_groups=run(facets_groups,show_candidate=args.show_candidate,dry_run=args.dry_run)
            facets_group=facets_groups[0]

            if 'data_node' in facets_group:
                print
                print "Nearest datanode: %s"%facets_group['data_node']
            else:
                if not args.dry_run:
                    print
                    print "No datanode found"
