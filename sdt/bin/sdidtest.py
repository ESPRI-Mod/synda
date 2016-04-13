#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains routines to test identifier type.

Note
    sdidtest means 'SynDa IDentifier test'
"""

import argparse

def is_filename(arg):
    if not arg.endswith('.nc'):
        return False
    if arg.count('.')>1:
        return False
    if '/' in arg:
        return False

    return True

def is_file_functional_id(arg):
    if not arg.endswith('.nc'):
        return False
    if not arg.count('.')>1:
        return False
    if '/' in arg:
        return False

    return True

def is_dataset_functional_id(arg):
    result=True

    if arg.endswith('.nc'):
        result=False
    if arg.count('/')>0:
        result=False
    if arg.count('.')<3:
        result=False



    last_field=get_last_field(arg,'.')
    if not is_version_number(last_field):
        # last field is not a version number, so it's not a dataset_functional_id

        result=False



    return result

def is_dataset_local_path(arg):
    if arg.endswith('.nc'):
        return False
    if arg.count('.')>0:
        return False
    if arg.count('/')<1:
        return False

    return True

def is_file_local_path(arg):
    if not arg.endswith('.nc'):
        return False
    if arg.count('/')<1:
        return False

    return True

def is_url(arg):
    if arg.startswith('irods://'):
        return True
    if arg.startswith('http://'):
        return True
    if arg.startswith('https://'):
        return True
    if arg.startswith('gsiftp://'):
        return True

    return False

# o-------------------------------------o

def get_last_field (arg,delim):
    li=arg.split(delim)
    return li[-1]

def is_version_number (value):
    """
    Sample
        v20110901
        v1
    """
    if len(value)==2:
        if value[0]=='v':
            if value[1].isdigit():
                return True
            else:
                return False
        else:
            return False
    elif len(value)==9:
        if value[0]=='v':
            buf=value[1:9]
            if buf.isdigit():
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def whatis (arg):
    """
    Inference using tree.

    Experimental: may replace the duck typing in the future.
    """
    """
    if arg.count('/')>0:
        # looks like a path
        
        # only two matching params at this point: institute|CSU/GMU and institute|NOAA/ESRL+CU/CIRES

        if arg.endswith('.nc'):
            # looks like a file local_path

            return 'local_path'

        else:
            last_field=arg.TODO
            if is_version_number():
                return
            else:
                return
    else:
        if arg.count('.')>0:
            # looks like file_functional_id

            TODO what if url ending with .nc ?

        else:
            # no '.', no '/'

            # so not a local path, not an functional identifier, not an url

            if arg.count('_')>0:
                # lools like a filename
    """
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('facet')
    args = parser.parse_args()

    print args.facet
