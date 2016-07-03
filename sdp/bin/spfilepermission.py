#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains file permission related functions."""

import os
import argparse
import glob
import spapp
import spconfig

def run(uid,gid):
    chown_folder(uid,gid)
    chown_file(uid,gid)

def chown_folder(uid,gid):

    # tmp folder
    li=[spconfig.tmp_folder]
    chown_files(li,uid,gid)

    # db folder
    li=[spconfig.db_folder]
    chown_files(li,uid,gid)

    # log folder
    li=[spconfig.log_folder]
    chown_files(li,uid,gid)

def chown_file(uid,gid):

    # db file
    li=[spconfig.db_file]
    chown_files(li,uid,gid)

    # log
    li=ls(spconfig.log_folder)
    chown_files(li,uid,gid)

def ls(path,filter_='*'):
    """Return full path files list inside the given folder.

    Note
        - non-recursive
        - folder are not listed
    """
    files=[]

    for file_ in glob.glob( os.path.join(path, filter_) ):
        if not os.path.isdir(file_): # exclude sub-dirs
            files.append(file_)

    return files

def chown_files(files,uid,gid):
    """Perform chown on all files.
    
    Note
        'files' can contain regular file or directory.
    """
    for file_ in files:
        if os.path.exists(file_): # this is to prevent error like "OSError: [Errno 2] No such file or directory: '/var/tmp/synda/sdt/.esg/certificates'"
            os.chown(file_,uid,gid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
