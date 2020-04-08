#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                            All Rights Reserved
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains delete functions."""

import os
from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils import sdlog
from sdt.bin.commons.utils import sdexception
from sdt.bin.commons.utils import sddeletedataset
from sdt.bin.db import session
from sdt.bin.db import dao


def delete_transfers(limit=None, remove_all=True):
    """Perform the deletion of DATA and METADATA.

    Returns
        how many files with TRANSFER_STATUS_DELETE status remain

    Notes
        - Can be called from the daemon code (deferred mode), or from
          interactive code (immediate mode).
        - 'limit' is used to delete only a subset of all files marked for
          deletion each time this func is called. If 'limit' is None,
          all files marked for deletion are removed.
    """
    with session.create():
        transfer_list = dao.get_files(status=sdconst.TRANSFER_STATUS_DELETE, limit=limit)

        try:
            for tr in transfer_list:
                if remove_all:
                    immediate_delete(tr)
                else:
                    immediate_md_delete(tr)

        except Exception as e:
            sdlog.error("SDDELETE-880", "Error occurs during files suppression ({})".format(str(e)))
            # no rollback here: i.e. we also commit if error occur (most likely a
            # filesystem permission error). This is to keep medatata synced with
            # data (else many files would have
            # been removed from filesystem but with metadata still in db..).
            #
            # TODO: exception is too generic here:
            #       improve this code by using a specific exception for "permission error".
            #
            raise sdexception.FatalException
        files_deleted = dao.transfer_status_count(status=sdconst.TRANSFER_STATUS_DELETE)
    return files_deleted


def deferred_delete(file_functional_id):
    with session.create():
        f = dao.get_files(limit=1, file_functional_id=file_functional_id)
        f.status = sdconst.TRANSFER_STATUS_DELETE
        f.error_msg = None
        f.sdget_status = None
        f.sdget_error_msg = None
        dao.update_file(f)


def immediate_delete(tr):
    """
    Delete file (metadata and data).
    This method is called within a db session.

    Notes
        - This method remove files but not directories (directories are removed in "cleanup.sh" script)
    """
    sdlog.info("SDDELETE-055", "Delete transfer ({})".format(tr.get_full_local_path()))
    if os.path.isfile(tr.get_full_local_path()):
        try:
            os.remove(tr.get_full_local_path())
            # note: if data cannot be removed (i.e. exception is raised), we don't remove metadata
            dao.delete_file(tr)

        except Exception as e:
            sdlog.error("SDDELETE-528",
                        "Error occurs during file suppression ({},{})".format(tr.get_full_local_path(), str(e)))
            raise
    else:
        if tr.status == sdconst.TRANSFER_STATUS_DONE:
            # this case is not normal as the file should exist on filesystem when status is done

            sdlog.error("SDDELETE-123", "Can't delete file: file not found ({})".format(tr.get_full_local_path()))
        else:
            # this case is for 'waiting' and 'error' status
            # (in these cases, data do not exist, so we just remove metadata)

            dao.delete_file(tr)


def immediate_md_delete(tr):
    """
    Delete file (metadata only).
    This method is called within a db session.
    """
    sdlog.info("SDDELETE-080", "Delete metadata ({})".format(tr.get_full_local_path()))
    try:
        dao.delete_file(tr, commit=False)
    except Exception as e:
        sdlog.error("SDDELETE-128",
                    "Error occurs during file metadata suppression ({},{})".format(tr.get_full_local_path(), str(e)))


def reset():
    with session.create():
        nbr = dao.purge_error_and_waiting_transfer()
        sddeletedataset.purge_orphan_datasets()

    sdlog.info("SDDELETE-931", "{} transfer(s) removed".format(nbr))
    return nbr


def delete_transfers_lowmem(remove_all=True):
    """Perform the full deletion of DATA and METADATA in lowmem mode."""

    # This code uses loop for lowmem machine compatibility
    count = delete_transfers(100, remove_all)
    while count > 0:
        count = delete_transfers(100, remove_all)
