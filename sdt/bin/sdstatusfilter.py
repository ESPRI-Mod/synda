#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script keeps files with the given status.

Note
    This module is intended to be use in post-call pipeline based on end-user
    choice (to remove status in other places (e.g. to enforce that some status
    are removed no matter what the end-user choice is), use sdsimplefilter
    module).
"""

import sys
import argparse
import json
import sdapp
import sdpostpipelineutils
import sdprint

def run(files):
    new_files=[]

    for f in files:

        # retrieve status attributes
        status=f['status']                                                   # scalar
        status_filter=sdpostpipelineutils.get_attached_parameter(f,'status') # list

        if status_filter is None:
            new_files.append(f)
        else:
            assert isinstance(status_filter,list)
            if status in status_filter:
                new_files.append(f)
            else:
                pass

    return new_files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
