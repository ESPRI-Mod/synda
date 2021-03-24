#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
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

from synda.sdt import sdfiledao
from synda.sdt import sddatasetdao
from synda.sdt import sdconst
from synda.sdt import sdprint
from synda.sdt import sdpostpipelineutils
from synda.sdt.sdexception import SDException

from synda.source.config.process.download.constants import TRANSFER
from synda.source.config.process.download.dataset.constants import STRUCTURE as DATASET_STRUCTURE
from synda.source.config.api.esgf_search.constants import STRUCTURE as SEARCH_API_STRUCTURE


def run(files):
    check_collision(files)
    files=complete(files)
    return files

def complete(files):
    for f in files:

        # the if/else block below is because this module can be used to process different metadata type (File and Dataset).
        if f["type"]==SEARCH_API_STRUCTURE['type']['file']:
            transfer=sdfiledao.get_file(f['file_functional_id'])

            if transfer is not None:
                f['status']=transfer.status

                if sdpostpipelineutils.exists_attached_parameter(f,'priority'): # this is to allow setting priority using selection parameter (i.e. default priority can be overrided using selection parameter). It is usefull here for example when user wants to change priority (YES, a search-API request is needed in this case!).
                    f['priority']=sdpostpipelineutils.get_attached_parameter(f,'priority')
                else:
                    f['priority']=transfer.priority
            else:
                f['status'] = TRANSFER["status"]['new']

                if sdpostpipelineutils.exists_attached_parameter(f,'priority'): # this is to allow setting priority using selection parameter (i.e. default priority can be overrided using selection parameter). This is usefull here to set special priority for new files.
                    f['priority']=sdpostpipelineutils.get_attached_parameter(f,'priority')
                else:
                    f['priority']=sdconst.DEFAULT_PRIORITY

        elif f["type"]==SEARCH_API_STRUCTURE['type']['dataset']:
            dataset=sddatasetdao.get_dataset(dataset_functional_id=f['dataset_functional_id'])

            if dataset is not None:
                f['status']=dataset.status
            else:
                f['status']=DATASET_STRUCTURE["status"]["new"]
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
    parser.add_argument('-F','--format',choices=sdprint.formats,default='raw')
    args = parser.parse_args()

    files=json.load( sys.stdin )
    files=run(files)
    sdprint.print_format(files,args.format,args.print_only_one_item)
