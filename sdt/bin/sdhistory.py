#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

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

import sdapp
import sdhistorydao

def previous_run_exists(selection_filename,action):
    li=sdhistorydao.get_history_lines(selection_filename=selection_filename,action=action)

    if len(li)>0:
        return True
    else:
        return False

def get_previous_run(selection_filename,action):
    di=sdhistorydao.get_latest_history_line(selection_filename=selection_filename,action=action)
    return di
