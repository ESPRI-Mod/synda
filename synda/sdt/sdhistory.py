#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains local repository changelog routines.

Note
    Local repository changelog is stored in 'history' table.
"""

import os
from synda.sdt import sdapp
from synda.sdt import sdutils
from synda.sdt import sdhistorydao

from synda.source.config.input.constants import USER_INPUT_TYPES


def previous_run_exists(selection_filename, action):
    li = sdhistorydao.get_history_lines(
        selection_filename=selection_filename,
        action=action,
    )

    if len(li) > 0:
        return True
    else:
        return False


def get_previous_run(selection_filename, action):
    return sdhistorydao.get_latest_history_line(
        selection_filename=selection_filename,
        action=action,
    )


def file_changed_since_last_run(selection_file, action):

    # retrieve current checksum
    current_checksum = sdutils.compute_checksum(selection_file)

    # retrieve previous run checksum
    selection_filename = os.path.basename(selection_file)
    previous_run = get_previous_run(selection_filename, action)
    previous_checksum = previous_run['selection_file_checksum']

    return previous_checksum == current_checksum


def add_history_line(action=None, selection_file=None, insertion_group_id=None, crea_date=None):

    # check
    assert action is not None
    assert selection_file is not None

    # compute checksum
    if selection_file == USER_INPUT_TYPES["cmdline"]:
        cs = None
    else:
        cs = sdutils.compute_checksum(selection_file)

    # main
    selection_filename = os.path.basename(selection_file)
    sdhistorydao.add_history_line(
        action,
        selection_filename=selection_filename,
        insertion_group_id=insertion_group_id,
        crea_date=crea_date,
        selection_file_checksum=cs,
    )
