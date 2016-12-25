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
import re
import abc
import urlparse
from datetime import datetime, timedelta
from xml.etree.ElementTree import fromstring
import sdapp
import sdlog
import sdconst
from sdexception import SDException,FatalException
import sdconfig
import sdtime
import sdfiledao
import sdevent
import sdutils
from globusonline.transfer import api_client
from globusonline.transfer.api_client import x509_proxy

def transfers_end():

    _, _, access_token = api_client.goauth.get_access_token(username=globus_username, password=globus_password)
    api = api_client.TransferAPIClient(username=globus_username, goauth=access_token)

    for task_id in globus_tasks:

        code, reason, data = api.task(task_id, fields="status")
        status = data['status']

        sdlog.debug("SDDMGLOB-016", "Checking the status of Globus transfer tasks, id: %s, status: %s" % (task_id, status))
        for item in globus_tasks[task_id]['items']:
            tr = item['tr']
            if status == "SUCCEEDED":

                assert tr.size is not None

                if int(tr.size) != os.path.getsize(tr.get_full_local_path()):
                    sdlog.error("SDDMGLOB-002","size don't match (remote_size=%i,local_size=%i,local_path=%s)"%(int(tr.size),os.path.getsize(tr.get_full_local_path()),tr.get_full_local_path()))

                # retrieve local and remote checksum
                checksum_type=tr.checksum_type if tr.checksum_type is not None else sdconst.CHECKSUM_TYPE_MD5
                local_checksum=sdutils.compute_checksum(tr.get_full_local_path(),checksum_type)
                remote_checksum=tr.checksum # retrieve remote checksum

                if remote_checksum!=None:
                    # remote checksum exists

                    # compare local and remote checksum
                    if remote_checksum==local_checksum:
                        # checksum is ok

                        tr.status = sdconst.TRANSFER_STATUS_DONE
                    else:
                        # checksum is not ok

                        if incorrect_checksum_action=="remove":
                            tr.status=sdconst.TRANSFER_STATUS_ERROR
                            tr.error_msg="File corruption detected: local checksum doesn't match remote checksum"

                            # remove file from local repository
                            sdlog.error("SDDMGLOB-155","checksum don't match: remove local file (local_checksum=%s,remote_checksum=%s,local_path=%s)"%(local_checksum,remote_checksum,tr.get_full_local_path()))
                            try:
                                os.remove(tr.get_full_local_path())
                            except Exception,e:
                                sdlog.error("SDDMGLOB-158","error occurs while removing local file (%s)"%tr.get_full_local_path())

                        elif incorrect_checksum_action=="keep":
                            sdlog.info("SDDMGLOB-157","local checksum doesn't match remote checksum (%s)"%tr.get_full_local_path())
                            
                            tr.status=sdconst.TRANSFER_STATUS_DONE

                        else:
                            raise FatalException("SDDMGLOB-507","incorrect value (%s)"%incorrect_checksum_action)
                else:
                    # remote checksum is missing
                    # NOTE: we DON'T store the local checksum ('file' table contains only the REMOTE checksum)

                    tr.status = sdconst.TRANSFER_STATUS_DONE

                if tr.status == sdconst.TRANSFER_STATUS_DONE:
                    tr.end_date=sdtime.now() # WARNING: this is not the real end of transfer date but the date when we ask the globus scheduler if the transfer is done.
                    tr.error_msg=""
                    sdlog.info("SDDMGLOB-101", "Transfer done (%s)" % str(tr))

            elif status == "FAILED":
                tr.status = sdconst.TRANSFER_STATUS_ERROR
                tr.error_msg = "Error occurs during download."

                sdlog.info("SDDMGLOB-101", "Transfer failed (%s)" % str(tr))

                # Remove local file if exists
                if os.path.isfile(tr.get_full_local_path()):
                    try:
                        os.remove(tr.get_full_local_path())
                    except Exception,e:
                        sdlog.error("SDDMGLOB-528","Error occurs during file suppression (%s,%s)"%(tr.get_full_local_path(),str(e)))

            elif status == "INACTIVE":
                # Reactivate both source and destination endpoints
                activate_endpoint(api, globus_tasks[task_id]['src_endpoint'])
                activate_endpoint(api)
            elif status == "ACTIVE":
                pass


            # update file
            sdfiledao.update_file(tr)


            if tr.status == sdconst.TRANSFER_STATUS_DONE:

                # TODO: maybe add a try/except and do some rollback here in
                # case fatal exception occurs in 'file_complete_event' (else,
                # we have a file marked as 'done' with the corresponding event
                # un-triggered)

                # NOTE: code below must run AFTER the file status has been
                # saved in DB (because it makes DB queries which expect the
                # file status to exist)

                sdevent.file_complete_event(tr) # trigger 'file complete' event


        # Remove the tasks from the lists of active tasks
        if status == "SUCCEEDED" or status == "FAILED":
            globus_tasks.pop(task_id, None)

def transfers_begin(transfers):

    # Activate the destination endpoint

    _, _, access_token = api_client.goauth.get_access_token(username=globus_username, password=globus_password)
    api = api_client.TransferAPIClient(username=globus_username, goauth=access_token)
    activate_endpoint(api)

    # Divide all files that are to be transferred into groups based on the source globus endpoint

    globus_transfers = {}

    for tr in transfers:
        src_endpoint, src_path, path = map_to_globus(tr.url)
        local_path = tr.get_full_local_path()
        if not src_endpoint in globus_transfers:
            globus_transfers[src_endpoint] = {
                    'src_endpoint': src_endpoint,
                    'items': []
            }
        globus_transfers[src_endpoint]['items'].append({
                'src_path': src_path,
                'dst_path': local_path,
                'tr': tr
        })
        sdlog.info("SDDMGLOB-001", "src_endpoint: %s, src_path: %s, local_path: %s" % (src_endpoint, src_path, local_path))

    # Submit transfers

    for src_endpoint in globus_transfers:

        # Activate the source endpoint
        activate_endpoint(api, src_endpoint)

        # Create a transfer and add files to the transfer

        code, message, data = api.transfer_submission_id()
        if code != 200:
            raise FatalException()
        submission_id = data['value']
        t = api_client.Transfer(submission_id, src_endpoint, dst_endpoint)
        sdlog.info("SDDMGLOB-004", "Globus transfer, source endpoint: %s, destination endpoint: %s" % (src_endpoint, dst_endpoint))
        for item in globus_transfers[src_endpoint]['items']:
            t.add_item(item['src_path'], item['dst_path'])
            sdlog.info("SDDMGLOB-005", "Globus transfer item, source path: %s, destination path: %s" % (item['src_path'], item['dst_path']))

        # Submit the transfer

        code, message, data = api.transfer(t)
        if code != 202:
            sdlog.error("SDDMGLOB-006","Error: Cannot add a transfer: (%s, %s)"% (code, message))
            raise FatalException()
        task_id = data['task_id']
        sdlog.info("SDDMGLOB-007", "Submitted Globus task, id: %s" % task_id)
        globus_tasks[task_id] = globus_transfers[src_endpoint]


def map_to_globus(url):
    parsed_url = urlparse.urlparse(url)
    hostname = parsed_url.netloc
    src_endpoint = None
    src_path = re.sub('/+', '/', parsed_url.path)
    path = src_path
    if hostname in globus_endpoints:
        src_endpoint = globus_endpoints[hostname].name
        path_out = globus_endpoints[hostname].path_out
        path_in = globus_endpoints[hostname].path_in
        if path_out:
            src_path.replace(path_out, '', 1)
        if path_in:
            src_path = path_out + src_path
    sdlog.debug("SDDMGLOB-024", "Mapped url %s to %s%s" % (url, src_endpoint, src_path))
    return src_endpoint, src_path, path


def activate_endpoint(api, ep=None):
    if ep is None:
        ep = dst_endpoint

    code, reason, reqs = api.endpoint_activation_requirements(ep, type='delegate_proxy')
    public_key = reqs.get_requirement_value("delegate_proxy", "public_key")
    proxy = x509_proxy.create_proxy_from_file(sdconfig.esgf_x509_proxy, public_key, lifetime_hours=72)
    reqs.set_requirement_value("delegate_proxy", "proxy_chain", proxy)
    try:
        code, reason, result = api.endpoint_activate(ep, reqs)
    except api_client.APIError as e:
        sdlog.error("SDDMGLOB-028","Error: Cannot activate the source endpoint: (%s)"% str(e))
        raise FatalException()


def can_leave():
    return True

def fatal_exception():
    return False


NS = "http://www.esgf.org/whitelist"


def file_modification_datetime(filepath):
    t = os.path.getmtime(filepath)
    return datetime.fromtimestamp(t)


class Endpoint(object):
    '''Utility class that stores the fields for processing a Globus endpoint.'''

    def __init__(self, name, path_out=None, path_in=None):
        self.name = name
        self.path_out = path_out
        self.path_in = path_in


class EndpointDict(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def endpointDict(self):
        '''Returns a dictionary of (GridFTP hostname:port, Globus Endpoint object) pairs.''' 
        pass


class LocalEndpointDict(EndpointDict):
    '''Implementation of EndpointDict based on a local XML configuration file.'''

    def __init__(self, filepath):
        self.filepath = None
        self.endpoints = {}
        self.init = False

        try:
            if os.path.exists(filepath):
                self.filepath = filepath
                self.modtime = file_modification_datetime(self.filepath)
                self._reload(force=True)
                self.init = True

        except IOError:
            pass

    def _reload(self, force=False):
        '''Internal method to reload the dictionary of endpoints if the file has changed since it was last read'''

        if self.filepath: # only if endpoints file exists
            modtime = file_modification_datetime(self.filepath)
            if force or modtime > self.modtime:
                sdlog.debug("SDDMGLOB-014", "Loading endpoints from: %s, last modified: %s" % (self.filepath, modtime))
                self.modtime = modtime
                endpoints = {}

                # read XML file
                with open (self.filepath, "r") as myfile:
                    xml=myfile.read().replace('\n', '')

                # <endpoints xmlns="http://www.esgf.org/whitelist">
                root = fromstring(xml)
                # <endpoint name="esg#jpl" gridftp="esg-datanode.jpl.nasa.gov:2811" />
                for endpoint in root.findall("{%s}endpoint" % NS):
                    gridftp = endpoint.attrib['gridftp']
                    name = endpoint.attrib['name']                   # mandatory attribute
                    path_out = endpoint.attrib.get('path_out', None) # optional attribute
                    path_in = endpoint.attrib.get('path_in', None)   # optional attribute
                    endpoints[ gridftp ] = Endpoint(name, path_out=path_out, path_in=path_in)
                    sdlog.debug("SDDMGLOB-018", "Using Globus endpoint %s : %s (%s --> %s)"  % (gridftp, name, path_out, path_in))

                # switch the dictionary of endpoints after reading
                self.endpoints = endpoints

    def endpointDict(self):
        self._reload() # reload dictionary from file ?
        return self.endpoints

#
# module init.
#

# sdt/conf/credentails.conf
globus_username = sdconfig.config.get('globustransfer', 'username')
globus_password = sdconfig.config.get('globustransfer', 'password')

# sdt/conf/sdt.conf
dst_endpoint = sdconfig.config.get('globustransfer', 'destination_endpoint')
endpoints_filepath = sdconfig.config.get('globustransfer', 'esgf_endpoints')
if endpoints_filepath:
    globus_endpoints = LocalEndpointDict(endpoints_filepath).endpointDict()

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

globus_tasks = {}
