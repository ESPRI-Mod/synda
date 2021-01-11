# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
"""
Variables used during SELECTION proceses
"""
IDENTIFIER = "selection"

# means it has never been retrieved yet
SELECTION_STATUS_NEW = "new"

# means the selection has new modifications since the last run
SELECTION_STATUS_MODIFIED = "modified"

# means no modification since the last run (and last run complete successfully)
SELECTION_STATUS_NORMAL = "normal"

ALL_STATUSES = [
    SELECTION_STATUS_NEW,
    SELECTION_STATUS_MODIFIED,
    SELECTION_STATUS_NORMAL,
]

STRUCTURE = dict(
    statuses=dict(
        all=ALL_STATUSES,
    ),
    status=dict(
        new=SELECTION_STATUS_NEW,
        modified=SELECTION_STATUS_MODIFIED,
        normal=SELECTION_STATUS_NORMAL,
    ),
)
