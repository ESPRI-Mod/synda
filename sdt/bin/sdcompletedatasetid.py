#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module add data_node to dataset_functional_id.

Notes
    - This module is useful for example to transform dataset_functional_id to ESGF dataset_id (aka ESGF id).
    - The datanode used is retrieve from ESGF and can be a replica datanode or a master datanode
    - If a standalone data_node facet is present, it takes the lead and is used in priority.
    - This module makes possible to search files using dataset instance_id aka dataset_functional_id.
    - In this module, input dataset_id can be one of two things:
        - 'ESGF dataset_id' (i.e. including the data_node)
        - dataset_functional_id (i.e. without the data_node)
    - In this module, output dataset_id is 'ESGF dataset_id' (i.e. including the
      data_node), except if no data_node is found, in which case output
      dataset_id is the dataset_functional_id (i.e. without the data_node).
    - Choose data_node depending on 'replica' flag (if set to false, use master
      data_node, if set to true use a random replica data_node).
    - This filter maybe be deprecated because of this:
         - it IS possible to send a search-API request with type=File and dataset_functional_id (i.e. without data_node)
              - example
                   - http://esgf-index1.ceda.ac.uk/esg-search/search?query=cmip5.output1.MIROC.MIROC4h.rcp45.6hr.atmos.6hrLev.r1i1p1.v20110926
                        - gives two datasets
                   - http://esgf-index1.ceda.ac.uk/esg-search/search?type=File&query=cmip5.output1.MIROC.MIROC4h.rcp45.6hr.atmos.6hrLev.r1i1p1.v20110926
                        - gives all files of the two datasets
              - the only thing to be careful of is replica
                (in the example above, both found datasets are the same, one is the master, one is a replica)
        - well maybe not
               - it is possible, but it seems not reliable
                    - see TAG543N45K3KJK
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
            dataset_id_list=facets_group['dataset_id'] # This is normal: dataset_id IS a list of values (MEMO: this module is used to build the query (i.e. not used after the search-api call))

            new_values=[]

            for dataset_id in dataset_id_list: 
                if is_data_node_present_in_dataset_id(dataset_id):
                    new_values.append(dataset_id)
                else:
                    instance_id=dataset_id # meaningfull as instance_id is dataset_id without data_node
                    new_values.append(instance_id_to_dataset_id(instance_id,facets_group))

            facets_group['dataset_id']=new_values # This is normal: dataset_id IS a list of values (MEMO: this module is used to build the query (i.e. not used after the search-api call))

    return facets_groups

def instance_id_to_dataset_id(instance_id,facets_group):
    if "data_node" in facets_group:

        # This block handles cases like this one
        #  synda get cmip5.output1.CCCma.CanCM4.decadal1972.fx.atmos.fx.r0i0p0.v20120601 esgf2.dkrz.de

        li=facets_group['data_node']

        assert len(li)==1 # arbitrary (TODO: maybe this is too restrictive)

        dnode=li[0]

        return "%s|%s"%(instance_id,dnode)
    else:
        replica=facets_group['replica'] if "replica" in facets_group else None

        if replica is None:

            # force value for replica if not present
            #
            #replica='false' # if replica flag not present, let's choose the master (arbitrary choice)


            # leave as None so to match master as well as replica in a random way
            pass

        else:
            replica=replica[0] # list to scalar

        # at this point, replica can be: 'true','false',None

        return retrieve_full_dataset_id(instance_id,replica)

def retrieve_full_dataset_id(instance_id,replica):
    """Retrieve missing data_node from search-API."""

    # search-API call
    datanodes=get_data_nodes(instance_id,replica)

    if len(datanodes)<1:
        return instance_id # datanode not found, don't change anything
    else:

        if replica is None:
            data_node=random.choice(datanodes) # retrieve random replica or master data_node
        elif replica=='true':
            data_node=random.choice(datanodes) # retrieve a random replica data_node
        elif replica=='false':
            data_node=datanodes[0] # retrieve master data_node

        return "%s|%s"%(instance_id,data_node)

def get_data_nodes(instance_id,replica):
    """Return one or more data_nodes depending on the 'replica' flag."""

    parameter=['limit=50','type=Dataset','instance_id=%s'%instance_id]

    if replica is not None:
        parameter.append('replica=%s'%replica)

    # debug
    #print parameter

    result=sdquicksearch.run(parameter=parameter,post_pipeline_mode=None,dry_run=False)
    if result.count()>0:

        datanodes=[]
        for d in result.get_files():
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
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    facets_groups=json.load(sys.stdin)
    facets_groups=run(facets_groups)
    sdprint.print_format(facets_groups,args.format,args.print_only_one_item)
