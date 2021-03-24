#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains 'attached_parameters' addition routine."""

import copy
from synda.sdt import sdapp
from synda.sdt import sdlog
from synda.sdt import sdtypes
from synda.sdt import sdpipelineprocessing


def run(o, attached_parameters):
    """This func adds some parameters to the result of a query.
    
    Note
        The idea is the keep some parameters around by making them jump
        over the search call (e.g. Search-api call, SQL call..), from
        'query pipeline' to 'file pipeline'.
    """
    assert isinstance(attached_parameters, dict)

    sdlog.debug("SYDADDAP-620", "Add attached_parameters..")

    if isinstance(o, sdtypes.Metadata):

        po = sdpipelineprocessing.ProcessingObject(
            add_attached_parameters,
            attached_parameters,
        )

        o = sdpipelineprocessing.run_pipeline(o, po)

    elif isinstance(o, sdtypes.Response):

        # no need to process chunk by chunk here as Response size only contains a small amount of data
        # (< Preferences().api_esgf_search_chunksize)

        files = add_attached_parameters(
            o.get_files(),
            attached_parameters,
        )

        o.set_files(files)

    else:
        assert False

    sdlog.debug("SYDADDAP-628", "attached_parameters added")

    return o


def add_attached_parameters(files, attached_parameters):
    for f in files:
        assert 'attached_parameters' not in f
        f['attached_parameters'] = copy.deepcopy(attached_parameters)
    return files
