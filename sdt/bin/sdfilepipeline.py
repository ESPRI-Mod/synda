#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script runs "file" pipeline's jobs.

Usage
 - cat file | sdfilepipeline -
 - cat file | sdfilepipeline
 - sdfilepipeline file
"""

import sys
import argparse
import json
import sdapp
import sdselectionfileutils
import sdreducecol
import sdreducerow
import sdtimefilter
import sdtransform
import sdprepare_dataset_attr
import sdprepare_file_attr
import sdlocalpath
import sdcheck_dataset_template
import sdremoveaggregation
import sdcomplete
import sdprint
import sdlog
import sdstatusfilter
import sdnormalizefattr
import sdprotocol
from sdexception import SDException

def run(**kw):
    files=kw.get('files')
    check_type(files)
    check_fields(files)
    files=sdreducerow.run(files)
    files=sdremoveaggregation.run(files)
    files=sdprotocol.run(files)
    files=sdtimefilter.run(files)
    files=sdtransform.run(files)
    files=sdprepare_dataset_attr.run(files)
    #files=sdcheck_dataset_template.run(files)

    # we do not remove the number of column here anymore
    #
    # Notes
    #     - not reducing the number of column here may slightly diminish
    #       performance (memory, cpu). But as we do need those informations (e.g.
    #       description, variable_long_name, facets..), we have no choice.
    #     - we need to keep those informations even if they are not essential,
    #       as we will need them soon to provide more descriptive informations to
    #       the user (e.g. description, variable_long_name..)
    #     - we need to keep all facets so the user can build custom local path
    #       (see local_path_custom_transform() func for more info)
    #     - we will now remove those column downstream (but only for 'dump' action)
    #
    #files=sdreducecol.run(files)

    files=sdnormalizefattr.run(files)

    files=sdprepare_file_attr.run(files)
    files=sdlocalpath.run(files)

    
    # EXT_FILE_POST
    #
    # load extensions here
    #
    # TODO


    files=sdcomplete.run(files)

    files=sdstatusfilter.run(files)

    return files

def check_type(files):
    for f in files:
        type=f['type']
        if type!='File':
            raise SDException('SDFIPIPE-001','Incorrect type (%s)'%type)

def check_fields(files):
    """This func is to prevent user to set 'fields' attribute (this attribute is set only by the program, in specific cases)."""

    for f in files:
        if 'fields' in f:
            raise SDException('SDFIPIPE-002',"'fields' parameter can't be used in 'file' pipeline (fields=%s)"%f['fields'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file',nargs='?',default='-')
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    args = parser.parse_args()

    path=None
    buffer=None
    if args.file == "-":
        files=json.load( sys.stdin )
    else:
        path=sdselectionfileutils.find_selection_file(args.file)
        with open(path, 'r') as fh:
            files=json.load( fh )

    files=run(files=files)

    sdprint.print_format(files,args.format,args.print_only_one_item)
