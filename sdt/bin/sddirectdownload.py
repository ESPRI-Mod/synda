#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script run download test on each url and display download status.

Note
    Return code is always 0
"""

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

def run(files,timeout=sdconst.DIRECT_DOWNLOAD_HTTP_TIMEOUT,force=False,http_client=sdconst.HTTP_CLIENT_URLLIB,local_path_prefix=sdconfig.sandbox_folder,verify_checksum=False,network_bandwidth_test=False,debug=True,verbose=True):

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
                    print_stderr('WARNING: download cancelled as local file already exists (%s)'%local_path)
                    continue


        # special case

        if network_bandwidth_test:
            local_path='/dev/null'


        # transfer

        (status,killed,script_stderr)=sdget.download(f.url,local_path,debug,http_client,timeout)


        # post-transfer

        if status!=0:
            print_stderr('Download failed (%s)'%f.url)

            if verbose:
                if http_client==sdconst.HTTP_CLIENT_WGET:
                    print_stderr(script_stderr)
        else:

            if network_bandwidth_test:
                return

            print_stderr('File successfully downloaded (%s)'%local_path)

            if verify_checksum:
                if missing_remote_checksum_attrs:
                    print_stderr('Warning: missing remote checksum attributes prevented checksum verification (%s)'%local_path)
                else:

                    remote_checksum=f.checksum
                    local_checksum=sdutils.compute_checksum(local_path,f.checksum_type)

                    if local_checksum==remote_checksum:
                        print_stderr('Checksum OK (%s)'%local_path)
                    else:
                        print_stderr('Checksum ERROR (%s)'%local_path)

def checksum_attrs_ok(file_):
    if 'checksum_type' in file_ and 'checksum' in file_:
        return True
    else:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    files=json.load( sys.stdin )

    run(files)

    sys.exit(0)
