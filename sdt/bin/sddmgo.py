#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains download management funcs (Globus implementation).

Note
    sddmgo means 'SynDa Download Manager Globus'
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
import sdglobus


class Download():
    exception_occurs=False

    @classmethod
    def run(cls, transfer):
        tc = transfer.get("tc")
        task_id = transfer.get("task_id")
        src_endpoint = transfer.get("src_endpoint")
        transfer_status = sddglobus.globus_wait(tc, task_id, src_endpoint)
        for item in transfer.get("items"):
            tr = item.get("tr")
            if transfer_status:
                tr.sdget_status = 0
                tr.status = sdconst.TRANSFER_STATUS_DONE
                tr.error_msg = ""
            else:
                tr.status = sdconst.TRANSFER_STATUS_ERROR


def end_of_transfers(task):

    # log
    for item in task.get("items"):
        tr = item.get("tr")
        if tr.status==sdconst.TRANSFER_STATUS_DONE:
            sdlog.info("SDDMGLOB-101","Transfer done (%s)"%str(tr))
        elif tr.status==sdconst.TRANSFER_STATUS_WAITING:
            sdlog.info("SDDMGLOB-108","Transfer marked for retry (error_msg='%s',url=%s,file_id=%d"%(tr.error_msg,tr.url,tr.file_id))
        else:
            sdlog.info("SDDMGLOB-102","Transfer failed (%s)"%str(tr))

        # update file
        sdfiledao.update_file(tr)

        # IMPORTANT: code below must run AFTER the file status has been saved in DB

        if tr.status==sdconst.TRANSFER_STATUS_DONE:
            sdevent.file_complete_event(tr) # trigger 'file complete' event


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
        sdlog.error("SDDMGLOB-502","Exception occured while retrieving certificate (%s)"%str(e))
        raise

    globus_transfers = {}
    """
    globus_transfers = {
        <src_endpoint>: {
            "items": [
                {
                    "src_path": <src_path>,
                    "dst_path": <dst_path>
                    "tr": sdtypes.File
                }...
            ],
            "task_id": <task_id>
        }
    }
    """

    for file_ in transfers:
        src_endpoint, src_path, path = sdglobus.map_to_globus(file_.get("url"))
        if src_endpoint is None:
            sdlog.error("SDDMGLOB-105", "Non-globus file: %s" % str(file_))
            continue
        dst_path = os.path.join(dst_directory, file_.get("local_path"))
        if src_endpoint not in globus_transfers:
            globus_transfers[src_endpoint] = {"task_id": None, "items": []}
        globus_transfers.get(src_endpoint).get("items").append({
                "src_path": src_path,
                "dst_path": dst_path,
                "tr": file_
        })
        sdlog.info("SDDMGLOB-001", "src_endpoint: %s, src_path: %s, dst_path: %s" % (src_endpoint, src_path, dst_path))

    # create a TransferClient object
    authorizer = sddglobus.get_native_app_authorizer(client_id=client_id)
    tc = globus_sdk.TransferClient(authorizer=authorizer)

    for src_endpoint in globus_transfers:

        # activate the ESGF endpoint
        resp = tc.endpoint_autoactivate(src_endpoint, if_expires_in=36000)
        if resp["code"] == "AutoActivationFailed":
            requirements_data = sddglobus.fill_delegate_proxy_activation_requirements(
                    resp.data, sdconfig.esgf_x509_proxy)
            r = tc.endpoint_activate(src_endpoint, requirements_data)
            if r["code"] != "Activated.ClientProxyCredential":
                sdlog.error("SDGLOBUS-028", "Error: Cannot activate the source endpoint: (%s)" % src_endpoint)
                raise FatalException()

        # submit a transfer job
        td = globus_sdk.TransferData(tc, src_endpoint, dst_endpoint)

        for item in globus_transfers.get(src_endpoint).get("items"):
            td.add_item(item.get("src_path"), item.get("dst_path"))

        try:
            task = tc.submit_transfer(td)
            task_id = task.get("task_id")
            print("Submitted Globus transfer: {}".format(task_id))
            globus_transfers.get(src_endpoint)["task_id"] = task_id
            globus_transfers.get(src_endpoint)["src_endpoint"] = src_endpoint
            globus_transfers.get(src_endpoint)["tc"] = tc
        except Exception as e:
            raise Exception("Globus transfer from {} to {} failed due to error: {}".format(
                src_endpoint, dst_endpoint, e))

    for src_endpoint in globus_transfers:
        start_transfer_thread(globus_transfers.get(src_endpoint))

def can_leave():
    return True

def fatal_exception():
    return False

#
# module init.
#

dst_endpoint = sdconfig.config.get("globustransfer", "destination_endpoint")
dst_directory = sdconfig.config.get("globustransfer", "destination_directory")
endpoints_filepath = sdconfig.config.get("globustransfer", "esgf_endpoints")
if endpoints_filepath:
    globus_endpoints = sdglobus.LocalEndpointDict(endpoints_filepath).endpointDict()

incorrect_checksum_action=sdconfig.config.get('behaviour','incorrect_checksum_action')

'''
All Globus active transfer tasks are stored by transfer_begin() in
globus_tasks = {
    <task_id>: {
        'src_endpoint': <src_endpoint>,
        'items': [
            {
                'src_path': <src_path>,
                'dst_path': <dst_path>,
                'tr': <tr>
            },
            ...
        ]
    },
    ...
}
The status of the tasks is checked by transfers_end(). If a Globus task is completed, the task is removed from the list.
'''

eot_queue=Queue.Queue()
