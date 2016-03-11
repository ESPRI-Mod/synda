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
import traceback
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
import sdlogon
import sdconfig
import sdtime
import sdfiledao
import sdevent
import sdget
from sdworkerutils import WorkerThread
from globusonline.transfer import api_client
from globusonline.transfer.api_client import x509_proxy

def transfers_end():

    _, _, access_token = api_client.goauth.get_access_token(username=globus_username, password=globus_password)
    api = api_client.TransferAPIClient(username=globus_username, goauth=access_token)

    for task_id in globus_tasks:

        code, reason, data = api.task(task_id, fields="status")
        status = data['status']

        sdlog.debug("SDDOWNLO-???", "Checking the status of Globus transfer tasks, id: %s, status: %s" % (task_id, status))
        for item in globus_tasks[task_id]['items']:
            tr = item['tr']
            if status == "SUCCEEDED":
                    tr.status = sdconst.TRANSFER_STATUS_DONE
                    sdlog.info("SDDOWNLO-101", "Transfer done (%s)" % str(tr))
            elif status == "FAILED":
                    tr.status = sdconst.TRANSFER_STATUS_ERROR
                    sdlog.info("SDDOWNLO-101", "Transfer failed (%s)" % str(tr))
            elif status == "INACTIVE":
                # Reactivate both source and destination endpoints
                activate_endpoint(api, globus_tasks[task_id]['src_endpoint'])
                activate_endpoint(api)
            elif status == "ACTIVE":
                pass

            # update file
            sdfiledao.update_file(tr)

            if tr.status == sdconst.TRANSFER_STATUS_DONE:
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
        sdlog.info("SDDOWNLO-???", "src_endpoint: %s, src_path: %s, local_path: %s" % (src_endpoint, src_path, local_path))

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
        sdlog.info("SDDOWNLO-???", "Globus transfer, source endpoint: %s, destination endpoint: %s" % (src_endpoint, dst_endpoint))
        for item in globus_transfers[src_endpoint]['items']:
            t.add_item(item['src_path'], item['dst_path'])
            sdlog.info("SDDOWNLO-???", "Globus transfer item, source path: %s, destination path: %s" % (item['src_path'], item['dst_path']))

        # Submit the transfer

        code, message, data = api.transfer(t)
        if code != 202:
            sdlog.error("SDDOWNLO-???","Error: Cannot add a transfer: (%s, %s)"% (code, message))
            raise FatalException()
        task_id = data['task_id']
        sdlog.info("SDDOWNLO-???", "Submitted Globus task, id: %s" % task_id)
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
    sdlog.debug("SDDOWNLO-???", "Mapped url %s to %s%s" % (url, src_endpoint, src_path))
    return src_endpoint, src_path, path


def activate_endpoint(api, ep=None):
    if ep is None:
        ep = dst_endpoint

    code, reason, reqs = api.endpoint_activation_requirements(ep, type='delegate_proxy')
    public_key = reqs.get_requirement_value("delegate_proxy", "public_key")
    proxy = x509_proxy.create_proxy_from_file(certificate_file, public_key, lifetime_hours=72)
    reqs.set_requirement_value("delegate_proxy", "proxy_chain", proxy)
    try:
        code, reason, result = api.endpoint_activate(ep, reqs)
    except api_client.APIError as e:
        sdlog.error("SDDOWNLO-???","Error: Cannot activate the source endpoint: (%s)"% str(e))
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
                sdlog.debug("SDDOWNLO-???", "Loading endpoints from: %s, last modified: %s" % (self.filepath, modtime))
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
                    sdlog.debug("SDDOWNLO-???", "Using Globus endpoint %s : %s (%s --> %s)"  % (gridftp, name, path_out, path_in))

                # switch the dictionary of endpoints after reading
                self.endpoints = endpoints

    def endpointDict(self):
        self._reload() # reload dictionary from file ?
        return self.endpoints

#
# module init.
#

# Determine a location of an ESGF X.509 credential
certdirprefix=sdconfig.tmp_folder if sdconfig.multiuser else os.environ.get('HOME')
certificate_file='%s/.esg/credentials.pem' % certdirprefix

# sdt/conf/credentails.conf
globus_username = sdconfig.config.get('globus', 'username')
globus_password = sdconfig.config.get('globus', 'password')

# sdt/conf/sdt.conf
dst_endpoint = sdconfig.config.get('globus', 'destination_endpoint')
endpoints_filepath = sdconfig.config.get('globus', 'esgf_endpoints')
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
