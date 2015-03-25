#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synchro-data
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @svn_file       $Id: sddownload.py 12605 2014-03-18 07:31:36Z jerome $
#  @version        $Rev: 12638 $
#  @lastrevision   $Date: 2014-03-18 08:36:15 +0100 (Tue, 18 Mar 2014) $
#  @license        CeCILL (http://dods.ipsl.jussieu.fr/jripsl/synchro_data/LICENSE)
##################################

"""This script contains download high level functions (low level ones are in 'sdget' script)."""

import os
import sdapp
import sdlog
import sdconst
import sdutils
from sdexception import SDException,FatalException
import sdlogon
import sdconfig
import sdtime
import sdfiledao
import sdevent

class Download():
    exception_occurs=False # this flag is used to stop the event loop if exception occurs in thread

    @classmethod
    def run(cls,tr):
        if lfae_mode=="keep":
            # usefull mode if
            #  - metadata needs to be regenerated without retransfering the data
            #  - synda files are mixed with files from other sources

            if os.path.isfile(tr.get_full_local_path()):
                # file already here, just do some check and update some metadata 

                assert tr.size==os.path.getsize(tr.get_full_local_path())

                tr.status=sdconst.TRANSFER_STATUS_DONE
                tr.error_msg="Local file already exists: keep it (lfae_mode=keep)"

                sdlog.info("SDDOWNLO-197","Local file already exists: keep it (lfae_mode=keep,local_file=%s)"%tr.get_full_local_path())
            else:
                # file not here, start the download

                cls.start_transfer_script(tr)
        elif lfae_mode=="replace":
            if os.path.isfile(tr.get_full_local_path()):
                sdlog.info("SDDOWNLO-187","Local file already exists: remove it (lfae_mode=replace,local_file=%s)"%tr.get_full_local_path())
                os.remove(tr.get_full_local_path())

            cls.start_transfer_script(tr)
        elif lfae_mode=="abort":
            if os.path.isfile(tr.get_full_local_path()):
                tr.status=sdconst.TRANSFER_STATUS_ERROR
                tr.error_msg="Local file already exists: transfer aborted (lfae_mode=abort)"
            else:
                cls.start_transfer_script(tr)

        tr.end_date=sdtime.now()

    @classmethod
    def start_transfer_script(cls,tr):

        # renew certificate if needed
        try:
            sdlogon.renew_certificate(False)
        except:
            sdlog.error("SDDOWNLO-504","Certificate error: the daemon must be stopped")
            raise

        # start wget in a new process
        # (wget fork is blocking here, so thread will wait until wget is done)
        #
        # Notes
        #  - if success (status==0), stdout contains only checksum
        #
        (sdget_status,stdout,stderr)=sdutils.get_status_output(tr.get_download_command_line(),shell=True)
        tr.sdget_status=sdget_status
        if sdget_status==0:
            local_checksum=stdout.rstrip(os.linesep) # BEWARE: unexpected "get_data.sh" errors may be hidden here (print "stdout" in logfile to debug)

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
            # we don't remove file in this case (this is already done in 'sdget.sh' script)

            if sdget_status==7:
                tr.status=sdconst.TRANSFER_STATUS_WAITING
                tr.error_msg="'sdget.sh' script gets killed"

            elif sdget_status==29:
                tr.status=sdconst.TRANSFER_STATUS_WAITING
                tr.error_msg="'wget' gets killed"

            else:
                sdlog.debug("SDDOWNLO-855","%s"%stderr) # if error occurs in 'sdget.sh', stderr contains error message

                tr.status=sdconst.TRANSFER_STATUS_ERROR
                tr.error_msg="Error occurs in 'sdget.sh' script"

def end_of_transfer(tr):
    # log
    if tr.status==sdconst.TRANSFER_STATUS_DONE:
        sdlog.info("SYNDTASK-101","Transfer done (%s)"%str(tr))
    elif tr.status==sdconst.TRANSFER_STATUS_WAITING:
        # Transfer have been marked for retry
        # (this happens for example during shutdown immediate, where
        # all running transfers are killed, or when wget are 'stalled'
        # and killed by watchdog)
        
        sdlog.info("SYNDTASK-108","%s"%(tr.error_msg,))
        #sdlog.info("SYNDTASK-104","Transfer marked for retry (%s)"%str(tr))
    else:
        sdlog.info("SYNDTASK-102","Transfer failed (%s)"%str(tr))

    # update file
    sdfiledao.update_file(tr)

    # IMPORTANT: code below must run AFTER the file status has been saved in DB

    if tr.status==sdconst.TRANSFER_STATUS_DONE:
        sdevent.file_complete_event(tr) # trigger 'file complete' event

    # TODO: maybe do some rollback here in case fatal exception occurs in 'file_complete_event'
    #       (else, we have a file marked as 'done' with the corresponding event un-triggered)

    # check for fatal error
    if tr.sdget_status==4:
        sdlog.info("SYNDTASK-147","Stopping daemon as get_data.sh script returns fatal error.")
        raise FatalException()

# module init.

incorrect_checksum_action=sdconfig.incorrect_checksum_action
lfae_mode=sdconfig.config.get('behaviour','lfae_mode')
