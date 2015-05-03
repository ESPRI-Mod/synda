#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
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
import sdget
import sdconfig
from sdtools import print_stderr

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    files=json.load( sys.stdin )

    for f in files:

        assert 'url' in f
        assert 'data_node' in f

        url=f['url']
        dn=f['data_node']

        #local_path='/tmp/test.nc'
        local_path='%s/test.nc'%sdconfig.tmp_folder

        if os.path.isfile(local_path):
            os.remove(local_path)

        (status,local_checksum,killed,script_stdxxx)=sdget.download(url,local_path,checksum_type='md5',debug_level=0)

        if status!=0:
            print_stderr('Download failed: %s'%dn)
        else:
            print_stderr('File successfully downloaded: %s'%dn)

    sys.exit(0)
