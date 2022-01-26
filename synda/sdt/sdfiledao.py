#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
from numpy import array as numpy_array

"""Contains file DAO SQL queries."""

from synda.sdt.sdexception import SDException
from synda.sdt import sdtime
from synda.sdt import sddb
from synda.sdt import sdsqlutils
from synda.sdt.sdtypes import File
from synda.sdt import sdlog
from synda.sdt.sdtime import SDTimer
from synda.sdt import sdsqlitedict

from synda.source.db.connection.models import get_db_connection
from synda.source.config.path.tree.default.models import Config as DefaultTreePath
from synda.source.config.file.user.preferences.models import Config as Preferences

from synda.source.config.process.download.constants import TRANSFER
from synda.source.config.file.internal.models import Config as Internal

preferences = Preferences()


def update_transfer_last_access_date(i__date, i__transfer_id, conn=None):
    if conn:
        transaction = True
    else:
        conn = get_db_connection()
        transaction = False
    # no commit here (will be committed in updatelastaccessdate())
    c = conn.cursor()
    c.execute("update file set last_access_date=? where file_id = ?", (i__date, i__transfer_id))
    c.close()

    if not transaction:
        conn.close()


def add_file(file, commit=True, conn=None):

    if conn:
        transaction = True
    else:
        conn = get_db_connection()
        transaction = False

    keys_to_insert=['status', 'crea_date', 'url', 'local_path', 'filename', 'file_functional_id', 'tracking_id', 'priority', 'checksum', 'checksum_type', 'size', 'variable', 'project', 'model', 'data_node', 'dataset_id', 'insertion_group_id', 'timestamp']
    # for future:, 'searchapi_host']

    if not Internal().is_processes_get_files_caching:
        id_ = sdsqlutils.insert(file, keys_to_insert, commit, conn)
        if not transaction:
            conn.close()
        return id_
    else:
        id_ = sdsqlutils.insert(file, keys_to_insert, commit, conn)

        priority = file.__dict__['priority']
        data_node = file.__dict__['data_node']
        hipri = highest_waiting_priority( data_node )
        if hipri is None or priority>hipri:
            # Compute cached max(priority) for the data node, ignoring any previous value.
            highest_waiting_priority( data_node, True, conn=conn)
        if not transaction:
            conn.close()
        return id_


def delete_file(tr, commit=True, conn=None):

    if conn:
        transaction = True
    else:
        conn = get_db_connection()
        transaction = False

    c = conn.cursor()

    c.execute("delete from selection__file where file_id=?", (tr.file_id,)) # also delete entries from junction table
    c.execute("delete from file where file_id=?", (tr.file_id,))
    # note that we don't delete entries (if any) from post_processing tables (this will be done in a batch procedure which will be manually executed from time to time)

    # TAGKRE45343J54K5JK
    if c.rowcount != 1:
        raise SDException("SYNCDDAO-908","file not found (file_id=%i,local_path=%s)"%(tr.file_id,tr.local_path,))

    c.close()

    if commit:
        conn.commit()

    if not transaction:
        conn.close()

# def exists_file(f,conn=sddb.conn):
#     """
#     Not used.
#     """
#     return exists_file_status(f , None, conn)


def exists_files_status(f,i__status,conn=None):
    """
    Not used.
    """
    found=False

    if conn:
        transaction = True
    else:
        conn = get_db_connection()
        transaction = False

    c = conn.cursor()

    if i__status!=None:
        q="select 1 from file where local_path='%s' and status='%s'" %(f.local_path,f.project,i__status)
    else:
        q="select 1 from file where local_path='%s'" %(f.local_path,f.project)

    c.execute(q)

    rs=c.fetchone()

    if rs==None:
        found=False
    else:
        found=True

    c.close()

    if not transaction:
        conn.close()

    return found

def get_file(file_functional_id,conn=None):
    """
    notes
      - returns None if file not found
      - return type is File
    """
    if conn:
        transaction = True
    else:
        conn = get_db_connection()
        transaction = False

    t=None

    c = conn.cursor()
    c.execute("select * from file where file_functional_id = ?", (file_functional_id,))
    rs=c.fetchone()
    if rs is not None:
        t=sdsqlutils.get_object_from_resultset(rs,File)
    c.close()

    if not transaction:
        conn.close()

    return t


# don't change arguments order here
def get_files(limit=None, conn=None, **search_constraints):
    """
    Notes
      - one search constraint must be given at least
      - if 'limit' is None, retrieve all records matching the search constraints
    """

    gfs0 = SDTimer.get_time()

    data_node = search_constraints.get('data_node', None)

    # Is the cache applicable to this situation?  Then use it, unless it's empty.
    if set(search_constraints.keys()) == set(['status', 'data_node']) and\
       search_constraints['status'] == TRANSFER["status"]['waiting'] and\
       limit == 1 and Internal().is_processes_get_files_caching:
        # ...limit==1 isn't essential, but the present coding is for limit==1
        use_cache = True
        if len(get_files.files.get(data_node, [])) > 0:
            gfs1 = SDTimer.get_elapsed_time(
                gfs0,
                show_microseconds=True,
            )
            sdlog.info(
                "SDFILDAO-200",
                "get_files time is {}, used cache, data_node {}".format(
                    gfs1,
                    data_node,
                ),
            )
            return [get_files.files[data_node].pop(0)]
        else:
            cachelen = 100
            limit += cachelen
    else:
        use_cache = False

    if conn:
        transaction = True
    else:
        conn = get_db_connection()
        transaction = False
    c = conn.cursor()

    files = []

    search_placeholder = sdsqlutils.build_search_placeholder(search_constraints)
    limit_clause = "limit %i" % limit if limit is not None else ""

    getfirst = priority_clause(
        data_node,
        use_cache,
        c,
    )

    if getfirst == '':
        if not transaction:
            c.close()
            conn.close()
        return []
    q = "select * from file where %s %s %s" % (search_placeholder, getfirst, limit_clause)
    import sqlite3
    try:
        c.execute(q, search_constraints)
        rs = c.fetchone()
        db_error = False
    except sqlite3.OperationalError as e:
        sdlog.info(
            "SDFILDAO-201",
            "sqlite3.OperationalError : {}".format(
                e,
            ),
        )
        db_error = True
        rs = None

    if db_error:
        if not transaction:
            c.close()
            conn.close()
        return []
    # if use_cache and (rs is None or len(rs)==0):
    if use_cache and (rs is None or len(rs) == 0):
        # No files found.  Possibly we could find one if we retry at another priority level.
        # Note that it makes no sense to do this if getfirst==''.  That has alread triggered
        # an early return.
        highest_waiting_priority(
            data_node,
            c,
        )   # compute the priority to retry at
        getfirst = priority_clause(
            data_node,
            use_cache,
            c,
        )

        q = "select * from file where %s %s %s" % (search_placeholder, getfirst, limit_clause)
        c.execute(q, search_constraints)
        rs = c.fetchone()
    while rs:
        files.append(
            sdsqlutils.get_object_from_resultset(
                rs,
                File,
            ),
        )
        rs = c.fetchone()

    if not transaction:
        c.close()
        conn.close()

    if len(files) > 1 and use_cache:
        # We shall return one of the files and cache the rest.
        get_files.files[data_node] = files[1:]
        files = files[0:1]

    gfs1 = SDTimer.get_elapsed_time(
        gfs0,
        show_microseconds=True,
    )

    sdlog.info(
        "SDFILDAO-200",
        "get_files time is %s, search %s with %s" % (gfs1, q, search_constraints),
    )

    return files


get_files.files = {}


def priority_clause( data_node, use_cache, cursor ):
    if use_cache:
        pri = highest_waiting_priority(data_node)
        if pri is None:
            getfirst = ''
        else:
            getfirst = "AND priority=%s" % pri
    else:
        getfirst = "ORDER BY priority DESC, checksum"
    return getfirst


def highest_waiting_priority(data_node, cursor=None, conn=None):
    """This function contains a dictionary-like cache of the highest priority among status='waiting'
    files for each data_node.  It will always return the dictionary value for the specified
    data node, or one of the specified data nodes if several are provided.
    - When called with a data_node and cursor, it will update its value for that data_node.
    - If cursor==True, then this function will create and close its own cursor.
    - If data_node==True, then this function will be applied to all data nodes.
    """
    if cursor is None:
        priority = highest_waiting_priority.vals.get(data_node, None)
        if isinstance(priority, str):
            try:
                priority = int(priority)
            except ValueError:
                priority = None
        return priority
    else:
        transaction = True
        if cursor==True:
            if not conn:
                transaction = False
                conn = get_db_connection()
            c = conn.cursor()
        else:
            conn = None
            c = cursor

        if data_node:
            q = "SELECT data_node FROM file GROUP BY data_node"
            c.execute(q)
            data_nodes = [tup[0] for tup in c.fetchall()]
        else:
            data_nodes = [data_node]

        for dn in data_nodes:
            hwp0 = SDTimer.get_time()
            q = "SELECT MAX(priority) FROM file WHERE status='waiting' AND data_node='%s'" % dn
            c.execute(q)
            val = c.fetchone()
            if len(val)>0:
                highest_waiting_priority.vals[dn] = val[0]
            else:
                highest_waiting_priority.vals.pop(dn,None)
            hwp1 = SDTimer.get_elapsed_time( hwp0, show_microseconds=True )
            #sdlog.info("SDFILDAO-300","time %s to recompute priority=%s for %s" %
            #           (hwp1,val[0],dn) )
            #sdlog.info("SDFILDAO-301","  query %s" % q )

        if cursor==True:
            c.close()
        priority = (highest_waiting_priority.vals).get(data_nodes[0], None) if data_nodes else None
        if isinstance(priority, str):
            try:
                priority = int(priority)
            except ValueError:
                priority = None
        if not transaction:
            conn.close()
        return priority
# The cache is a database masquerading as a dictionary.  A real dictionary in memory would be:
# highest_waiting_priority.vals = {}


default_db_folder = DefaultTreePath().get("db")

highest_waiting_priority.vals = sdsqlitedict.SqliteStringDict(
    default_db_folder + "/caches.db",
    'maxpri',
    None,
)


def get_dataset_files(d,conn=sddb.conn,limit=None, transaction=False):
    """
    Retrieves all dataset's files

    Args
        limit: if set, returns only a subset of datasets's files
    """
    files=[]

    c = conn.cursor()

    limit_clause="limit %i"%limit if limit is not None else ""

    q="select * from file where dataset_id = %i order by variable %s" % (d.dataset_id,limit_clause)

    c.execute(q)

    rs=c.fetchone()
    while rs!=None:
        files.append(sdsqlutils.get_object_from_resultset(rs,File))
        rs=c.fetchone()

    if not transaction:
        c.close()

    return files


def update_file(_file, commit=True, conn=None):

    keys = [
        'status',
        'error_msg',
        'sdget_status',
        'sdget_error_msg',
        'start_date',
        'end_date',
        'duration',
        'rate',
        'priority',
    ]

    if conn:
        transaction = True
    else:
        conn = get_db_connection()
        transaction = False

    # 'url' needs to be present when 'sdnexturl' feature is enabled
    next_url_on_error = Preferences().is_download_http_fallback

    if next_url_on_error:
        keys.append('url')
        keys.append('data_node')
        # for future: keys.append('searchapi_host')

    rowcount = sdsqlutils.update(
        _file,
        keys,
        commit,
        conn,
    )

    if not transaction:
        conn.close()

    # check
    if rowcount == 0:
        raise SDException(
            "SYNCDDAO-121",
            "file not found (file_id=%i)" % (i__tr.file_id,),
        )

    elif rowcount > 1:
        raise SDException(
            "SYNCDDAO-120",
            "duplicate functional primary key (file_id=%i)" % (i__tr.file_id,),
        )


def update_files(file_instances):
    for file_instance in file_instances:
        file_instance.start_date = sdtime.now()
        file_instance.end_date = sdtime.now()
        update_file(file_instance, commit=False)


def update_file_as_running(file_instance):
    file_instance.status = TRANSFER["status"]['running']
    update_file(file_instance, commit=True)


def update_file_before_download(file_instance):
    file_instance.start_date = sdtime.now()
    update_file(file_instance, commit=True)


def update_file_after_download(file_instance):
    update_file(file_instance, commit=True)


def validate_for_download(file_instance):
    validated = False
    lfae_mode = preferences.behaviour_lfae_mode

    file_instance.start_date = None
    file_instance.end_date = None
    file_instance.error_msg = None

    if lfae_mode == "keep":

        # usefull mode if
        #  - metadata needs to be regenerated without retransfering the data
        #  - synda files are mixed with files from other sources

        if os.path.isfile(file_instance.get_full_local_path()):
            # file already here, mark the file as done

            sdlog.info(
                "SYNDTASK-197",
                "Local file already exists: keep it (lfae_mode=keep, local_file={})".format(
                    file_instance.get_full_local_path(),
                ),
            )

            file_instance.status = TRANSFER["status"]['done']
            file_instance.error_msg = "Local file already exists: keep it (lfae_mode=keep)"

            # note: it is important not to update a running status in this case,
            # else local file non-related with synda may be removed by synda
            # (because of cleanup_running_transfer() func). See mail from Hans Ramthun at 20150331 for more details.

        else:
            validated = True

    elif lfae_mode == "replace":
        if os.path.isfile(file_instance.get_full_local_path()):
            sdlog.info(
                "SYNDTASK-187",
                "Local file already exists: remove it (lfae_mode=replace, local_file={})".format(
                    file_instance.get_full_local_path(),
                ),
            )
            os.remove(file_instance.get_full_local_path())
        # file_instance.status = TRANSFER["status"]['running']
        validated = True
    elif lfae_mode == "abort":
        if os.path.isfile(file_instance.get_full_local_path()):
            sdlog.info(
                "SYNDTASK-188",
                "Local file already exists: file_instance transfer aborted (lfae_mode=abort, local_file={})".format(
                    file_instance.get_full_local_path(),
                ),
            )

            file_instance.status = TRANSFER["status"]['error']
            file_instance.priority -= 1
            file_instance.error_msg = "Local file already exists: transfer aborted (lfae_mode=abort)"

        else:
            validated = True

    return validated


def sort_by_size_descending(files):
    sizes = numpy_array([_file.size for _file in files])
    ascending_indexes = sizes.argsort()
    descending_indexes = ascending_indexes[::-1]
    return [files[index] for index in descending_indexes]


def sort_by_size_ascending(files):
    sizes = numpy_array([_file.size for _file in files])
    ascending_indexes = sizes.argsort()
    return [files[index] for index in ascending_indexes]


def file_status_is_running(file_functional_id):
    _file = get_file(file_functional_id=file_functional_id)
    return _file.status == TRANSFER["status"]['running']


def cleanup_running_transfer():
    """This handle zombie cases (transfers with 'running' status, but not running).

    Check for zombie transfer (move "running" transfer to "waiting")

    Notes:
        - remaining "running" transfers exist if the daemon has been killed or if the server rebooted when the daemon was running)
        - if there are still transfers in running state, we switch them to waiting and remove file chunk
    """
    transfer_list = get_files(status=TRANSFER["status"]['running'])

    for t in transfer_list:
        sdlog.info(
            "SDTSCHED-023",
            "fixing transfer status (%s)" % t.get_full_local_path(),
        )

        if os.path.isfile(t.get_full_local_path()):
            os.remove(t.get_full_local_path())

        t.status = TRANSFER["status"]['waiting']
        update_file(t)
