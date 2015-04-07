#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This script deserialize timeaxis runlog.

Description
    When timeaxis job run, many debug informations are stored in 'runlog' column using a serialized format.
    This script deserialize 'runlog' column thus permitting easier access to the debug informations.
"""

import os
import sys
import sqlite3
import argparse
import json

def connect(dbfile):

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
    conn=sqlite3.connect(db_file,l__timeout)
    conn.row_factory=sqlite3.Row # this is for "by name" colums indexing

    return conn

def disconnect(conn):
    if is_connected(conn):
        conn.close()

def is_connected(conn):
    if (conn==None):
        return False
    else:
        return True

# module init

destination_database='/tmp/timeaxis_runlog.db'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source_database')
    args = parser.parse_args()

    # check
    if os.path.isfile(args.destination_database):
        print 'ERROR: destination database exists (%s)'%args.destination_database
        sys.exit(1)
    
    # open connection
    src_conn=connect(args.source_database)
    dest_conn=connect(destination_database)

    # Create dest. table
    #
    # Notes
    #   - following columns are NOT file specific: ppprun_id,jobrun_id,variable,error,error_msg
    #   - jobrun.status column and per-file status JSON attribute are not the same thing (JSON status attribute is a per-file error code set on the worker and jobrun.status is a per-job ENUM set on the server side)
    #   - jobrun.status column and per-job error JSON attribute are not exactly the same thing, but quite similar (error is a per-job error boolean flag set on the worker and jobrun.status is a a per-job ENUM set on the server side)
    #
    dest_conn.execute("create table if not exists time_axis_normalization (time_axis_normalization_id INTEGER PRIMARY KEY, ppprun_id INT, jobrun_id INT, dataset_pattern TEXT, start_date TEXT, end_date TEXT, full_path_variable TEXT, variable TEXT,filename TEXT,version TEXT,calendar TEXT,start TEXT,end TEXT,last TEXT,length INT,instant INT,bnds INT,error INT,error_msg TEXT,new_checksum TEXT,status TEXT)")

    # load n extract
    print 'Extracting time axis run log...'
    src_cursor=src_conn.cursor()
    src_cursor.execute("select jobrun_id, runlog from jobrun where transition = 'time_axis_normalization'?'")
    rs=src_cursor.fetchone()
    while rs is not None:

        runlog=json.loads(rs['runlog'])

        for filename,attr in runlog['files'].iteritems():

            dest_conn.execute(
                """insert into time_axis_normalization
                   (ppprun_id,jobrun_id,variable,start_date,end_date,dataset_pattern,full_path_variable,filename,version,calendar,start,end,last,length,instant,bnds,error,error_msg,checksum,status)
                   values
                   (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
               (runlog['ppprun_id'],rs['jobrun_id'],runlog['start_date'],runlog['end_date'],runlog['dataset_pattern'],runlog['full_path_variable'],runlog['variable'],filename,attr['version'],attr['calendar'],attr['start'],attr['end'],attr['last'],attr['length'],attr['instant'],attr['bnds'],runlog['error'],runlog['error_msg'],attr['new_checksum'],attr['status']))

        rs=src_cursor.fetchone()

    src_cursor.close()
    dest_conn.commit()

    disconnect(src_conn)
    disconnect(dest_conn)


    print 'Time axis run log is now available at %s'%destination_database
