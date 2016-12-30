#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

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
import sdapp
import sdlog
import sdconfig
import sddbobj
import sddbversion
import sdtools

def connect():
    global conn

    # set timeout
    #
    # When a database is accessed by multiple connections, and one of the processes
    # modifies the database, the SQLite database is locked until that transaction is
    # committed. The timeout parameter specifies how long the connection should wait
    # for the lock to go away until raising an exception. The default for the timeout
    # parameter is 5.0 (five seconds).
    #
    # more info here => http://www.sqlite.org/faq.html#q5
    #
    if sdtools.is_daemon():

        # we set a high sqlite timeout value for the daemon,
        # so it doesn't exit on timeout error when we are running
        # huge query in Synda IHM (e.g. synda install CMIP5)
        #
        # by doing so, so we are able to use Synda IHM and sqlite3
        # to run manual query without stopping the daemon.
        #
        timeout=12000 # 200mn # TODO maybe use 86400 / 24h here

    else:

        # we do not need to set a high sqlite timeout value for Synda IHM,
        # as daemon do not perform huge queries, so Synda IHM do not have
        # to wait for long until the sqlite lock is release.

        timeout=120 # 2 mn

    # Note
    #  by default, sqlite is in autocommit mode,
    #  but the sqlite3 python module is *not* in autocommit mode by default
    #  we don't want autocommit mode, so we leave it at its default, which will result in a plain "BEGIN" statement
    #  (If you want autocommit mode, then set isolation_level to None)

    # open connection
    conn=sqlite3.connect(sdconfig.db_file,timeout)
    conn.row_factory=sqlite3.Row # this is for "by name" colums indexing

    # create DB object
    sddbobj.create_tables(conn)
    sddbobj.create_indexes(conn)

def disconnect():
    global conn

    if is_connected():
        conn.close()

    conn=None

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
    if os.path.exists(sdconfig.db_file):
        if not sdtools.is_group_writable(sdconfig.db_file):
            if sdtools.set_file_permission(sdconfig.db_file):
                sdlog.info("SDDATABA-003","File permissions have been modified ('%s')"%sdconfig.db_file)
            else:
                # we come here when user have not enough priviledge to set file permission

                sdlog.info("SDDATABA-004","Missing privilege to modify file permissions ('%s')"%sdconfig.db_file)

def is_connected():
    if (conn==None):
        return False
    else:
        return True

def unload_table_from_memory(tablename):
    _in_memory_conn.execute("drop table if exists main.'%s'"%tablename)

def close_in_memory_database():
    global _in_memory_conn

    _in_memory_conn.close()
    _in_memory_conn=None

def load_table_in_memory(tablename,indexname):
    global _in_memory_conn

    sdlog.info("SDDATABA-001","loading '%s' table"%tablename)

    # create a database in memory
    if _in_memory_conn is None:
        _in_memory_conn = sqlite3.connect(":memory:")

    # attach persistent DB
    _in_memory_conn.execute("ATTACH '%s' AS persistentdb"%get_db_name())

    # drop table if already exists in memory
    _in_memory_conn.execute("drop table if exists main.'%s'"%tablename)
    # copy table from persistent DB to memory
    _in_memory_conn.execute("create table main.'%s' as select * from persistentdb.[%s]"%(tablename,tablename))
    # create index
    _in_memory_conn.execute("create index if not exists main.'%s' on '%s' (file)"%(indexname,tablename))

    # commit
    _in_memory_conn.commit()

    # detach persistent DB
    _in_memory_conn.execute("detach persistentdb")  

    _in_memory_conn.row_factory = sqlite3.Row

    sdlog.info("SDDATABA-002","table loaded")

# module init

conn=None
_in_memory_conn=None

connect()
sddbversion.check_version(conn) # this call upgrade the database schema if database version does not match binary version
atexit.register(disconnect)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    c = conn.cursor()
    c.execute("select url from file")
    rs=c.fetchone()
    if rs!=None:
        print type(rs[0])
        print rs[0]
    c.close()
