#!/usr/share/python/synda/sdt/bin/python
#jfp was
# -*- coding: ISO-8859-1 -*-

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
from sdtime import SDTimer

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

        if hasattr( tr, 'delay' ):
            time.sleep( tr.delay )
        else:
            sdlog.warning("SDDMDEFA-001","delay attribute not set for transfer %s"%(tr,))
        sdlog.info("JFPDMDEF-001","Will download url=%s"%(tr.url,))
#        sts0 = SDTimer.get_time()
        if sdconfig.fake_download:
            tr.status=sdconst.TRANSFER_STATUS_DONE
            tr.error_msg=""
            tr.sdget_error_msg=""
            return

        # main
        sdget0 = SDTimer.get_time()
        (tr.sdget_status,killed,tr.sdget_error_msg)\
            = sdget.download( tr.url,
                              tr.get_full_local_path(),
                              debug=False,
                              http_client=sdconst.HTTP_CLIENT_WGET,
                              timeout=sdconst.ASYNC_DOWNLOAD_HTTP_TIMEOUT,
                              verbosity=0,
                              buffered=True,
                              hpss=hpss )
        sdget1 = SDTimer.get_elapsed_time(sdget0, show_microseconds=True)
        sdlog.info("JFPDMDEF-010","%s sdget_download time for %s, status %s"%
                   (sdget1,tr.url,tr.sdget_status))


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
#                sum0 = SDTimer.get_time()
                local_checksum=sdutils.compute_checksum(tr.get_full_local_path(),checksum_type)
#                sum1 = SDTimer.get_elapsed_time(sum0, show_microseconds=True)
#                sdlog.info("JFPDMDEF-020","%s compute_checksum time for %s"%(sum1,tr.url))

                # compare local and remote checksum
                if remote_checksum==local_checksum:
                    # checksum is ok

                    tr.status=sdconst.TRANSFER_STATUS_DONE
                    tr.error_msg=""
                else:
                    # checksum is not ok
                    update_error_history( tr, "bad checksum" )

                    if incorrect_checksum_action=="remove":
                        tr.status=sdconst.TRANSFER_STATUS_ERROR
                        tr.priority -= 1
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
        else:   # tr.sdget_status != 0:

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
                tr.priority -= 1
                tr.error_msg="Download process has been killed"

                sdlog.error("SDDMDEFA-190","%s (file_id=%d,url=%s,local_path=%s)"%(tr.error_msg,tr.file_id,tr.url,tr.local_path))
                update_error_history( tr, 'killed' )
            elif tr.sdget_error_msg.find('ERROR 404')>0:
                # wget reported 'ERROR 404', i.e. the url was not found.
                update_error_history( tr, 'ERROR 404' )
            else:
                update_error_history( tr, 'other' )

            if sdconfig.next_url_on_error:


                # Hack
                #
                # Notes
                #     - We need a log here so to have a trace of the original failed transfer (i.e. in case the url-switch succeed, the error msg will be reset)
                #
                sdlog.info("SDDMDEFA-088","Transfer failed: try to use another url (%s)"%str(tr))

                result=sdnexturl.run(tr)
                if result:
                    tr.status=sdconst.TRANSFER_STATUS_WAITING
                    tr.error_msg=''
                else:
                    tr.status=sdconst.TRANSFER_STATUS_ERROR
                    tr.priority -= 1
                    tr.error_msg='Error occurs during download.'


            else:  # i.e., if not sdconfig.next_url_on_error
                tr.status=sdconst.TRANSFER_STATUS_ERROR
                tr.priority -= 1
                tr.error_msg='Error occurs during download.'

#        sts1 = SDTimer.get_elapsed_time(sts0, show_microseconds=True)
#        sdlog.info("JFPDMDEF-030","%s    Total elapsed time for %s"%(sts1,tr.url))

def update_error_history( tr, error ):
    """update the error_history field of a transfer, to add the specified error, a string
     The error should be short, e.g. 'ERROR 404'.  And it should be specific to the file
     represented by tr. Thus an error 503 or "Connection refused" should not be provided."""
    if tr.error_history is None:
        tr.error_history = str([])
    error_history = eval(tr.error_history)
    error_history.append( ( sdtime.now(), error ) )
    tr.error_history = str(error_history)
    sdlog.info( "SDDMDEFA-080","error history for %s is %s" % (tr.filename,tr.error_history) )

def end_of_transfer(tr):

#    eotr0 = SDTimer.get_time() #jfp
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

#    eotr1 = SDTimer.get_elapsed_time( eotr0, show_microseconds=True ) #jfp
#    sdlog.info("JFPDMDEF-100","%s    end_of_transfer time for transfer %s"%(eotr1,tr.url))
    # TODO: maybe do some rollback here in case fatal exception occurs in 'file_complete_event'
    #       (else, we have a file marked as 'done' with the corresponding event un-triggered)

    # check for fatal error
    if tr.sdget_status==4:
        sdlog.info("SDDMDEFA-147","Stopping daemon as sdget.download() returned fatal error.")
        raise sdexception.FatalException()

def start_transfer_thread(tr):
    th=sdworkerutils.WorkerThread(tr,eot_queue,Download)
    th.setDaemon(True) # if main thread quits, we kill running threads (note though that forked child processes are NOT killed and continue running after that !)
    try:
        th.start()
    except Exception as e:
        sdlog.info("JFPDMDEF-105","th.start raised exception %s for transfer %s"%(e,tr))
        raise

def transfers_end():
#    trend0 = SDTimer.get_time()
    nq = eot_queue.qsize()   #jfp
    for i in range(nq):
        try:
            task=eot_queue.get_nowait() # raises Empty when empty
            end_of_transfer(task)
            eot_queue.task_done()
        except Queue.Empty, e:
            break
        except sdexception.FatalException, e:
            raise
        except:
            # debug
            #sdtrace.log_exception(stderr=True)
            raise
#    trend1 = SDTimer.get_elapsed_time( trend0, show_microseconds=True )
#    sdlog.info("JFPDMDEF-110","%s    transfers_end time for %s tasks"%(trend1,nq))
    return

def transfers_begin(transfers):

#    tb0 = SDTimer.get_time()
    # renew certificate if needed
    try:
        sdlogon.renew_certificate(sdconfig.openid,sdconfig.password,force_renew_certificate=False)
    except Exception,e:
        sdlog.error("SDDMDEFA-502","Exception occured while retrieving certificate (%s)"%str(e))
        if sdconfig.config.getboolean('download','continue_on_cert_errors'):
            pass  # Try to keep on going, probably a certificate isn't needed.
        else:
            raise
#    tbrc1 = SDTimer.get_elapsed_time( tb0, show_microseconds=True )
#    sdlog.info("JFPDMDEF-200","%s    transfers_begin call of renew_certificate time"%(tbrc1,))

    # An item in datanode_delays will be datanode:delay, e.g. 'esg-dn1.nsc.liu.se':3.
    # The delay, in seconds, will precede the attempt to connect to the data node.
    # This feature will replace the 1-second 'sleep' which previously separated every call of
    # start_transfer_thread.  The reason given for it was "not to be too agressive with datanodes".
    datanode_delays = {}

#    tbstt0 = SDTimer.get_time()
    for tr in transfers:
        if tr.data_node not in datanode_delays:
            datanode_delays[tr.data_node] = 0
        else:
            datanode_delays[tr.data_node] += 1
        tr.delay = datanode_delays[tr.data_node]
        start_transfer_thread(tr)

#    tbstt1 = SDTimer.get_elapsed_time( tbstt0, show_microseconds=True )
#    sdlog.info("JFPDMDEF-300","%s    time for transfers_begin to do %s calls of start_transfer_thread"%(tbstt1,len(transfers)))

#    tb1 = SDTimer.get_elapsed_time( tb0, show_microseconds=True )
#    sdlog.info("JFPDMDEF-400","%s    transfers_begin time"%(tb1,))

def can_leave():
    return eot_queue.empty()

def fatal_exception():
    return Download.exception_occurs

# module init.

hpss=sdconfig.config.getboolean('download','hpss') # hpss & parse_output hack
eot_queue=Queue.Queue() # eot means "End Of Task"
incorrect_checksum_action=sdconfig.config.get('behaviour','incorrect_checksum_action')
