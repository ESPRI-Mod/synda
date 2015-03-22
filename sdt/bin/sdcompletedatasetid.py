#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdcompletedatasetid.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module add data_node to dataset_id in case dataset_id is set without data_node in selection file.

Notes
  - This module make possible to search files using reduced dataset_id (aka
    instance_id aka dataset_functional_id).
  - If 'data_node' is set in selection file use it, else use choose data_node
    depending on 'replica' flag (if set to false, use master data_node, if set
    to true use a random replica data_node).
  - This filter maybe be deprecated because of this:
     - it IS possible to use type=File and dataset_id WITHOUT DATA_NODE
        - example
           - http://esgf-index1.ceda.ac.uk/esg-search/search?query=cmip5.output1.MIROC.MIROC4h.rcp45.6hr.atmos.6hrLev.r1i1p1.v20110926
              - gives two datasets
           - http://esgf-index1.ceda.ac.uk/esg-search/search?type=File&query=cmip5.output1.MIROC.MIROC4h.rcp45.6hr.atmos.6hrLev.r1i1p1.v20110926
              - gives all files of the two datasets
        - the only thing to be careful of is replica
          (in the example above, both found datasets are the same, one is the master, one is a replica)
"""

import sys
import argparse
import json
import random
import sdapp
import sdprint
import sdquicksearch

def run(facets_groups):
    for facets_group in facets_groups:
        if 'dataset_id' in facets_group:
            dataset_id_list=facets_group['dataset_id'] # dataset_id is a list of values

            new_values=[]

            for dataset_id in dataset_id_list: 
                if is_data_node_present_in_dataset_id(dataset_id):
                    new_values.append(dataset_id)
                else:
                    instance_id=dataset_id # meaningfull as instance_id is dataset_id without data_node
                    new_values.append(instance_id_to_dataset_id(instance_id,facets_group))

            facets_group['dataset_id']=new_values

    return facets_groups

def instance_id_to_dataset_id(instance_id,facets_group):
    if "data_node" in facets_group:
        return "%s|%s"%(instance_id,facets_group['data_node'])
    else:
        replica=facets_group['replica'] if "replica" in facets_group else None
        return retrieve_full_dataset_id(instance_id,replica)

def retrieve_full_dataset_id(instance_id,replica):
    """Retrieve missing data_node from search-API."""

    if replica is None:
        replica=['false'] # if replica flag not present, let's choose the master (arbitrary choice)

    # list to scalar
    replica=replica[0]

    # search-API call
    datanodes=get_data_nodes(instance_id,replica)

    if replica=='true':
        # retrieve a random replica data_node

        if len(datanodes)>0:
            return "%s|%s"%(instance_id, random.choice(datanodes))
        else:
            return instance_id # datanode not found, don't change anything

    elif replica=='false':
        # retrieve master data_node

        if len(datanodes)==1:
            return "%s|%s"%(instance_id,datanodes[0])
        else:
            return instance_id # datanode not found, don't change anything

def get_data_nodes(instance_id,replica_scalar):
    """Return one or more data_nodes depending on the 'replica' flag."""

    parameter=['limit=50','type=Dataset','instance_id=%s'%instance_id,'replica=%s'%replica_scalar]

    # debug
    #print parameter

    result=sdquicksearch.run(parameter=parameter,post_pipeline_mode=None,dry_run=False)
    if result.num_result>0:

        datanodes=[]
        for d in result.files:
            datanodes.append(d['data_node'])

        return datanodes
    else: 
        return []

def is_data_node_present_in_dataset_id(dataset_id):
    """Check whether data_node is present in the dataset_id."""

    if '|' in dataset_id:
        return True

    """
    if '%7C' in dataset_id:
        return True
    """

    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    facets_groups=json.load(sys.stdin)
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
