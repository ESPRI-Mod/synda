#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This module contains data file download routines.

Note
    This module contains two implementations to download data file
        - Pure python implementation (https and urllib2)
        - 'wget' based implementation
"""

import sdapp
import sdconfig
from sdtools import print_stderr

def download_with_wget(url):
    import os, sdutils

    tmpfile='/tmp/sdt_test_file.nc'

    if os.path.isfile(tmpfile):
        os.remove(tmpfile)

    (sdget_status,stdout,stderr)=sdutils.get_status_output([sdconfig.data_download_script,'-d 3',url,tmpfile],shell=False)

    print_stderr(stdout) # TODO: do not mix stderr and stdout upside down

    #print "'sdget.sh' exit code: %i"%sdget_status

    """
    if sdget_status==0:
        print 'file location: %s'%tmpfile
    """

# init.
