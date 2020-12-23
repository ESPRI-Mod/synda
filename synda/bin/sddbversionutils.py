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
"""

from distutils.version import LooseVersion

def version_range( versions, version_begin, version_end ):
    """Returns a sorted list of all versions between version_begin and version_end, inclusive.
    The inputs and outputs are version strings."""
    vs = [ LooseVersion(v) for v in versions ]
    vbegin = LooseVersion(version_begin)
    vend  =  LooseVersion(version_end)
    vrange = [ v for v in vs if v>=vbegin and v<=vend ]
    vrange.sort()
    return [vs.vstring for vs in vrange]

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
    import sddbversion
    print sddbversion.upgrade_procs.keys()
    print version_range(sddbversion.upgrade_procs.keys(), '3.0','4.2')
