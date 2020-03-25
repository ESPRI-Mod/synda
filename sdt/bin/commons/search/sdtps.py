#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module pre-fetch the list of datasets matching a selection to improve global performance.

It operates by first retrieving matching datasets (using type=Dataset), then
passing the datasets list to the second query (which use type=File) to retrieve
the files. The gain come from the fact that dataset id index gives better result
than using separate facets.

Notes
    - sdtps means 'SynDa Two Phases Search'
    - this filter is experimental (not sure if the gain from fast indexing bypass the cost of having to do multiple
    search-api calls.. to be tested)
"""

import sys
import argparse
import json
import copy
from sdt.bin.commons.search import sdremoteqbuilder
from sdt.bin.commons.search import sdexplode
from sdt.bin.commons.search import sdrun
from sdt.bin.commons.utils import sdprint
from sdt.bin.commons.pipeline import sdpipeline


def run(facets_groups):
    # check (this filter cannot be used if 'query' search-api parameter has been set by user)
    for facets_group in facets_groups:
        if 'query' in facets_group:
            return facets_group

    for facets_group in facets_groups:

        tps = facets_group.get('tps', 'false')
        if tps == 'true':

            # duplicate not to corrupt original query
            facets_group_cpy = copy.deepcopy(facets_group)

            # force type
            facets_group_cpy['type'] = ['Dataset']

            # remove some keys
            try:
                del facets_group_cpy['tps']
                del facets_group_cpy['limit']
            except:
                pass

            # build n run
            # we need to process one facets group at a time, as each datasets list is facets group specific
            queries = sdremoteqbuilder.run([facets_group_cpy])
            metadata = sdrun.run(queries)
            metadata = sdpipeline.post_pipeline(metadata, 'generic')

            datasets = metadata.get_files()  # warning: load list in memory

            if len(datasets) > 0:
                if explode_on_instance_id:
                    facets_group['query'] = [dataset['instance_id'] for dataset in datasets]
                else:
                    facets_group['query'] = ['%20OR%20'.join([dataset['instance_id'] for dataset in datasets])]
            else:
                # reason we are here maybe because 'First Phase Request' failed and thus returned no datasets

                pass

    if explode_on_instance_id:
        facets_groups = sdexplode.run(facets_groups, facet_to_explode='query')

    return facets_groups
