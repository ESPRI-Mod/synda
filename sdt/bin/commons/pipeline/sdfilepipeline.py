#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script runs "file" pipeline's jobs.

Usage
 - cat file | sdfilepipeline -
 - cat file | sdfilepipeline
 - sdfilepipeline file
"""

from sdt.bin.commons.utils import sdreducerow
from sdt.bin.commons.utils import sdtimefilter
from sdt.bin.commons.utils import sdprotocol
from sdt.bin.commons.utils import sdtransform
from sdt.bin.commons.utils import sdlocalpath
from sdt.bin.commons.utils import sdprepare_file_attr
from sdt.bin.commons.utils import sdprepare_dataset_attr
from sdt.bin.commons.esgf import sdnormalize
from sdt.bin.commons.search import sdcomplete
from sdt.bin.commons.facets import sdremoveaggregation
from sdt.bin.commons.pipeline import sdstatusfilter
from sdt.bin.commons.utils.sdexception import SDException


def run(**kw):
    files = kw.get('files')
    check_type(files)
    check_fields(files)
    files = sdreducerow.run(files)
    files = sdremoveaggregation.run(files)
    files = sdprotocol.run(files)
    files = sdtimefilter.run(files)
    files = sdtransform.run(files)
    files = sdprepare_dataset_attr.run(files)
    # files=sdcheck_dataset_template.run(files)

    # we do not remove the number of column here anymore
    #
    # Notes
    #     - not reducing the number of column here may slightly diminish
    #       performance (memory, cpu). But as we do need those informations (e.g.
    #       description, variable_long_name, facets..), we have no choice.
    #     - we need to keep those informations even if they are not essential,
    #       as we will need them soon to provide more descriptive informations to
    #       the user (e.g. description, variable_long_name..)
    #     - we need to keep all facets so the user can build custom local path
    #       (see local_path_custom_transform() func for more info)
    #     - we will now remove those column downstream (but only for 'dump' action)
    #
    # files=sdreducecol.run(files)

    files = sdnormalize.normalize_files(files)
    files = sdprepare_file_attr.run(files)
    files = sdlocalpath.run(files)

    # EXT_FILE_POST
    #
    # load extensions here
    #
    # TODO

    files = sdcomplete.run(files)

    files = sdstatusfilter.run(files)

    return files


def check_type(files):
    for f in files:
        type = f['type']
        if type != 'File':
            raise SDException('SDFIPIPE-001', 'Incorrect type ({})'.format(type))


def check_fields(files):
    """
    This func is to prevent user to set 'fields' attribute
    (this attribute is set only by the program, in specific cases).
    """

    for f in files:
        if 'fields' in f:
            raise SDException('SDFIPIPE-002', "'fields' parameter can't be used in "
                                              "'file' pipeline (fields={})".format(f['fields']))
