#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script runs "dataset" pipeline's jobs."""

from sdt.bin.commons.utils import sdprepare_dataset_attr
from sdt.bin.commons.utils import sdlocalpath
from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils.sdexception import SDException
from sdt.bin.commons.facets import sdremoveaggregation
from sdt.bin.commons.search import sdcomplete
from sdt.bin.commons.pipeline import sdstatusfilter


def run(**kw):
    files = kw.get('files')
    check_type(files)
    files = sdremoveaggregation.run(files)
    files = sdprepare_dataset_attr.run(files)
    files = sdlocalpath.run(files, mode='dataset')
    files = sdcomplete.run(files)
    files = sdstatusfilter.run(files)
    return files


def check_type(files):
    for f in files:
        type = f['type']
        if type != sdconst.SA_TYPE_DATASET:
            raise SDException('SDDAPIPE-001', 'Incorrect type (%s)' % type)
