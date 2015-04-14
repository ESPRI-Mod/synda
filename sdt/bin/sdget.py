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
import sdconst
import sdlog

def download_with_wget(url):

    tmpfile='/tmp/sdt_test_file.nc'

    if os.path.isfile(tmpfile):
        os.remove(tmpfile)

    (sdget_status,stdout,stderr)=sdutils.get_status_output([sdconfig.data_download_script_http,'-d 3',url,tmpfile],shell=False)

    print_stderr(stdout) # TODO: do not mix stderr and stdout upside down

    #print "'sdget.sh' exit code: %i"%sdget_status

    """
    if sdget_status==0:
        print 'file location: %s'%tmpfile
    """

def download(url,full_local_path,checksum_type):
    killed=False

    transfer_protocol=get_transfer_protocol(url)


    if transfer_protocol==sdconst.TRANSFER_PROTOCOL_HTTP
            and sdconfig.http_client==sdconst.HTTP_CLIENT_URLLIB:

        import sdnetutils
        (status,local_checksum)=sdnetutils.download_file(url,full_local_path,checksum_type)
    else:
        (status,local_checksum,killed)=run_download_script(url,full_local_path,checksum_type,transfer_protocol)


    return (status,local_checksum,killed)

def run_download_script(url,full_local_path,checksum_type,transfer_protocol):

    if transfer_protocol==sdconst.TRANSFER_PROTOCOL_HTTP:
        script=sdconfig.data_download_script_http        
    elif transfer_protocol==sdconst.TRANSFER_PROTOCOL_GRIDFTP:
        script=sdconfig.data_download_script_gridftp
    else:
        assert False


    cmd_line="%s -c %s %s %s" % (script,checksum_type,url,full_local_path)
    (status,stdout,stderr)=sdutils.get_status_output(cmd_line,shell=True) # start a new process (fork is blocking here, so thread will wait until wget is done)


    if status==0:
        local_checksum=stdout.rstrip(os.linesep) # if success (status==0), stdout contains only checksum
    else:
        local_checksum=None

    killed=is_killed(transfer_protocol,status)


    if not killed:
        sdlog.debug("SYNDAGET-002","%s"%stderr) # if error occurs in 'sdget.sh', stderr contains error message

    sdlog.debug("SYNDAGET-001","%s"%stdout) # unexpected errors may be hidden in stdout


    return (status,local_checksum,killed)

def get_transfer_protocol(url):
    if url.startswith('http://'):
        return sdconst.TRANSFER_PROTOCOL_HTTP
    elif url.startswith('gsiftp://'):
        return sdconst.TRANSFER_PROTOCOL_GRIDFTP
    else:
        assert False

def is_killed(transfer_protocol,status):
    """This func return True if child process has been killed."""

    if transfer_protocol=sdconst.TRANSFER_PROTOCOL_HTTP:
        if sdconfig.http_client=sdconst.HTTP_CLIENT_WGET:
            if status in (7,29):
                return True
            else:
                return False
        elif sdconfig.http_client=sdconst.HTTP_CLIENT_URLLIB:
            return False
        else:
            assert False
    elif transfer_protocol=sdconst.TRANSFER_PROTOCOL_GRIDFTP:
        return False # TODO
    else:
        assert False

# init.
