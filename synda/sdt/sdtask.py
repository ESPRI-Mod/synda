#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
# @program        synda
# @description    climate models data transfer program
# @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                            All Rights Reserved"
# @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
 
"""This module contains funcs used in 'sdtaskscheduler' module."""
import os
import sdfiledao
import sddao
import sdfilequery
import sdtime
import sdlog
import sddeletefile
from sdexception import NoTransferWaitingException

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.process.download.constants import TRANSFER
from synda.source.config.file.user.preferences.decorators import report_elapsed_time_into_log_file

preferences = Preferences()
scheduler_profiling = preferences.log_scheduler_profiling


@report_elapsed_time_into_log_file(scheduler_profiling)
def delete_transfers():
    sddeletefile.delete_transfers(limit=100)


@report_elapsed_time_into_log_file(scheduler_profiling)
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
    tr.status = TRANSFER["status"]['running']
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

            sdlog.info(
                "SYNDTASK-197",
                "Local file already exists: keep it (lfae_mode=keep, local_file={})".format(
                    tr.get_full_local_path(),
                ),
            )

            tr.status = TRANSFER["status"]['done']
            tr.error_msg = "Local file already exists: keep it (lfae_mode=keep)"
            tr.end_date = sdtime.now()
            # note: it is important not to update a running status in this case,
            # else local file non-related with synda may be removed by synda
            # (because of cleanup_running_transfer() func). See mail from Hans Ramthun at 20150331 for more details.
            sdfiledao.update_file(tr)

            return False
        else:
            # file not here, start the download

            return True

    elif lfae_mode == "replace":
        if os.path.isfile(tr.get_full_local_path()):
            sdlog.info(
                "SYNDTASK-187",
                "Local file already exists: remove it (lfae_mode=replace, local_file={})".format(
                    tr.get_full_local_path(),
                ),
            )
            os.remove(tr.get_full_local_path())

        return True
    elif lfae_mode == "abort":
        if os.path.isfile(tr.get_full_local_path()):
            sdlog.info(
                "SYNDTASK-188",
                "Local file already exists: transfer aborted (lfae_mode=abort, local_file={})".format(
                    tr.get_full_local_path(),
                ),
            )

            tr.status = TRANSFER["status"]['error']
            tr.priority -= 1
            tr.error_msg = "Local file already exists: transfer aborted (lfae_mode=abort)"
            tr.end_date = sdtime.now()
            sdfiledao.update_file(tr)

            return False
        else:
            return True


@report_elapsed_time_into_log_file(scheduler_profiling)
def transfers_begin():
    transfers = []

    # how many new transfers can be started:
    new_transfer_count = max_transfer - sdfilequery.transfer_running_count()
    # running_datanode_counts[datanode], is number of running transfers for a data node:
    running_datanode_counts = sdfilequery.transfer_running_count_by_datanode()
    waiting_datanodes = running_datanode_counts.keys()
    if new_transfer_count > 0:
        transfers_needed = new_transfer_count

        for i in range(new_transfer_count):
            try:
                for datanode in waiting_datanodes:
                    # Handle per-datanode maximum number of transfers:
                    try:
                        # First check for a special max specific to this datanode, e.g. 3 if
                        # mpdsdd={ "ec.gc.ca":3 } and datanode='crd-esgf-drc.ec.gc.ca'
                        # We expect mpdsdd to be very short; otherwise performance will be poor.
                        special_maxes = [ value for key,value in mpdsdd.items() if key in datanode ]
                        if len(special_maxes)==0:
                            new_count = max_datanode_count - running_datanode_counts[datanode]
                        else:
                            new_count = special_maxes[0] - running_datanode_counts[datanode]
                    except KeyError:  # probably not possible any more
                        sdlog.info(
                            "SYNDTASK-189",
                            "key error on datanode {}, legal keys are {}".format(
                                datanode,
                                running_datanode_counts.keys(),
                            ),
                        )
                        new_count = max_datanode_count
                    if new_count <= 0:
                        continue

                    tr = sddao.get_one_waiting_transfer(datanode)
                    prepare_transfer(tr)
                    if pre_transfer_check_list(tr):
                        sdfiledao.update_file(tr)
                        transfers.append(tr)


                    running_datanode_counts[datanode] += 1
                    transfers_needed -= 1
                    if transfers_needed <= 0:
                        break

            except NoTransferWaitingException, e:
                break
            if transfers_needed <= 0:
                break

    sdlog.info("SYNDTASK-190","ready to call transfers_begin on %s transfers"%
               len(transfers) )
    dmngr.transfers_begin(transfers)


def get_download_manager():

    import sddmdefault
    return sddmdefault


def can_leave():
    return dmngr.can_leave()


def fatal_exception():
    return dmngr.fatal_exception()

# init.


max_transfer = preferences.download_max_parallel_download

max_datanode_count = preferences.download_max_parallel_download_per_datanode

mpdsd = preferences.download_max_parallel_download_special_datanodes
#...e.g. "crd-esgf-drc:3, tropmet:1"
if mpdsd=='':
    mpdsdd = {}
else:
    try:
        mpdsdd = eval('{"'+mpdsd.replace(' ','').replace(':','":').replace(',',',"')+'}')
        #...e.g. {"crd-esgf-drc":3, "tropmet":1}
    except:
        mpdsdd = {}
        sdlog.warning("SYNDTASK-250","trouble parsing max_parallel_download_special_datanodes=%s"
                   % mpdsd )
#...e.g. {"crd-esgf-drc}:3, "tropmet":1}


lfae_mode = preferences.behaviour_lfae_mode

dmngr = get_download_manager()
