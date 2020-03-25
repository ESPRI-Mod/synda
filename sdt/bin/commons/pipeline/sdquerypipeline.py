#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains "query" pipeline's jobs.

Notes
    - Depending on the mode (local or remote), 'query' pipeline builds SQL query or Search-API query.
    - This pipeline is used to retrieve file or dataset from search-API.
    - This pipeline run *before* the main search-api call.
    - This pipeline use sdparampipeline module.
"""

import os
import argparse

from sdt.bin.commons.utils import sdparse
from sdt.bin.commons.utils import sdconfig
from sdt.bin.commons.utils import sdprint
from sdt.bin.commons.utils.sdexception import SDException
from sdt.bin.commons.param import sdbuffer
from sdt.bin.commons.search import sdparampipeline
from sdt.bin.commons.search import sdexplode

# TODO needs rewriting to suit sqlalchemy style query.
# Could be left as a raw_query
from sdt.bin.commons.search import sdremoteqbuilder
from sdt.bin.commons.search import sdtps
from sdt.bin.commons.esgf import sdcompletedatasetid
from sdt.bin.commons.esgf import sdindexhost
from sdt.bin.commons.esgf import sdremote2local
from sdt.bin.commons.esgf import sdlocalvalue2remotevalue
from sdt.bin.commons.esgf import sdnearestpre


def run(facets_groups, parallel=True, index_host=None, dry_run=False, query_type='remote'):
    facets_groups = sdparampipeline.run(facets_groups)
    if query_type == 'remote':
        # both filters below transform attributes to fit search-api special syntax
        # (e.g. suffix added to id and url, using '|' as delimiter)
        if sdconfig.dataset_filter_mecanism_in_file_context == 'dataset_id':
            # beware: this triggers a search-api call
            facets_groups = sdcompletedatasetid.run(facets_groups)

        facets_groups = sdlocalvalue2remotevalue.run(facets_groups)

        # EXT_FILE_PRE
        #
        # load extensions here
        #
        # TODO

        facets_groups = sdindexhost.run(facets_groups, parallel=parallel, index_host=index_host, dry_run=dry_run)
        # facets_groups=sdexplode.run(facets_groups) # ,facet_to_explode='filename'

        # experimental
        if sdconfig.nearest_schedule == 'pre':
            facets_groups = sdexplode.run(facets_groups)  # maybe this is not needed (to be confirmed)
            facets_groups = sdnearestpre.run(facets_groups)

        if sdconfig.twophasesearch:
            facets_groups = sdtps.run(facets_groups)  # two phase search

        queries = sdremoteqbuilder.run(facets_groups)
    elif query_type == 'local':
        facets_groups = sdremote2local.run(facets_groups)
        queries = sdlocalqbuilder.run(facets_groups)
    else:
        raise SDException("SDQUERYP-001", "Unknow query type ({})".format(query_type))

    return queries
