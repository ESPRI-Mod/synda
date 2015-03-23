#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sptypes.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains core classes.

Note
    This module contains only instantiable classes (i.e. no static class)
"""

import spapp
import spconst
import json

class PPPRun(): # 'PPPRun' means 'Post-Processing Pipeline Run'
    def __init__(self,**kwargs):
        self.__dict__.update( kwargs )

    def __str__(self):
            return "".join(['%s=%s,'%(k,v) for (k,v) in self.__dict__.iteritems()])

class JOBRun():
    def __init__(self,**kwargs):
        self.__dict__.update( kwargs )

    def __str__(self):
            return "".join(['%s=%s,'%(k,v) for (k,v) in self.__dict__.iteritems()])

class Event():
    def __init__(self,**kwargs):
        self.status=spconst.EVENT_STATUS_NEW
        self.__dict__.update( kwargs )
    def __str__(self):
        return self.name

# init.
