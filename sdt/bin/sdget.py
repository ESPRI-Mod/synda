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
    This module provides 3 ways to download data file
        - urllib2 (pure python)
        - wget (external script)
        - gridftp (external script)
"""

import os
import sdapp
import sdconfig
from sdtools import print_stderr
import sdutils
import sdconst
import sdlog
import sdnetutils

def download(url,full_local_path,checksum_type='md5',debug_level=0):
    killed=False
    script_stdxxx=None

    transfer_protocol=sdutils.get_transfer_protocol(url)


    if (transfer_protocol==sdconst.TRANSFER_PROTOCOL_HTTP
        and sdconfig.http_client==sdconst.HTTP_CLIENT_URLLIB):

        (status,local_checksum)=sdnetutils.download_file(url,full_local_path,checksum_type)
    else:
        (status,local_checksum,killed,script_stdxxx)=run_download_script(url,full_local_path,checksum_type,transfer_protocol,debug_level)


    return (status,local_checksum,killed,script_stdxxx)

def run_download_script(url,full_local_path,checksum_type,transfer_protocol,debug_level):

    if transfer_protocol==sdconst.TRANSFER_PROTOCOL_HTTP:
        script=sdconfig.data_download_script_http        
    elif transfer_protocol==sdconst.TRANSFER_PROTOCOL_GRIDFTP:
        script=sdconfig.data_download_script_gridftp
    else:
        assert False


    (status,stdout,stderr)=sdutils.get_status_output([script,'-c',checksum_type,'-d',debug_level,url,full_local_path],shell=False) # start a new process (fork is blocking here, so thread will wait until child is done)


    # debug
    #sdlog.debug("SYNDAGET-002","%s"%stderr) # unexpected errors may be hidden in stderr
    #sdlog.debug("SYNDAGET-001","%s"%stdout) # unexpected errors may be hidden in stdout


    if status==0:
        local_checksum=stdout.rstrip(os.linesep) # if success (status==0), stdout contains only checksum
    else:
        local_checksum=None


    killed=is_killed(transfer_protocol,status)


    script_stdxxx=stderr # memo: in the child shell script, stdout is redirected to stderr so to leave stdout for the checksum (so stderr contains both stdout and stderr)


    return (status,local_checksum,killed,script_stdxxx)

def is_killed(transfer_protocol,status):
    """This func return True if child process has been killed."""

    if transfer_protocol==sdconst.TRANSFER_PROTOCOL_HTTP:
        if sdconfig.http_client==sdconst.HTTP_CLIENT_WGET:
            if status in (7,29):
                return True
            else:
                return False
        elif sdconfig.http_client==sdconst.HTTP_CLIENT_URLLIB:
            return False
        else:
            assert False
    elif transfer_protocol==sdconst.TRANSFER_PROTOCOL_GRIDFTP:
        return False # TODO
    else:
        assert False

# init.
