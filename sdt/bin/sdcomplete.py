#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sdcomplete.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""Add local files attributes after search-API call.

Description
    - If file already exist locally, this module completes file with
      informations coming from local database.
    - If file doesn't exist locally, this module completes file with default
      values.

Notes
  - This module can be used to process different metadata types (File and Dataset).
  - Some attributes may exist both at file level (A) and at
    file['attached_parameters'] level (B). This is normal: A attributes are
    final values and B attributes are input values coming from end-user.
"""

import sdapp
import sddao
import sdfiledao
import sddatasetdao
import sdconst
import sdprint
import sdpostpipelineutils
from sdexception import SDException

def run(files):
    check_collision(files)
    files=complete(files)
    return files

def complete(files):
    for f in files:

        # the if/else block below is because this module can be used to process different metadata type (File and Dataset).
        if f["type"]==sdconst.SA_TYPE_FILE:
            transfer=sdfiledao.get_file(f['file_functional_id'])

            if transfer<>None:
                f['status']=transfer.status

                if not sdpostpipelineutils.exists_attached_parameter(f,'priority'): # this is to allow setting priority using selection parameter (i.e. default priority can be overrided using selection parameter). It is usefull here for example when user wants to change priority (YES, a search-API request is needed in this case!).
                    f['priority']=transfer.priority
            else:
                f['status']=sdconst.TRANSFER_STATUS_NEW

                if not sdpostpipelineutils.exists_attached_parameter(f,'priority'): # this is to allow setting priority using selection parameter (i.e. default priority can be overrided using selection parameter). This is usefull here to set special priority for new files.
                    f['priority']=sdconst.DEFAULT_PRIORITY

        elif f["type"]==sdconst.SA_TYPE_DATASET:
            dataset=sddatasetdao.get_dataset(dataset_functional_id=f['dataset_functional_id'])

            if dataset<>None:
                f['status']=dataset.status
            else:
                f['status']=sdconst.DATASET_STATUS_NEW
        else:
            raise SDException('SDCOMPLE-001','Incorrect type (%s)'%f["type"])

    return files

def check_collision(files):
    for f in files:
        if 'status' in f:
            raise SDException("SDCOMPLE-032","incorrect field")
        if 'priority' in f:
            raise SDException("SDCOMPLE-033","incorrect field")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-1','--print_only_one_item',action='store_true')
    parser.add_argument('-f','--format',choices=['raw','line','indent'],default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
