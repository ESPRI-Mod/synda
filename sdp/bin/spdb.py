#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda-pp
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdp/doc/LICENSE)
##################################

"""This script contains database I/O routines."""

import os
import sqlite3
import spapp
import spconfig
import spdbobj
import splog
import sptools

def connect():

    # When a database is accessed by multiple connections, and one of the processes
    # modifies the database, the SQLite database is locked until that transaction is
    # committed. The timeout parameter specifies how long the connection should wait
    # for the lock to go away until raising an exception. The default for the timeout
    # parameter is 5.0 (five seconds).
    #
    # more info here => http://www.sqlite.org/faq.html#q5
    #
    # we increase the timeout so we are able to use sqlite3 to run manual
    # query without stopping the daemon
    #
    l__timeout=120 # 2 mn

    # Note
    #  by default, sqlite is in autocommit mode,
    #  but the sqlite3 python module is *not* in autocommit mode by default
    #  we don't want autocommit mode, so we leave it at its default, which will result in a plain "BEGIN" statement
    #  (If you want autocommit mode, then set isolation_level to None)

    # open connection
    conn=sqlite3.connect(spconfig.db_file,l__timeout)
    conn.row_factory=sqlite3.Row # this is for "by name" colums indexing

    return conn

def disconnect(conn):
    if is_connected(conn):
        conn.close()

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
    if os.path.exists(spconfig.db_file):
        if not sptools.is_group_writable(spconfig.db_file):
            if sptools.set_file_permission(spconfig.db_file):
                splog.info("SPDATABA-003","File permissions have been modified ('%s')"%spconfig.db_file)
            else:
                # we come here when user have not enough priviledge to set file permission

                splog.info("SPDATABA-004","Missing privilege to modify file permissions ('%s')"%spconfig.db_file)

def is_connected(conn):
    if (conn==None):
        return False
    else:
        return True

# module init

conn=connect()
spdbobj.create_tables(conn)
spdbobj.create_indexes(conn)
disconnect(conn)
