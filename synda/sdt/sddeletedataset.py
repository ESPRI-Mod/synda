#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
 
"""This module contains dataset delete functions."""

from synda.sdt import sdapp
from synda.sdt import sddatasetutils
from synda.sdt import sdlog
from synda.sdt import sddao
from synda.sdt import sddb
from synda.sdt import sddatasetdao
from synda.sdt import sddeletequery

def remove_old_versions_datasets(dry_run=False):
    """Remove old versions of datasets (i.e. all datasets versions but the latest)."""
    for d in sddatasetutils.get_old_versions_datasets():
        if dry_run:
            print(d.get_full_local_path())
        else:
            sdlog.info("SDDELETE-032","remove dataset (%s)"%d.get_full_local_path())

            sddeletequery.delete_dataset_transfers(d,conn=sddb.conn)
            sddatasetdao.remove_dataset(d,commit=False,conn=sddb.conn)

    if not dry_run:
        sddb.conn.commit()

def purge_orphan_datasets():
    """Remove orphan datasets (datasets which doesn't have any entries in "transfer" table)."""
    nbr=sddeletequery.purge_orphan_datasets()
    sdlog.info("SDDELETE-232","%i orphan dataset(s) removed"%nbr)
    return nbr
