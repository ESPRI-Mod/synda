#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains data file download routines.

Notes
    - This module provides 3 ways to download data file
        - urllib2 (pure python)
        - wget (external script)
        - gridftp (external script)
    - This module is mainly used as module, but can also be used as script for basic
      url download test.
"""

import argparse
import os
import sys
import json
import sdapp
import sdconfig
import sdutils
import sdconst
import sdget_urllib
from sdtools import print_stderr

def download(url,full_local_path,debug=False,http_client=sdconfig.http_client,timeout=sdconst.ASYNC_DOWNLOAD_HTTP_TIMEOUT,verbosity=0,buffered=True,hpss=False):
    killed=False
    script_stderr=None

    transfer_protocol=sdutils.get_transfer_protocol(url)


    if transfer_protocol==sdconst.TRANSFER_PROTOCOL_HTTP:

        if http_client==sdconst.HTTP_CLIENT_URLLIB:
            status=sdget_urllib.download_file(url,full_local_path,timeout)
        elif http_client==sdconst.HTTP_CLIENT_WGET:

            li=prepare_args(url,full_local_path,sdconfig.data_download_script_http,debug,timeout,verbosity,hpss)

            (status,script_stderr)=run_download_script(li,buffered)

            killed=is_killed(transfer_protocol,status)

        else:
            assert False

    elif transfer_protocol==sdconst.TRANSFER_PROTOCOL_GRIDFTP:

        gridftp_opt=sdconfig.config.get('download','gridftp_opt')
        if len(gridftp_opt)>0:
            os.environ["GRIDFTP_OPT"]=gridftp_opt

        li=prepare_args(url,full_local_path,sdconfig.data_download_script_gridftp,debug,timeout,verbosity,hpss)

        (status,script_stderr)=run_download_script(li,buffered)

        killed=is_killed(transfer_protocol,status)

    elif transfer_protocol==sdconst.TRANSFER_PROTOCOL_GLOBUSTRANSFER:

        pass

    else:

        assert False

    return (status,killed,script_stderr)

def run_download_script(li,buffered):
    if buffered:
        return run_download_script_BUFSTDXXX(li)
    else:
        return run_download_script_RTSTDXXX(li)

def run_download_script_RTSTDXXX(li):

    # start a new process (fork is blocking here, so thread will wait until child is done)
    status=sdutils.get_status(li,shell=False)

    return (status,None)

def run_download_script_BUFSTDXXX(li):

    # start a new process (fork is blocking here, so thread will wait until child is done)
    #
    # note
    #  in the child shell script, stderr for error message
    #
    (status,stdout,stderr)=sdutils.get_status_output(li,shell=False)


    # download scripts may
    #   - return error message on stderr, one line terminated by EOL
    #   - return error message on stderr, multiple lines, each terminated by EOL

    # first, we chomp
    #
    # note
    #     only the last eol is chomped here.
    #
    stderr=stderr.rstrip('\r\n')

    # then we replace all eol from string but the last (which has already been chomped)
    #
    stderr=stderr.replace('\n', '<eol-n>').replace('\r', '<eol-r>')


    # encoding
    #
    # Depending on which encoding is set in the system, scripts can return
    # utf-8, latin1, or something else.
    #
    # As for now, Synda encoding is latin1 (this is enforced by setting
    # 'LANG=C' in external script), we remove any non-latin1 character if any.
    #
    # TODO
    #     In the futur, Synda will move to unicode instead of latin1.
    #     Thus, external scripts output encoding will have to be converted to
    #     unicode before being processed by synda
    #
    #     All synda input should be checked to only accept unicode
    #     (except for specific case where input encoding must be specific, in
    #     which case we make the required explicit conversion to obtain unicode)
    #
    #     samples
    #     stderr=unicode(stderr, encoding='utf-8')
    #     stderr=unicode(stderr, encoding='latin1')
    #
    #
    stderr=unicode(stderr,errors='ignore').encode('latin1')
    

    # debug (unexpected errors may be hidden in stdxxx)
    """
    with open(sdconfig.stacktrace_log_file,'a') as fh:
        fh.write("BEGIN '%s' script output\n"%os.path.basename(script))
        fh.write("status: %s\n"%status)
        fh.write("stdout:\n")
        fh.write(stdout)
        fh.write("stderr:\n")
        fh.write(stderr)
        fh.write("END '%s' script output\n"%os.path.basename(script))
    """

    return (status,stderr)

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

def build_verbosity_option(verbosity):
    """
    sample
        0 => None
        2 => '-vv'
        4 => '-vvvv'
    """

    if verbosity > 0:
        buf='v'*verbosity
        buf='-%s'%buf
        return buf
    else:
        return None

def prepare_args(url,full_local_path,script,debug,timeout,verbosity,hpss):

    li=[script,'-l',sdconfig.log_folder,'-T',sdconfig.tmp_folder,'-t',str(timeout),'-c',sdconfig.get_security_dir(),url,full_local_path]

    if debug:
        li.insert(1,'-d')

    verbosity_option=build_verbosity_option(verbosity)
    if verbosity_option is not None:
        li.insert(1,verbosity_option)

    if hpss:
        li.insert(1,'-p')
        li.insert(2,'0')

    return li

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-q','--quiet',action='store_true')
    args = parser.parse_args()

    files=json.load( sys.stdin )

    for f in files:

        assert 'url' in f

        url=f['url']
        local_path='/tmp/test.nc'

        if os.path.isfile(local_path):
            os.remove(local_path)

        (status,killed,script_stderr)=download(url,local_path,debug=True)

        if status!=0:
            if not args.quiet:
                print_stderr('Download failed: %s'%url)

            sys.exit(1)

    if not args.quiet:
        print_stderr('File(s) successfully downloaded')

    sys.exit(0)
