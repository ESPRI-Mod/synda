#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script download files sequentially in foreground (without using the daemon)."""

import argparse
import os
import sys
import json
import sdapp
import sdconst
import sdconfig
import sdutils
import sdget
from sdtypes import File
from sdtools import print_stderr

def run(files,
        timeout=sdconst.DIRECT_DOWNLOAD_HTTP_TIMEOUT,
        force=False,
        http_client=sdconst.HTTP_CLIENT_WGET,
        local_path_prefix=sdconfig.sandbox_folder,
        verify_checksum=False,
        network_bandwidth_test=False,
        debug=True,
        verbosity=0,
        buffered=False,
        hpss=False):
    """
    Returns:
        0 if all transfers complete successfully
        1 if one or more transfer(s) didn't complete successfully
    """
    failed_count=0

    for file_ in files:

        # check

        assert 'url' in file_
        #assert 'data_node' in file_
        assert 'local_path' in file_


        if verify_checksum:
            if checksum_attrs_ok(file_):
                missing_remote_checksum_attrs=False
            else:
                missing_remote_checksum_attrs=True


        # cast

        f=File(**file_)


        # prepare attributes

        #local_path='/tmp/test.nc'
        #local_path='%s/test.nc'%sdconfig.tmp_folder
        local_path=f.get_full_local_path(prefix=local_path_prefix)


        # check

        if not network_bandwidth_test:

            if os.path.isfile(local_path):

                if force:
                    os.remove(local_path)
                else:
                    print_stderr('Warning: download cancelled as local file already exists (%s)'%local_path)

                    failed_count+=1

                    continue


        # special case

        if network_bandwidth_test:
            local_path='/dev/null'


        # transfer

        (status,killed,script_stderr)=sdget.download(f.url,local_path,debug,http_client,timeout,verbosity,buffered,hpss)


        # post-transfer

        if status!=0:
            failed_count+=1

            print_stderr('Download failed (%s)'%f.url)

            if buffered: # in non-buffered mode, stderr is already display (because child stderr is binded to parent stderr)

                # currently, we don't come here but we may need in the futur so we keep this block

                if script_stderr is not None:
                    print_stderr(script_stderr)
        else:

            if network_bandwidth_test:
                return

            if verify_checksum:
                if missing_remote_checksum_attrs:
                    failed_count+=1

                    print_stderr('Warning: missing remote checksum attributes prevented checksum verification (%s)'%local_path)
                else:

                    remote_checksum=f.checksum
                    local_checksum=sdutils.compute_checksum(local_path,f.checksum_type)

                    if local_checksum==remote_checksum:
                        print_stderr('File successfully downloaded, checksum OK (%s)'%local_path)
                    else:
                        failed_count+=1

                        print_stderr("Error: local checksum don't match remote checksum (%s)"%local_path)
            else:
                print_stderr('File successfully downloaded, no checksum verification (%s)'%local_path)

    if failed_count>0:
        return 1
    else:
        return 0

def checksum_attrs_ok(file_):
    if 'checksum_type' in file_ and 'checksum' in file_:
        return True
    else:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    files=json.load( sys.stdin )
    status=run(files)
    sys.exit(status)
