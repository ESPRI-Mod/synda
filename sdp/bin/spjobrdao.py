#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains jobrun DAO SQL queries."""

import spapp
import spsqlutils

def add_jobrun(jobrun,conn):
    keys_to_insert=['ppprun_id', 'transition', 'start_date', 'end_date', 'duration', 'status', 'error_msg', 'runlog']
    spsqlutils.insert(jobrun,keys_to_insert,conn)
