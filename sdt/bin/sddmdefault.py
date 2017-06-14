#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains download management funcs (default implementation).

Note
    sddmdefault means 'SynDa Download Manager default'
"""

import os
import time
import Queue
import sdapp
import sdlog
import sdconst
import sdexception
import sdlogon
import sdconfig
import sdtime
import sdfiledao
import sdevent
import sdutils
import sdtools
import sdget
import sdtrace
import sdnexturl
import sdworkerutils

class Download():
    exception_occurs=False # this flag is used to stop the event loop if exception occurs in thread

    @classmethod
    def run(cls,tr):
        cls.start_transfer_script(tr)

        # unset metrics fields if transfer did not complete successfully
        if tr.status!=sdconst.TRANSFER_STATUS_DONE:
            tr.duration=None
            tr.rate=None

    @classmethod
    def start_transfer_script(cls,tr):

        if sdconfig.fake_download:
            tr.status=sdconst.TRANSFER_STATUS_DONE
            tr.error_msg=""
            tr.sdget_error_msg=""
            return

        # main
        (tr.sdget_status,killed,tr.sdget_error_msg)=sdget.download(tr.url,
                                                                   tr.get_full_local_path(),
                                                                   debug=False,
                                                                   http_client=sdconst.HTTP_CLIENT_WGET,
                                                                   timeout=sdconst.ASYNC_DOWNLOAD_HTTP_TIMEOUT,
                                                                   verbosity=0,
                                                                   buffered=True,
                                                                   hpss=hpss)


        # check
        assert tr.size is not None

        # compute metrics
        tr.end_date=sdtime.now()
        tr.duration=sdtime.compute_duration(tr.start_date,tr.end_date)
        tr.rate=sdtools.compute_rate(tr.size,tr.duration)

        # post-processing
        if tr.sdget_status==0:

            if int(tr.size) != os.path.getsize(tr.get_full_local_path()):
                sdlog.error("SDDMDEFA-002","size don't match (remote_size=%i,local_size=%i,local_path=%s)"%(int(tr.size),os.path.getsize(tr.get_full_local_path()),tr.get_full_local_path()))

            # retrieve remote checksum
            remote_checksum=tr.checksum

            if remote_checksum!=None:
                # remote checksum exists

                # compute local checksum
                checksum_type=tr.checksum_type if tr.checksum_type is not None else sdconst.CHECKSUM_TYPE_MD5 # fallback to 'md5' (arbitrary)
                local_checksum=sdutils.compute_checksum(tr.get_full_local_path(),checksum_type)

                # compare local and remote checksum
                if remote_checksum==local_checksum:
                    # checksum is ok

                    tr.status=sdconst.TRANSFER_STATUS_DONE
                    tr.error_msg=""
                else:
                    # checksum is not ok

                    if incorrect_checksum_action=="remove":
                        tr.status=sdconst.TRANSFER_STATUS_ERROR
                        tr.error_msg="File corruption detected: local checksum doesn't match remote checksum"

                        # remove file from local repository
                        sdlog.error("SDDMDEFA-155","checksum don't match: remove local file (local_checksum=%s,remote_checksum=%s,local_path=%s)"%(local_checksum,remote_checksum,tr.get_full_local_path()))
                        try:
                            os.remove(tr.get_full_local_path())
                        except Exception,e:
                            sdlog.error("SDDMDEFA-158","error occurs while removing local file (%s)"%tr.get_full_local_path())

                    elif incorrect_checksum_action=="keep":
                        sdlog.info("SDDMDEFA-157","local checksum doesn't match remote checksum (%s)"%tr.get_full_local_path())
                        
                        tr.status=sdconst.TRANSFER_STATUS_DONE
                        tr.error_msg=""
                    else:
                        raise sdexception.FatalException("SDDMDEFA-507","incorrect value (%s)"%incorrect_checksum_action)
            else:
                # remote checksum is missing
                # NOTE: we DON'T store the local checksum ('file' table contains only the *remote* checksum)

                tr.status=sdconst.TRANSFER_STATUS_DONE
                tr.error_msg=""
        else:

            # Remove file if exists
            if os.path.isfile(tr.get_full_local_path()):
                try:
                    os.remove(tr.get_full_local_path())
                except Exception,e:
                    sdlog.error("SDDMDEFA-528","Error occurs during file suppression (%s,%s)"%(tr.get_full_local_path(),str(e)))

            # Set status
            if killed:

                # OLD WAY
                #tr.status=sdconst.TRANSFER_STATUS_WAITING
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
                tr.status=sdconst.TRANSFER_STATUS_ERROR
                tr.error_msg="Download process has been killed"

                sdlog.error("SDDMDEFA-190","%s (file_id=%d,url=%s,local_path=%s)"%(tr.error_msg,tr.file_id,tr.url,tr.local_path))
            else:

                if sdconfig.next_url_on_error:


                    # Hack
                    #
                    # Notes
                    #     - Only active for gridftp url to prevent having useless log message (i.e. there is currently no url switching mecanism for http url)
                    #     - We need a log here so to have a trace of the original failed transfer (i.e. in case the url-switch succeed, the error msg will be reset)
                    #
                    transfer_protocol=sdutils.get_transfer_protocol(tr.url)
                    if transfer_protocol==sdconst.TRANSFER_PROTOCOL_GRIDFTP:
                        sdlog.info("SDDMDEFA-088","Transfer failed: try to use another url (%s)"%str(tr))


                    result=sdnexturl.run(tr)
                    if result:
                        tr.status=sdconst.TRANSFER_STATUS_WAITING
                        tr.error_msg=''
                    else:
                        tr.status=sdconst.TRANSFER_STATUS_ERROR
                        tr.error_msg='Error occurs during download.'


                else:
                    tr.status=sdconst.TRANSFER_STATUS_ERROR
                    tr.error_msg='Error occurs during download.'

def end_of_transfer(tr):

    # log
    if tr.status==sdconst.TRANSFER_STATUS_DONE:
        sdlog.info("SDDMDEFA-101","Transfer done (%s)"%str(tr))
    elif tr.status==sdconst.TRANSFER_STATUS_WAITING:
        # Transfer have been marked for retry
        #
        # This may happen for example
        #  - during shutdown immediate, where all running transfers are killed, or when wget are 'stalled' and killed by watchdog
        #  - as a consequence of sdnexturl
        
        sdlog.info("SDDMDEFA-108","Transfer marked for retry (error_msg='%s',url=%s,file_id=%d"%(tr.error_msg,tr.url,tr.file_id))
    else:
        sdlog.info("SDDMDEFA-102","Transfer failed (%s)"%str(tr))

    # update file
    sdfiledao.update_file(tr)

    # IMPORTANT: code below must run AFTER the file status has been saved in DB

    if tr.status==sdconst.TRANSFER_STATUS_DONE:
        sdevent.file_complete_event(tr) # trigger 'file complete' event

    # TODO: maybe do some rollback here in case fatal exception occurs in 'file_complete_event'
    #       (else, we have a file marked as 'done' with the corresponding event un-triggered)

    # check for fatal error
    if tr.sdget_status==4:
        sdlog.info("SDDMDEFA-147","Stopping daemon as sdget.download() returned fatal error.")
        raise sdexception.FatalException()

def start_transfer_thread(tr):
    th=sdworkerutils.WorkerThread(tr,eot_queue,Download)
    th.setDaemon(True) # if main thread quits, we kill running threads (note though that forked child processes are NOT killed and continue running after that !)
    th.start()

def transfers_end():
    for i in range(8): # arbitrary
        try:
            task=eot_queue.get_nowait() # raises Empty when empty
            end_of_transfer(task)
            eot_queue.task_done()
        except Queue.Empty, e:
            pass
        except sdexception.FatalException, e:
            raise
        except:

            # debug
            #sdtrace.log_exception(stderr=True)

            raise

def transfers_begin(transfers):

    # renew certificate if needed
    try:
        sdlogon.renew_certificate(sdconfig.openid,sdconfig.password,force_renew_certificate=False)
    except Exception,e:
        sdlog.error("SDDMDEFA-502","Exception occured while retrieving certificate (%s)"%str(e))
        raise

    for tr in transfers:
        start_transfer_thread(tr)
        time.sleep(1) # this sleep is not to be too agressive with datanodes

def can_leave():
    return eot_queue.empty()

def fatal_exception():
    return Download.exception_occurs

# module init.

hpss=sdconfig.config.getboolean('download','hpss') # hpss & parse_output hack
eot_queue=Queue.Queue() # eot means "End Of Task"
incorrect_checksum_action=sdconfig.config.get('behaviour','incorrect_checksum_action')
