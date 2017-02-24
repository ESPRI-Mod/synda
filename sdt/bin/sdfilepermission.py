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
import sdapp
import sdconfig
import sdtools

def run(uid,gid):
    chown_folder(uid,gid)
    chown_file(uid,gid)

def chown_folder(uid,gid):

    # tmp folder
    li=[sdconfig.tmp_folder]
    chown_files(li,uid,gid)

    # security folder
    assert False # this code needs review (with default security_dir_mode, there are two more subfolder levels that need to be processed as well (<uuid> and .esg))
    li=[sdconfig.get_security_dir()]
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

    # pid files
    li=[sdconfig.daemon_pid_file,sdconfig.ihm_pid_file]
    chown_files(li,uid,gid)

    # sdt credentials file
    li=[sdconfig.credential_file]
    chown_files(li,uid,gid)

    # proxy cert file
    li=[sdconfig.esgf_x509_proxy]
    chown_files(li,uid,gid)

    # CA certificates
    li=sdtools.ls(sdconfig.esgf_x509_cert_dir)
    chown_files(li,uid,gid)
    
    # db file
    li=[sdconfig.db_file]
    chown_files(li,uid,gid)

    # log
    li=sdtools.ls(sdconfig.log_folder)
    chown_files(li,uid,gid)

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
