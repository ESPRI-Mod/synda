# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
VARIABLE_COMPLETE = "complete"
VARIABLE_NOT_COMPLETE = "not_complete"

STATUS = dict(
    complete=VARIABLE_COMPLETE,
    not_complete=VARIABLE_NOT_COMPLETE,
)

STATUSES_ALL = [
    VARIABLE_COMPLETE,
    VARIABLE_NOT_COMPLETE,
]

STRUCTURE = dict(
    statuses=dict(
        all=STATUSES_ALL,
    ),
    status=STATUS,
)
