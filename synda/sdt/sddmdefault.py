#!/usr/share/python/synda/sdt/bin/python
#jfp was
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains download management funcs (default implementation).

Note
    sddmdefault means 'SynDa Download Manager default'
"""

import os
import time
import queue
from synda.sdt import sdapp
from synda.sdt import sdlog
from synda.sdt import sdexception
from synda.sdt import sdlogon
from synda.sdt import sdconfig
from synda.sdt import sdtime
from synda.sdt import sdfiledao
# from synda.sdt import sdevent
from synda.sdt import sdutils
from synda.sdt import sdtools
from synda.sdt import sdget
from synda.sdt import sdtrace
from synda.sdt import sdnexturl
from synda.sdt import sdworkerutils

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.file.user.credentials.models import Config as Credentials
from synda.source.config.process.download.constants import get_http_clients
from synda.source.config.process.download.constants import TRANSFER
from synda.source.config.file.constants import CHECKSUM

preferences = Preferences()
credentials = Credentials()


class Download():
    # this flag is used to stop the event loop if exception occurs in thread
    exception_occurs = False

    @classmethod
    def run(cls, tr):
        cls.start_transfer_script(tr)

        # unset metrics fields if transfer did not complete successfully
        if tr.status != TRANSFER["status"]['done']:
            tr.duration = None
            tr.rate = None

    @classmethod
    def start_transfer_script(cls,tr):

        sdlog.info("JFPDMDEF-001", "Will download url={}".format(tr.url,))
        if sdconfig.fake_download:
            tr.status = TRANSFER["status"]['done']
            tr.error_msg = ""
            tr.sdget_error_msg = ""
            return

        # main
        tr.sdget_status,killed,tr.sdget_error_msg = sdget.download(
            tr.url,
            tr.get_full_local_path(),
            debug=False,
            http_client=get_http_clients()["wget"],
            timeout=Preferences().download_async_http_timeout,
            verbosity=0,
            buffered=True,
            hpss=hpss,
        )

        # check
        assert tr.size is not None

        # compute metrics
        tr.end_date = sdtime.now()
        tr.duration = sdtime.compute_duration(tr.start_date, tr.end_date)
        tr.rate = sdtools.compute_rate(tr.size, tr.duration)

        # post-processing
        if tr.sdget_status == 0:

            if int(tr.size) != os.path.getsize(tr.get_full_local_path()):
                sdlog.error(
                    "SDDMDEFA-002",
                    "size don't match (remote_size={}, local_size={}, local_path={})".format(
                        int(tr.size),
                        os.path.getsize(tr.get_full_local_path()),
                        tr.get_full_local_path(),
                    ),
                )

            # retrieve remote checksum
            remote_checksum = tr.checksum

            if remote_checksum:
                # remote checksum exists

                # compute local checksum
                # fallback to 'md5' (arbitrary)

                checksum_type = tr.checksum_type if tr.checksum_type is not None else CHECKSUM['type']["md5"]
                local_checksum = sdutils.compute_checksum(tr.get_full_local_path(), checksum_type)

                # compare local and remote checksum
                if remote_checksum == local_checksum:
                    # checksum is ok

                    tr.status = TRANSFER["status"]['done']
                    tr.error_msg = ""
                else:
                    # checksum is not ok

                    if incorrect_checksum_action == "remove":
                        tr.status = TRANSFER["status"]['error']
                        tr.priority -= 1
                        tr.error_msg = "File corruption detected: local checksum doesn't match remote checksum"

                        # remove file from local repository
                        sdlog.error(
                            "SDDMDEFA-155",
                            "checksum don't match: "
                            "remove local file (local_checksum={}, remote_checksum={}, local_path={})".format(
                                local_checksum,
                                remote_checksum,
                                tr.get_full_local_path(),
                            ),
                        )
                        try:
                            os.remove(
                                tr.get_full_local_path(),
                            )
                        except Exception as e:
                            sdlog.error(
                                "SDDMDEFA-158",
                                "error occurs while removing local file ({})".format(
                                    tr.get_full_local_path(),
                                ),
                            )

                    elif incorrect_checksum_action == "keep":
                        sdlog.info(
                            "SDDMDEFA-157",
                            "local checksum doesn't match remote checksum ({})".format(
                                tr.get_full_local_path(),
                            ),
                        )

                        tr.status = TRANSFER["status"]['done']
                        tr.error_msg = ""
                    else:
                        raise sdexception.FatalException(
                            "SDDMDEFA-507",
                            "incorrect value ({})".format(incorrect_checksum_action),
                        )
            else:
                # remote checksum is missing
                # NOTE: we DON'T store the local checksum ('file' table contains only the *remote* checksum)

                tr.status = TRANSFER["status"]['done']
                tr.error_msg = ""
        else:

            # Remove file if exists
            if os.path.isfile(tr.get_full_local_path()):
                try:
                    os.remove(tr.get_full_local_path())
                except Exception as e:
                    sdlog.error(
                        "SDDMDEFA-528",
                        "Error occurs during file suppression ({},{})".format(
                            tr.get_full_local_path(),
                            e,
                        ),
                    )

            # Set status
            if killed:

                # OLD WAY
                #tr.status=TRANSFER["status"]['waiting']
                #tr.error_msg="Error occurs during download (killed). Transfer marked for retry."

                # NEW WAY (TAG4JK4JJJ4454)
                #
                # We do not switch to 'waiting' anymore in this case, because
                # most often, process is killed by the watchdog for good
                # reason (e.g. the transfer process is frozen because of a
                # non-fixable server side problem).
                #
                # If we set to 'waiting' here, it will be retried for ever
                # without ending, causing synda to never complete a download
                # task (download task here means all files added and marked for
                # download  during a discovery step, e.g. 300 To of files).
                #
                # The downside of this new way of doing is that if the process
                # has been killed for bad reason (sudden reboot, watchdog kills
                # it because it was too slow or because of a temporary server
                # failure, etc..), then it will not be automatically retried
                # and will requires manual intervention.
                #
                # To solve this later problem, a high level manual retry system
                # must be implemented (directly in synda, or using crontab).
                #
                tr.status = TRANSFER["status"]['error']
                tr.priority -= 1
                tr.error_msg = "Download process has been killed"

                sdlog.error(
                    "SDDMDEFA-190",
                    "{} (file_id={},url={},local_path={})".format(
                        tr.error_msg,
                        tr.file_id,
                        tr.url,
                        tr.local_path,
                    ),
                )

            else:
                pass

            next_url_on_error = preferences.is_download_http_fallback

            if next_url_on_error:

                # Hack
                #
                # Notes
                #     - We need a log here so to have a trace of the original failed transfer
                # (i.e. in case the url-switch succeed, the error msg will be reset)
                #
                sdlog.info(
                    "SDDMDEFA-088",
                    "Transfer failed: try to use another url ({})".format(tr),
                )

                result = sdnexturl.run(tr)
                if result:
                    tr.status = TRANSFER["status"]['waiting']
                    tr.error_msg = ''
                else:
                    tr.status = TRANSFER["status"]['error']
                    tr.priority -= 1
                    tr.error_msg = 'Error occurs during download.'


            else:
                tr.status = TRANSFER["status"]['error']
                tr.priority -= 1
                tr.error_msg = 'Error occurs during download.'


def end_of_transfer(tr):

    # log
    if tr.status == TRANSFER["status"]['done']:
        sdlog.info(
            "SDDMDEFA-101",
            "Transfer done ({})".format(tr),
        )
    elif tr.status == TRANSFER["status"]['waiting']:
        # Transfer have been marked for retry
        #
        # This may happen for example
        #  - during shutdown immediate, where all running transfers are killed,
        # or when wget are 'stalled' and killed by watchdog
        #  - as a consequence of sdnexturl

        sdlog.info(
            "SDDMDEFA-108",
            "Transfer marked for retry (error_msg='{}',url={},file_id={}".format(
                tr.error_msg,
                tr.url,
                tr.file_id,
            ),
        )
    else:
        sdlog.info(
            "SDDMDEFA-102",
            "Transfer failed ({})".format(tr),
        )

    # update file
    sdfiledao.update_file(tr)

    # IMPORTANT: code below must run AFTER the file status has been saved in DB

    # check for fatal error
    if tr.sdget_status == 4:
        sdlog.info(
            "SDDMDEFA-147",
            "Stopping daemon as sdget.download() returned fatal error.",
        )
        raise sdexception.FatalException()


def start_transfer_thread(tr):
    th = sdworkerutils.WorkerThread(tr, eot_queue, Download)
    # if main thread quits, we kill running threads (note though that forked child processes are
    # NOT killed and continue running after that !)
    th.setDaemon(True)
    th.start()


def transfers_end():
    for i in range(8): # arbitrary
        try:
            task = eot_queue.get_nowait() # raises Empty when empty
            end_of_transfer(task)
            eot_queue.task_done()
        except queue.Empty as e:
            pass
        except sdexception.FatalException as e:
            raise
        except:
            # debug
            # sdtrace.log_exception(stderr=True)

            raise


def transfers_begin(transfers):
    # renew certificate if needed
    try:
        sdlogon.renew_certificate(
            credentials.openid,
            credentials.password,
            force_renew_certificate=False,
        )

    except Exception as e:
        sdlog.error(
            "SDDMDEFA-502",
            "Exception occured while retrieving certificate ({})".format(e),
        )

        raise

    for tr in transfers:
        start_transfer_thread(tr)
        # this sleep is not to be too agressive with datanodes
        time.sleep(1)


def can_leave():
    return eot_queue.empty()


def fatal_exception():
    return Download.exception_occurs

# module init.

# hpss & parse_output hack


hpss = preferences.is_download_hpss

# eot means "End Of Task"
eot_queue = queue.Queue()
incorrect_checksum_action = preferences.behaviour_incorrect_checksum_action
