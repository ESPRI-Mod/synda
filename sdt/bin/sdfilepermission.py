#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains file permission related functions."""

import os
import argparse
import glob
import sdapp
import sdconfig

def run(uid,gid):
    chown_folder(uid,gid)
    chown_file(uid,gid)

def chown_folder(uid,gid):

    # tmp folder
    #
    # no need as this folder is 777 anyway
    #
    """
    li=[sdconfig.tmp_folder]
    chown_files(li,uid,gid)
    """

    # security folder
    li=[sdconfig.security_dir]
    chown_files(li,uid,gid)

    # CA certificate folder
    li=[sdconfig.esgf_x509_cert_dir]
    chown_files(li,uid,gid)

    # db folder
    li=[sdconfig.db_folder]
    chown_files(li,uid,gid)

    # log folder
    li=[sdconfig.log_folder]
    chown_files(li,uid,gid)

def chown_file(uid,gid):

    # proxy cert file
    li=[sdconfig.credential_file]
    chown_files(li,uid,gid)

    # proxy cert file
    li=[sdconfig.esgf_x509_proxy]
    chown_files(li,uid,gid)

    # CA certificates
    li=ls(sdconfig.esgf_x509_cert_dir)
    chown_files(li,uid,gid)
    
    # db file
    li=[sdconfig.db_file]
    chown_files(li,uid,gid)

    # log
    li=ls(sdconfig.log_folder)
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
