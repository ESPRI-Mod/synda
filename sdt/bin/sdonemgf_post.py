#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This filter improves Search-API query response time when searching for one specific model.

Notes
    - Not used for now.
    - 'sdonemgf' means 'SynDa ONE Model Go Faster'.
    - This module IS independant from the 'sdonemgf_pre' module.
    - This module works by calling lock func *after* search-api call.
      This make possible, for example, to first run
      'sdtc search cmip5.output1.NSF-DOE-NCAR.CESM1-CAM5.rcp26.mon.ocean.Omon.r1i1p1.v20130302.rhopoto_Omon_CESM1-CAM5_rcp26_r1i1p1_216001-216912.nc'
      which take sometime, 
      but then the next calls will be faster (only if next calls are using the same model, of course)
    - One drawback is 'unlock' func must be called (in sdtc) to switch to another model

Also see
    - 'sdadmcon' module
    - 'sdonemgf_pre' module
"""

import sdlock

def run(files):

    # seems to be 2.7 only
    #models=list({file.get('model') for file in files}) # note: 'set' is used here to remove duplicates
    # version below is 2.6 compatible
    models=list(set([file.get('model') for file in files])) # note: 'set' is used here to remove duplicates

    if len(models)==0:
        # model not specified

        pass
    elif len(models)==1:
        # one model specified

        model=models[0]
        sdlock.lock(model)

    else:
        # more than one models specified

        pass

    return files

# module init.

