#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains download high level functions."""

import os
import traceback
import Queue
import sdapp
import sdlog
import sdconst
from sdexception import SDException,FatalException
import sdlogon
import sdconfig
import sdtime
import sdfiledao
import sdevent
import sdget
from sdworkerutils import WorkerThread

class Download():
    exception_occurs=False # this flag is used to stop the event loop if exception occurs in thread

    @classmethod
    def run(cls,tr):
        cls.start_transfer_script(tr)
        tr.end_date=sdtime.now()

    @classmethod
    def start_transfer_script(cls,tr):

        # renew certificate if needed
        try:
            sdlogon.renew_certificate(False)
        except Exception,e:
            sdlog.error("SDDOWNLO-502","Exception occured while retrieving certificate (%s)"%str(e))
            raise

        checksum_type=tr.checksum_type if tr.checksum_type is not None else 'md5'

        (tr.sdget_status,local_checksum,killed,script_stdxxx)=sdget.download(tr.url,tr.get_full_local_path(),checksum_type)

        if tr.sdget_status==0:

            tr.status=sdconst.TRANSFER_STATUS_DONE

            assert tr.size is not None

            if int(tr.size) != os.path.getsize(tr.get_full_local_path()):
                sdlog.error("SDDOWNLO-002","size don't match (remote_size=%i,local_size=%i,local_path=%s)"%(int(tr.size),os.path.getsize(tr.get_full_local_path()),tr.get_full_local_path()))

            # retrieve remote checksum
            remote_checksum=tr.checksum

            if remote_checksum!=None:
                # remote checksum exists

                # compare local and remote checksum
                if remote_checksum==local_checksum:

                    # checksum is ok, nothing to do
                    pass
                else:
                    # checksum is not ok

                    if incorrect_checksum_action=="remove":
                        tr.status=sdconst.TRANSFER_STATUS_ERROR
                        tr.error_msg="File corruption detected: local checksum doesn't match remote checksum"

                        # remove file from local repository
                        sdlog.error("SDDOWNLO-155","checksum don't match: remove local file (local_checksum=%s,remote_checksum=%s,local_path=%s)"%(local_checksum,remote_checksum,tr.get_full_local_path()))
                        try:
                            os.remove(tr.get_full_local_path())
                        except Exception,e:
                            sdlog.error("SDDOWNLO-158","error occurs while removing local file (%s)"%tr.get_full_local_path())

                    elif incorrect_checksum_action=="keep":
                        sdlog.info("SDDOWNLO-157","local checksum doesn't match remote checksum (%s)"%tr.get_full_local_path())
                        
                        tr.status=sdconst.TRANSFER_STATUS_DONE
                        tr.error_msg=""

                    else:
                        raise SDException("SDDOWNLO-507","incorrect value (%s)"%incorrect_checksum_action)
            else:
                # remote checksum is missing

                pass # we DON'T store the local checksum ('file' table contains only the *remote* checksum)
        else:

            # Remove file if exists
            if os.path.isfile(tr.get_full_local_path()):
                try:
                    os.remove(tr.get_full_local_path())
                except Exception,e:
                    sdlog.error("SDDOWNLO-528","Error occurs during file suppression (%s,%s)"%(tr.get_full_local_path(),str(e)))

            # Set status
            if killed:
                tr.status=sdconst.TRANSFER_STATUS_WAITING
                tr.error_msg="Error occurs during download (killed). Transfer marked for retry."
            else:
                tr.status=sdconst.TRANSFER_STATUS_ERROR
                tr.error_msg="Error occurs during download."

def end_of_transfer(tr):
    # log
    if tr.status==sdconst.TRANSFER_STATUS_DONE:
        sdlog.info("SDDOWNLO-101","Transfer done (%s)"%str(tr))
    elif tr.status==sdconst.TRANSFER_STATUS_WAITING:
        # Transfer have been marked for retry
        # (this happens for example during shutdown immediate, where
        # all running transfers are killed, or when wget are 'stalled'
        # and killed by watchdog)
        
        sdlog.info("SDDOWNLO-108","%s"%(tr.error_msg,))
        #sdlog.info("SDDOWNLO-104","Transfer marked for retry (%s)"%str(tr))
    else:
        sdlog.info("SDDOWNLO-102","Transfer failed (%s)"%str(tr))

    # update file
    sdfiledao.update_file(tr)

    # IMPORTANT: code below must run AFTER the file status has been saved in DB

    if tr.status==sdconst.TRANSFER_STATUS_DONE:
        sdevent.file_complete_event(tr) # trigger 'file complete' event

    # TODO: maybe do some rollback here in case fatal exception occurs in 'file_complete_event'
    #       (else, we have a file marked as 'done' with the corresponding event un-triggered)

    # check for fatal error
    if tr.sdget_status==4:
        sdlog.info("SDDOWNLO-147","Stopping daemon as sdget.download() returns fatal error.")
        raise FatalException()

def start_transfer_thread(tr):
    th=WorkerThread(tr,eot_queue,Download)
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
        except FatalException, e:
            raise
        except:

            # debug
            #traceback.print_exc(file=sys.stderr)
            #traceback.print_exc(file=open(sdconfig.stacktrace_log_file,"a"))

            raise

def can_leave():
    return eot_queue.empty()

# module init.

eot_queue=Queue.Queue() # eot means "End Of Task"
incorrect_checksum_action=sdconfig.config.get('behaviour','incorrect_checksum_action')
