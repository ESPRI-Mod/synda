#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
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
