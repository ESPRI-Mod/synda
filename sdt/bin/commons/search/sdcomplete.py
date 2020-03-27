#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright œ(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Add local files attributes after search-API call.

Description
    - If file already exist locally, this module completes file with
      informations coming from local database.
    - If file doesn't exist locally, this module completes file with default
      values.

Notes
  - This module can be used to process different metadata types (File and Dataset).
  - Some attributes may exist both at file level (A) and at
    file['attached_parameters'] level (B). This is normal: A attributes are
    final values and B attributes are input values coming from end-user.
"""

from sdt.bin.commons.pipeline import sdpostpipelineutils
from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils.sdexception import SDException
from sdt.bin.db import dao
from sdt.bin.db import session


def run(files):
    check_collision(files)
    files = complete(files)
    return files


def complete(files):
    for f in files:

        # the if/else block below is because this module can be used
        # to process different metadata type (File and Dataset).
        with session.create():
            if f["type"] == sdconst.SA_TYPE_FILE:
                transfer = dao.get_files(file_functional_id=f['file_functional_id'], limit=1)
                if transfer is not None and transfer != []:
                    f['status'] = transfer.status
                    # this is to allow setting priority using selection parameter (i.e. default priority can be
                    # overriden using selection parameter). It is usefull here for example when user wants to change
                    # priority. (YES, a search-API request is needed in this case!).
                    if sdpostpipelineutils.exists_attached_parameter(f, 'priority'):
                        f['priority'] = sdpostpipelineutils.get_attached_parameter(f, 'priority')
                    else:
                        f['priority'] = transfer.priority
                else:
                    f['status'] = sdconst.TRANSFER_STATUS_NEW
                    # this is to allow setting priority using selection parameter (i.e. default priority can be
                    # overridden using selection parameter). This is useful here to set special priority for new files.
                    if sdpostpipelineutils.exists_attached_parameter(f, 'priority'):
                        f['priority'] = sdpostpipelineutils.get_attached_parameter(f, 'priority')
                    else:
                        f['priority'] = sdconst.DEFAULT_PRIORITY

            elif f["type"] == sdconst.SA_TYPE_DATASET:
                dataset = dao.get_dataset(dataset_functional_id=f['dataset_functional_id'])
                if dataset is not None:
                    f['status'] = dataset.status
                else:
                    f['status'] = sdconst.DATASET_STATUS_NEW
            else:
                raise SDException('SDCOMPLE-001', 'Incorrect type ({})'.format(f["type"]))

    return files


def check_collision(files):
    for f in files:
        if 'status' in f:
            raise SDException("SDCOMPLE-032", "incorrect field")
        if 'priority' in f:
            raise SDException("SDCOMPLE-033", "incorrect field")
