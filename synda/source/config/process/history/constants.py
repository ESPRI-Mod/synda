# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
ACTION_ADD = 'add'
ACTION_DELETE = 'delete'

ACTIONS = [
    ACTION_ADD,
    ACTION_DELETE,
]

STRUCTURE = dict(
    action=dict(
        add=ACTION_ADD,
        delete=ACTION_DELETE,

    ),
    actions=ACTIONS,
)
