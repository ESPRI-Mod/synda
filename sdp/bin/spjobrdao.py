#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: spjobrdao.py 3049 2014-02-09 15:52:49Z jripsl $
#  @version        $Rev: 3049 $
#  @lastrevision   $Date: 2014-02-09 16:52:49 +0100 (Sun, 09 Feb 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Contains jobrun DAO SQL queries."""

import spapp
import spsqlutils

def add_jobrun(jobrun,conn):
    keys_to_insert=['ppprun_id', 'transition', 'start_date', 'end_date', 'duration', 'status', 'error_msg', 'runlog']
    spsqlutils.insert(jobrun,keys_to_insert,conn)
