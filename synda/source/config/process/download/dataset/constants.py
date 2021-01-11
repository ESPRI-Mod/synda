# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

# this means it has never been retrieved yet
DATASET_STATUS_NEW = "new"
# this means there is no complete variables yet in the dataset (although there may be many files already downloaded)
DATASET_STATUS_EMPTY = "empty"
# this means there is at least one complete variable in the dataset
DATASET_STATUS_IN_PROGRESS = "in-progress"
# complete here is related to selection (i.e. it doesn't mean that of variable of the dataset are done)
DATASET_STATUS_COMPLETE = "complete"


ALL_STATUSES = [
    DATASET_STATUS_NEW,
    DATASET_STATUS_EMPTY,
    DATASET_STATUS_IN_PROGRESS,
    DATASET_STATUS_COMPLETE
]

STRUCTURE = dict(
    statuses=dict(
        all=ALL_STATUSES,
    ),
    status=dict(
        new=DATASET_STATUS_NEW,
        empty=DATASET_STATUS_EMPTY,
        in_progress=DATASET_STATUS_IN_PROGRESS,
        complete=DATASET_STATUS_COMPLETE,
    ),
)
