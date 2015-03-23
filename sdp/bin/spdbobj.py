#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: spdbobj.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12611 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This script contains database objects."""

def create_tables(conn):
    """
    Notes
        - 'ppprun' table
            - 'ppp' mean 'Post-Processing Pipeline'
            - in 'dataset_pattern' column, '*' character can be used instead of facet to match multiple dataset.
            - 'state' columns is updated at each step of the pipeline
            - when pipeline status is 'done', 'transition' is null
            - when pipeline status is 'waiting' or 'pause', 'transition' contain the next transition to run
            - when pipeline status is 'running', 'transition' contain transition currently running
        - 'jobrun' table
            - 'runlog' column contains detailed infos about the job execution
    """
    conn.execute("create table if not exists ppprun (ppprun_id INTEGER PRIMARY KEY, variable TEXT, dataset_pattern TEXT, project TEXT, model TEXT, state TEXT, transition TEXT, status TEXT, pipeline TEXT, error_msg TEXT, priority INT, crea_date TEXT, last_mod_date TEXT)")
    conn.execute("create table if not exists event (event_id INTEGER PRIMARY KEY, name TEXT, status TEXT, project TEXT, model TEXT, dataset_pattern TEXT, variable TEXT, filename_pattern TEXT, crea_date TEXT, priority INT)")
    conn.execute("create table if not exists jobrun (jobrun_id INTEGER PRIMARY KEY, ppprun_id INT, transition TEXT, start_date TEXT, end_date TEXT, duration INT, status TEXT, error_msg TEXT, runlog TEXT)")

    conn.commit()

def create_indexes(conn):
    conn.execute("create unique index if not exists idx_ppprun_1 on ppprun (dataset_pattern,variable,pipeline)")
    conn.execute("create        index if not exists idx_ppprun_2 on ppprun (status,transition)")
    conn.execute("create        index if not exists idx_ppprun_3 on ppprun (priority,last_mod_date)") # this is only needed when using worker '-P' option
    conn.execute("create        index if not exists idx_event_1 on event (name)")
    conn.execute("create        index if not exists idx_event_2 on event (status)")
    conn.execute("create        index if not exists idx_event_3 on event (crea_date)")
    conn.commit()
