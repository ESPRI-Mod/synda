#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
import sdconfig
import sdtools

from synda.source.config.file.db.models import Config as Db
from synda.source.config.file.daemon.models import Config as DaemonFile

from synda.source.config.path.tree.certificate.x509.models import Config as SecurityPath
from synda.source.config.file.certificate.x509.models import Config as SecurityFile
from synda.source.config.path.tree.models import Config as TreePath

from synda.source.config.file.user.credentials.models import Config as Credentials

tree_path = TreePath()
DAEMON_FULLFILENAME = DaemonFile().default


def run(uid, gid):
    chown_folder(uid, gid)
    chown_file(uid, gid)


def chown_folder(uid,gid):
    # tmp folder
    li = [tree_path.get("tmp")]
    chown_files(li,uid,gid)

    # security folder
    assert False # this code needs review (with default security_dir_mode, there are two more subfolder levels that need to be processed as well (<uuid> and .esg))
    li=[SecurityPath().get_security()]
    chown_files(li,uid,gid)

    # CA certificate folder
    li=[SecurityPath().get_certificates()]
    chown_files(li,uid,gid)

    # db folder
    li=[tree_path.get("db")]
    chown_files(li,uid,gid)

    # log folder
    li=[tree_path.get("log")]
    chown_files(li,uid,gid)


def chown_file(uid, gid):

    # pid files
    li = [DAEMON_FULLFILENAME]
    chown_files(li, uid, gid)

    # sdt credentials file
    credential_file = Credentials().get()
    li = [credential_file]
    chown_files(li, uid, gid)

    # proxy cert file
    li=[SecurityFile().get_credentials()]
    chown_files(li,uid,gid)

    # CA certificates
    li=sdtools.ls(SecurityPath().get_certificates())
    chown_files(li,uid,gid)
    
    # db file
    db_file = Db().get()
    li = [db_file]
    chown_files(li, uid, gid)

    # log
    li=sdtools.ls(tree_path.get("log"))
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
