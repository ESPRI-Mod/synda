#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains replica related routines.""" 

import argparse
import random

def replica_next(current_url,replicas): # TODO: rename me
    """Select next replica."""

    new_replica=None

    replicas=sort(replicas)

    # find current pos
    current=None
    for i,(url,data_node) in enumerate(replicas):
        if current_url==url:
            current=i

    if current is not None:
        if current+1==len(replicas): # is last item in list ?
            next_=0 # rotation
        else:
            next_=current+1

        new_replica=replicas[next_]
    else:
        # current replica doesn't exist

        if len(replicas)>0:

            # use a random replica from the list
            new_replica=random.choice(replicas)

        else:
            new_replica=None

    # is same replica, return None
    if new_replica[0]==current_url:
        return None

    return new_replica

def sort(replicas):
    #print replicas
    replicas=sorted(replicas, key=lambda replica: replica[0]) # use url as sort key
    #print replicas
    return replicas

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    # TESTS

    url_1='http://dn.jp/a/f.nc'
    url_2='http://dn.de/t/f.nc'
    url_3='http://dn.gouv/z/f.nc'

    replicas=[]
    replicas.append((url_1,'dn.jp'))
    replicas.append((url_2,'dn.de'))
    replicas.append((url_3,'dn.gouv'))

    current_url=url_2

    replica=replica_next(current_url,replicas)

    print replica
