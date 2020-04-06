#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains post-processing order related routines.

Note
    'sdpporder' stands for 'SynDa Post-Processing order'
"""
from sdt.bin.db import dao
from sdt.bin.db import session
from sdt.bin.db import models
from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils import sdtime
from sdt.bin.commons.utils import sdlog
from sdt.bin.commons.utils import sdproduct


# TODO: replace single quote with None and move 'None2SingleQuote' processing inside Event object
# (and add comment about why we use single quote instead of None in event table !!!)


def submit(order_name, project, model, dataset, variable='', filename=''):
    event_name = order_name
    dataset_pattern = sdproduct.replace_output12_product_with_wildcard(dataset)
    filename_pattern = filename
    sdlog.info("SDPPORDE-001", "'{}' triggered ({},{})".format(event_name, dataset_pattern, variable))
    event = models.Event(name=event_name, project=project, model=model, dataset_pattern=dataset_pattern,
                         variable=variable, filename_pattern=filename_pattern, crea_date=sdtime.now(),
                         priority=sdconst.DEFAULT_PRIORITY)
    with session.create():
        dao.add_event(event)
