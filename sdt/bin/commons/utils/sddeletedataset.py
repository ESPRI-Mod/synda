#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved”
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains dataset delete functions."""
from sdt.bin.db import dao
from sdt.bin.db import session
from sdt.bin.db import dao_operations
from sdt.bin.commons.utils import sdlog


def remove_old_versions_datasets(dry_run=False):
    """Remove old versions of datasets (i.e. all datasets versions but the latest)."""
    for d in dao_operations.get_old_versions_datasets():
        if dry_run:
            print(d.get_full_local_path())
        else:
            with session.create():
                sdlog.info("SDDELETE-032", "remove dataset ({})".format(d.get_full_local_path()))
                dao.delete_dataset_transfers(d)
                dao.remove_datasets([d])


def purge_orphan_datasets():
    """Remove orphan datasets (datasets which doesn't have any entries in "transfer" table)."""
    with session.create():
        nbr = dao.purge_orphan_datasets()
    sdlog.info("SDDELETE-232", "{} orphan dataset(s) removed".format(nbr))
    return nbr
