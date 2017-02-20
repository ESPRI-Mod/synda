#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        syndat
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains database versioning routines."""

import sdapp
import sdlog
import sddbnormalize
import sddbversionutils
from sdexception import SDException

def check_version(conn):
    """Upgrade the database schema if database version does not match binary version.

    Note
        This func must be light as executed each time 'synda' starts
        (except for special case like 'synda -V').
    """

    current_db_version=sddbversionutils.get_db_version(conn)

    if current_db_version==None:
        # this case is for when starting from scratch
        # (first startup or when db file as been removed)

        c = conn.cursor()
        c.execute("insert into version (version) values (?)",(sdapp.version,))
        conn.commit()
        c.close()
    else:
        if current_db_version < "2.9":
            raise SDException("SDDBVERS-316","Database version too old: cannot upgrade database")

        if sdapp.version==current_db_version:
            pass # db version matches binary version, nothing to do
        elif sdapp.version < current_db_version:
            raise SDException("SDDBVERS-317","Binary cannot be used with this database (binary version too old)")
        elif sdapp.version > current_db_version:
            upgrade_db(conn,current_db_version,sdapp.version)

def upgrade_db(conn,current_db_version,new_db_version):
    li=sddbversionutils.version_range(current_db_version,new_db_version)

    # remove the first value (i.e. no upgrade needed there as db is already at this version)
    li=li[1:]

    for v in li:
        if v not in upgrade_procs:
            raise SDException("SDDBVERS-318","Incorrect database version: cannot upgrade database (version=%s)."%(v,))
        else:
            upgrade_procs[v](conn)
            sdlog.info("SDDBVERS-319","Database updated to version %s"%(v,))

# -- upgrade procs -- #

def upgrade_39(conn):

    # put schema upgrade code here if any

    sddbversionutils.update_db_version(conn,'3.9')

def upgrade_38(conn):

    # put schema upgrade code here if any

    sddbversionutils.update_db_version(conn,'3.8')

def upgrade_37(conn):

    # put schema upgrade code here if any

    sddbversionutils.update_db_version(conn,'3.7')

def upgrade_36(conn):

    # put schema upgrade code here if any

    sddbversionutils.update_db_version(conn,'3.6')

def upgrade_35(conn):

    sddbnormalize.normalize_checksum_type(conn)

    conn.execute("alter table history add column selection_file_checksum TEXT")
    conn.execute("alter table history add column selection_file TEXT")

    conn.execute("update file set duration=cast(((julianday(end_date) - julianday(start_date)) * 86400.0) as integer) where status = 'done'")
    conn.execute("update file set duration=1 where duration=0 and status='done'")
    conn.execute("update file set rate=size/duration where status='done'")

    conn.commit()

    sddbversionutils.update_db_version(conn,'3.5')

def upgrade_34(conn):

    # put schema upgrade code here if any

    sddbversionutils.update_db_version(conn,'3.4')

def upgrade_33(conn):

    # put schema upgrade code here if any

    sddbversionutils.update_db_version(conn,'3.3')

def upgrade_32(conn):

    # put schema upgrade code here if any

    sddbversionutils.update_db_version(conn,'3.2')

def upgrade_31(conn):

    # put schema upgrade code here if any

    sddbversionutils.update_db_version(conn,'3.1')

def upgrade_30(conn):

    # put schema upgrade code here if any

    sddbversionutils.update_db_version(conn,'3.0')

# init.

upgrade_procs={
    '3.9': upgrade_39,
    '3.8': upgrade_38,
    '3.7': upgrade_37,
    '3.6': upgrade_36,
    '3.5': upgrade_35,
    '3.4': upgrade_34,
    '3.3': upgrade_33,
    '3.2': upgrade_32,
    '3.1': upgrade_31,
    '3.0': upgrade_30
}
