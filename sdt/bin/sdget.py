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

import os
import sdapp
import sdconfig
from sdtools import print_stderr
import sdutils

def download_with_wget(url):

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

def download(url,full_local_path,checksum_type):

    download_cmd_line="%s -c %s %s %s" % (sdconfig.data_download_script,checksum_type,url,full_local_path)

    # start a new process (fork is blocking here, so thread will wait until wget is done)
    (status,stdout,stderr)=sdutils.get_status_output(download_cmd_line,shell=True)

    if status==0:
        local_checksum=stdout.rstrip(os.linesep) # if success (status==0), stdout contains only checksum
    else:
        local_checksum=None

    # debug (unexpected errors may be hidden in stdout)
    #print stdout

    return (status,local_checksum,stderr) # if error occurs in 'sdget.sh', stderr contains error message

# init.
