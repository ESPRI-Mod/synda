#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains database I/O routines."""

import os
import argparse
import sqlite3
import atexit
from synda.sdt import sdlog
from synda.sdt import sddbobj
from synda.sdt import sddbversion
from synda.sdt import sdtools
from synda.source.config.file.db.models import Config as DbConfig
from synda.source.config.process.db.constants import get_timeout

db_file = DbConfig().get()


def connect():
    global conn

    timeout = get_timeout()

    # Note
    #  by default, sqlite is in autocommit mode,
    #  but the sqlite3 python module is *not* in autocommit mode by default
    #  we don't want autocommit mode, so we leave it at its default, which will result in a plain "BEGIN" statement
    #  (If you want autocommit mode, then set isolation_level to None)

    # open connection

    conn = sqlite3.connect(
        db_file,
        timeout,
    )

    # this is for "by name" colums indexing
    conn.row_factory = sqlite3.Row

    # create DB object
    sddbobj.create_tables(conn)
    sddbobj.create_indexes(conn)


def disconnect():
    global conn

    if is_connected():
        conn.close()

    conn = None

    # hack
    #
    # force sqlite db file to be group writable
    #
    # It should be done with umask when creating the db, but seems not working due to a bug.
    #
    # more info
    #   http://www.mail-archive.com/sqlite-users@mailinglists.sqlite.org/msg59080.html
    #   https://code.djangoproject.com/ticket/19292
    #
    if os.path.exists(db_file):
        if not sdtools.is_group_writable(db_file):
            if sdtools.set_file_permission(db_file):
                sdlog.info("SDDATABA-003", "File permissions have been modified ('%s')" % db_file)
            else:
                # we come here when user have not enough priviledge to set file permission

                sdlog.info("SDDATABA-004", "Missing privilege to modify file permissions ('%s')" % db_file)


def is_connected():
    if not conn:
        return False
    else:
        return True

# module init


conn = None
_in_memory_conn = None

connect()
# this call upgrade the database schema if database version does not match binary version
sddbversion.check_version(conn)
atexit.register(disconnect)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    c = conn.cursor()
    c.execute("select url from file")
    rs = c.fetchone()
    if rs:
        print(type(rs[0]))
        print(rs[0])
    c.close()
