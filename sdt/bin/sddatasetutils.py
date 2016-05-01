#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains local dataset utils."""

import sdapp
import sddatasetdao
import sddatasetquery
from sdexception import SDException

def get_old_versions_datasets():
    """Return old versions datasets list."""
    lst=[]

    for d in sddatasetdao.get_datasets():
        datasetVersions=sddatasetquery.get_dataset_versions(d,True) # retrieves all the versions of the dataset
        if d.latest==False: # this version is not the latest
            if datasetVersions.exists_version_with_latest_flag_set_to_true(): # latest exists
                if not datasetVersions.is_version_higher_than_latest(d): # version is not higher than latest
                    # assert
                    if datasetVersions.is_most_recent_version_number(d): # should never occurs because of the previous tests
                        raise SDException("SDSTAT-042","fatal error (version=%s,path_without_version=%s)"%(d.version,d.get_name_without_version()))

                    lst.append(d)

    return lst
