#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synchro-data
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved”
# @svn_file       $Id: sddeletedataset.py 12605 2014-03-18 07:31:36Z jerome $
# @version        $Rev: 12611 $
# @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
# @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################
 
"""This module contains dataset delete functions."""

import sdapp
import sddatasetutils
import sdlog
import sddao
import sddb
import sddatasetdao
import sddeletequery

def remove_old_versions_datasets(dry_run=False):
    """Remove old versions of datasets (i.e. all datasets versions but the latest)."""
    for d in sddatasetutils.get_old_versions_datasets():
        if dry_run:
            print d.get_full_local_path()
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
