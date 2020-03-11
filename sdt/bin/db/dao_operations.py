import os
from sdt.bin.commons.utils import sdlog
from sdt.bin.commons.utils import sdconst
from sdt.bin.db import session
from sdt.bin.db import dao


def delete_transfers(limit=None, remove_all=True):
    """Perform the deletion of METADATA.

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
        sdlog.error("SDDELETE-880", "Error occurs during files suppression ({})".format(str(e), ))
        raise  # fatal error
    with session.create():
        transfer_count = dao.transfer_status_count(status=sdconst.TRANSFER_STATUS_DELETE)
    return transfer_count


def immediate_delete(tr):
    """Delete file (metadata and data).

    Notes
        - This method remove files but not directories (directories are removed in "cleanup.sh" script)
    """
    sdlog.info("SDDELETE-055", "Delete transfer ({})".format(tr.get_full_local_path()))

    if os.path.isfile(tr.get_full_local_path()):
        try:
            os.remove(tr.get_full_local_path())
            # note: if data cannot be removed (i.e. exception is raised), we don't remove metadata
            with session.create():
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
            # this case is for 'waiting' and 'error' status (in these cases, data do not exist, so we just remove metadata)
            with session.create():
                dao.delete_file(tr)


def immediate_md_delete(tr):
    """Delete file (metadata only)."""
    sdlog.info("SDDELETE-080", "Delete metadata ({})".format(tr.get_full_local_path()))
    try:
        with session.create():
            dao.delete_file(tr)
    except Exception as e:
        sdlog.error("SDDELETE-128",
                    "Error occurs during file metadata suppression ({},{})".format(tr.get_full_local_path(), str(e)))


def next_url(tr):
    """
        Returns
            True: url has been switched to a new one
            False: nothing changed (same url)
        """
    try:

        conn = sqlite3.connect(sdconfig.db_file, 120)  # 2 minute timeout
        c = conn.cursor()
        c.execute("INSERT INTO failed_url(url,file_id) VALUES (?," +
                  "(SELECT file_id FROM file WHERE file_functional_id=?))",
                  (tr.url, tr.file_functional_id))
        conn.commit()
    except sqlite3.IntegrityError as e:
        # url is already in the failed_url table
        sdlog.info("SDNEXTUR-001", "During database operations, IntegrityError %s" % (e,))
    except Exception as e:
        sdlog.info("SDNEXTUR-002", "During database operations, unknown exception %s" % (e,))
        return False
    finally:
        c.close()

    try:
        next_url(tr, conn)
        return True
    except sdexception.FileNotFoundException as e:
        sdlog.info("SDNEXTUR-003", "Cannot switch url for %s (FileNotFoundException)" % (tr.file_functional_id,))
        return False
    except sdexception.NextUrlNotFoundException as e:
        sdlog.info("SDNEXTUR-004", "Cannot switch url for %s (NextUrlNotFoundException)" % (tr.file_functional_id,))
        return False
    except Exception as e:
        sdlog.info("SDNEXTUR-005",
                   "Unknown exception (file_functional_id=%s,exception=%s)" % (tr.file_functional_id, str(e)))
        conn.close()
        return False
    finally:
        conn.close()
