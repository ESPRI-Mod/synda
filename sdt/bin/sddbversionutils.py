#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains database versioning utils routines.

Note
    Version pattern must be "x.x" with x an integer.
"""

def _str2int(version):
    assert isinstance(version,str)
    return int(float(version)*10)

def _int2str(version):
    assert isinstance(version,int)
    return str(float(version)/10)

def version_range(version_begin,version_end):
    """Return version range between version_begin and version_end."""

    vb=_str2int(version_begin)
    ve=_str2int(version_end)

    return [_int2str(i) for i in range(vb,ve)]

# --- version table I/O --- #

def get_db_version(conn):
    """
    Note
        Return None if 'version' table is empty
    """
    c = conn.cursor()
    c.execute("select version from version")
    rs=c.fetchone()
    version=rs[0] if rs!=None else None
    c.close()

    return version

def update_db_version(conn,version):
    c = conn.cursor()
    c.execute("update version set version=?",(version,))
    conn.commit()
    c.close()

# init.

if __name__ == '__main__':
    print version_range('3.0','4.2')
