#!/usr/bin/env python

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                            All Rights Reserved"
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains funcs used in 'sdtaskscheduler' module."""

import sys
import os

from sdt.bin.commons.utils import sdconfig
from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils import sdlog
from sdt.bin.commons.utils import sdtime
from sdt.bin.commons.utils.sdexception import *

from sdt.bin.commons.daemon import sdprofiler
from sdt.bin.commons import sdtrace
from sdt.bin.models import sdtypes
from sdt.bin.db import dao

import sddeletefile


@sdprofiler.timeit
def delete_transfers():
    sddeletefile.delete_transfers(limit=100)


@sdprofiler.timeit
def transfers_end():
    """Process end of transfer instructions.

    When a task is done, tasks are enqueued. Those tasks are then processed by
    this function.
    """

    dmngr.transfers_end()


def prepare_transfer(tr):
    # we reset values from previous try if any
    tr.end_date = None
    tr.error_msg = None
    tr.status = sdconst.TRANSFER_STATUS_RUNNING
    tr.start_date = sdtime.now()


def pre_transfer_check_list(tr):
    """
    Return:
        Check list status

        True: Check list OK
        False: Check list NOK
    """

    if lfae_mode == "keep":
        # usefull mode if
        #  - metadata needs to be regenerated without retransfering the data
        #  - synda files are mixed with files from other sources

        if os.path.isfile(tr.get_full_local_path()):
            # file already here, mark the file as done

            sdlog.info("SYNDTASK-197",
                       "Local file already exists: keep it (lfae_mode=keep,local_file=%s)" % tr.get_full_local_path())

            tr.status = sdconst.TRANSFER_STATUS_DONE
            tr.error_msg = "Local file already exists: keep it (lfae_mode=keep)"
            tr.end_date = sdtime.now()
            # note: it is important not to update a running status in this case, else local file non-related with synda
            # may be removed by synda (because of cleanup_running_transfer() func).
            # See mail from Hans Ramthun at 20150331 for more details.

            dao.update_file(tr)

            return False
        else:
            # file not here, start the download

            return True
    elif lfae_mode == "replace":
        if os.path.isfile(tr.get_full_local_path()):
            sdlog.info("SYNDTASK-187",
                       "Local file already exists: remove it (lfae_mode=replace,local_file=%s)" % tr.get_full_local_path())
            os.remove(tr.get_full_local_path())

        return True
    elif lfae_mode == "abort":
        if os.path.isfile(tr.get_full_local_path()):
            sdlog.info("SYNDTASK-188",
                       "Local file already exists: transfer aborted (lfae_mode=abort,local_file=%s)" % tr.get_full_local_path())

            tr.status = sdconst.TRANSFER_STATUS_ERROR
            tr.priority -= 1
            tr.error_msg = "Local file already exists: transfer aborted (lfae_mode=abort)"
            tr.end_date = sdtime.now()
            dao.update_file(tr)

            return False
        else:
            return True


@sdprofiler.timeit
def transfers_begin():
    transfers = []

    # how many new transfers can be started:
    new_transfer_count = max_transfer - dao.transfer_status_count(status=sdconst.TRANSFER_STATUS_RUNNING)
    # datanode_count[datanode], is number of running transfers for a data node:
    datanode_count = dao.transfer_running_count_by_datanode()
    if new_transfer_count > 0:
        transfers_needed = new_transfer_count
        for i in range(new_transfer_count):
            for datanode in datanode_count.keys():
                try:
                    # Handle per-datanode maximum number of transfers:
                    try:
                        new_count = max_datanode_count - datanode_count[datanode]
                    except KeyError:
                        sdlog.info("SYNDTASK-189", "key error on datanode {}, "
                                                   "legal keys are {}".format(datanode, datanode_count.keys()))
                        new_count = max_datanode_count
                    if new_count <= 0:
                        continue

                    tr = dao.get_one_waiting_transfer(datanode)

                    prepare_transfer(tr)

                    if pre_transfer_check_list(tr):
                        dao.update_file(tr)
                        transfers.append(tr)

                    if datanode in datanode_count:
                        datanode_count[datanode] += 1
                    else:
                        datanode_count[datanode] = 1
                    transfers_needed -= 1
                    if transfers_needed <= 0:
                        break
                except NoTransferWaitingException as e:
                    pass
            if transfers_needed <= 0:
                break

    dmngr.transfers_begin(transfers)


def get_download_manager():
    download_manager = 'globustransfer_dm' if sdconfig.config.getboolean('module', 'globustransfer') else 'default_dm'

    if download_manager == 'globustransfer_dm':
        import sddmgo
        return sddmgo
    elif download_manager == 'default_dm':
        import sddmdefault
        return sddmdefault
    else:
        assert False


def can_leave():
    return dmngr.can_leave()


def fatal_exception():
    return dmngr.fatal_exception()


# init.

max_transfer = sdconfig.config.getint('download', 'max_parallel_download')
max_datanode_count = sdconfig.config.getint('download', 'max_parallel_download_per_datanode')
lfae_mode = sdconfig.config.get('behaviour', 'lfae_mode')

dmngr = get_download_manager()
