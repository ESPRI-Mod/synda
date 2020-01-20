#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains security related functions."""

import os
import sys
import re
import struct
import abc
import json
import threading
import datetime
from xml.etree.ElementTree import fromstring
import six
from six import with_metaclass
from six.moves.urllib.parse import urlparse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
import globus_sdk

import sdlog
import sdconst
import sdconfig
from sdtools import print_stderr
from sdexception import FatalException


client_id = "83ec00c1-e67a-4356-9f1f-f7e31177e31a"


def file_modification_datetime(filepath):
    t = os.path.getmtime(filepath)
    return datetime.datetime.fromtimestamp(t)


class Endpoint(object):
    """Utility class that stores the fields for processing a Globus endpoint."""

    def __init__(self, name, path_out=None, path_in=None):
        self.name = name
        self.path_out = path_out
        self.path_in = path_in


class EndpointDict(with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    def endpointDict(self):
        """Returns a dictionary of (GridFTP hostname:port, Globus Endpoint object) pairs."""
        pass


class LocalEndpointDict(EndpointDict):
    """Implementation of EndpointDict based on a local XML configuration file."""

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
        """Internal method to reload the dictionary of endpoints if the file has changed since it was last read"""

        if self.filepath:
            modtime = file_modification_datetime(self.filepath)
            if force or modtime > self.modtime:
                sdlog.debug("SDDMGLOB-014", "Loading endpoints from: %s, last modified: %s" % (self.filepath, modtime))
                self.modtime = modtime
                endpoints = {}

                # read XML file
                with open(self.filepath, "r") as myfile:
                    xml = myfile.read().replace("\n", "")

                # <endpoints xmlns="http://www.esgf.org/whitelist">
                root = fromstring(xml)
                # <endpoint name="esg#jpl" gridftp="esg-datanode.jpl.nasa.gov:2811" />
                for endpoint in root.findall("{%s}endpoint" % "http://www.esgf.org/whitelist"):
                    gridftp = endpoint.attrib["gridftp"]
                    name = endpoint.attrib["name"]
                    path_out = endpoint.attrib.get("path_out", None)
                    path_in = endpoint.attrib.get("path_in", None)
                    endpoints[gridftp] = Endpoint(name, path_out=path_out, path_in=path_in)
                    sdlog.debug("SDDMGLOB-018", "Using Globus endpoint %s : %s (%s --> %s)" % (gridftp, name, path_out, path_in))

                # switch the dictionary of endpoints after reading
                self.endpoints = endpoints

    def endpointDict(self):
        self._reload()
        return self.endpoints


dst_endpoint = sdconfig.config.get("globustransfer", "destination_endpoint")
dst_directory = sdconfig.config.get("globustransfer", "destination_directory")
endpoints_filepath = sdconfig.config.get("globustransfer", "esgf_endpoints")
if endpoints_filepath:
    globus_endpoints = LocalEndpointDict(endpoints_filepath).endpointDict()


def load_tokens_from_file(filepath):
    """Load a set of saved tokens."""
    with open(filepath, 'r') as f:
        tokens = json.load(f)
    return tokens


def save_tokens_to_file(filepath, tokens):
    """Save a set of tokens for later use."""
    directory = os.path.dirname(filepath)
    if not os.path.isdir(directory):
        try:
            os.makedirs(directory)
        except OSError as e:
            print_stderr("Could not create {} directory for a Globus OAuth2 token.\n{}".format(directory, e))
            sys.exit(1)
    with open(filepath, 'w') as f:
        json.dump(tokens, f)


def update_tokens_file_on_refresh(token_response):
    """
    Callback function passed into the RefreshTokenAuthorizer.
    Will be invoked any time a new access token is fetched.
    """
    save_tokens_to_file(sdconfig.globus_tokens, token_response.by_resource_server)


def get_native_app_authorizer(client_id):
    transfer_tokens = None
    try:
        tokens = load_tokens_from_file(sdconfig.globus_tokens)
        transfer_tokens = tokens["transfer.api.globus.org"]
    except:
        print_stderr("Globus tokens not found (use 'renew' command to retrieve new tokens).")
        sys.exit(1)

    auth_client = globus_sdk.NativeAppAuthClient(client_id=client_id)

    return globus_sdk.RefreshTokenAuthorizer(
            transfer_tokens["refresh_token"],
            auth_client,
            access_token=transfer_tokens["access_token"],
            expires_at=transfer_tokens["expires_at_seconds"],
            on_refresh=update_tokens_file_on_refresh)


def fill_delegate_proxy_activation_requirements(requirements_data, cred_file, lifetime_hours=12):
    """
    Given the activation requirements for an endpoint and a filename for
    X.509 credentials, extracts the public key from the activation
    requirements, uses the key and the credentials to make a proxy credential,
    and returns the requirements data with the proxy chain filled in.
    """
    # get the public key from the activation requirements
    for data in requirements_data["DATA"]:
        if data["type"] == "delegate_proxy" and data["name"] == "public_key":
            public_key = data["value"]
            break
    else:
        raise ValueError(
            (
                "No public_key found in activation requirements, this endpoint "
                "does not support Delegate Proxy activation."
            )
        )

    # get user credentials from user credential file"
    with open(cred_file) as f:
        issuer_cred = f.read()
    # create the proxy credentials
    proxy = create_proxy_credentials(issuer_cred, public_key, lifetime_hours)
    # return the activation requirements document with the proxy_chain filled
    for data in requirements_data["DATA"]:
        if data["type"] == "delegate_proxy" and data["name"] == "proxy_chain":
            data["value"] = proxy
            return requirements_data
    else:
        raise ValueError(
            (
                "No proxy_chain found in activation requirements, this endpoint "
                "does not support Delegate Proxy activation."
            )
        )


def create_proxy_credentials(issuer_cred, public_key, lifetime_hours):
    """
    Given an issuer credentials PEM file in the form of a string, a public_key
    string from an activation requirements document, and an int for the
    proxy lifetime, returns credentials as a unicode string in PEM format
    containing a new proxy certificate and an extended proxy chain.
    """
    # parse the issuer credential
    loaded_cert, loaded_private_key, issuer_chain = parse_issuer_cred(issuer_cred)

    # load the public_key into a cryptography object
    loaded_public_key = serialization.load_pem_public_key(
        public_key.encode("ascii"), backend=default_backend()
    )

    # check that the issuer certificate is not an old proxy
    # and is using the keyUsage section as required
    confirm_not_old_proxy(loaded_cert)
    validate_key_usage(loaded_cert)

    # create the proxy cert cryptography object
    new_cert = create_proxy_cert(
        loaded_cert, loaded_private_key, loaded_public_key, lifetime_hours
    )

    # extend the proxy chain as a unicode string
    extended_chain = loaded_cert.public_bytes(serialization.Encoding.PEM).decode(
        "ascii"
    ) + six.u(issuer_chain)

    # return in PEM format as a unicode string
    return (
        new_cert.public_bytes(serialization.Encoding.PEM).decode("ascii")
        + extended_chain
    )


def parse_issuer_cred(issuer_cred):
    """
    Given an X509 PEM file in the form of a string, parses it into sections
    by the PEM delimiters of: -----BEGIN <label>----- and -----END <label>----
    Confirms the sections can be decoded in the proxy credential order of:
    issuer cert, issuer private key, proxy chain of 0 or more certs .
    Returns the issuer cert and private key as loaded cryptography objects
    and the proxy chain as a potentially empty string.
    """
    # get each section of the PEM file
    sections = re.findall(
        "-----BEGIN.*?-----.*?-----END.*?-----", issuer_cred, flags=re.DOTALL
    )
    try:
        issuer_cert = sections[0]
        issuer_private_key = sections[1]
        issuer_chain_certs = sections[2:]
    except IndexError:
        raise ValueError(
            "Unable to parse PEM data in credentials, "
            "make sure the X.509 file is in PEM format and "
            "consists of the issuer cert, issuer private key, "
            "and proxy chain (if any) in that order."
        )

    # then validate that each section of data can be decoded as expected
    try:
        loaded_cert = x509.load_pem_x509_certificate(
            six.b(issuer_cert), default_backend()
        )
        loaded_private_key = serialization.load_pem_private_key(
            six.b(issuer_private_key), password=None, backend=default_backend()
        )
        for chain_cert in issuer_chain_certs:
            x509.load_pem_x509_certificate(six.b(chain_cert), default_backend())
        issuer_chain = "".join(issuer_chain_certs)
    except ValueError:
        raise ValueError(
            "Failed to decode PEM data in credentials. Make sure "
            "the X.509 file consists of the issuer cert, "
            "issuer private key, and proxy chain (if any) "
            "in that order."
        )

    # return loaded cryptography objects and the issuer chain
    return loaded_cert, loaded_private_key, issuer_chain


def create_proxy_cert(loaded_cert, loaded_private_key, loaded_public_key, lifetime_hours):
    """
    Given cryptography objects for an issuing certificate, a public_key,
    a private_key, and an int for lifetime in hours, creates a proxy
    cert from the issuer and public key signed by the private key.
    """
    builder = x509.CertificateBuilder()

    # create a serial number for the new proxy
    # Under RFC 3820 there are many ways to generate the serial number. However
    # making the number unpredictable has security benefits, e.g. it can make
    # this style of attack more difficult:
    # http://www.win.tue.nl/hashclash/rogue-ca
    serial = struct.unpack("<Q", os.urandom(8))[0]
    builder = builder.serial_number(serial)

    # set the new proxy as valid from now until lifetime_hours have passed
    builder = builder.not_valid_before(datetime.datetime.utcnow())
    builder = builder.not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(hours=lifetime_hours)
    )

    # set the public key of the new proxy to the given public key
    builder = builder.public_key(loaded_public_key)

    # set the issuer of the new cert to the subject of the issuing cert
    builder = builder.issuer_name(loaded_cert.subject)

    # set the new proxy's subject
    # append a CommonName to the new proxy's subject
    # with the serial as the value of the CN
    new_atribute = x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, six.u(str(serial)))
    subject_attributes = list(loaded_cert.subject)
    subject_attributes.append(new_atribute)
    builder = builder.subject_name(x509.Name(subject_attributes))

    # add proxyCertInfo extension to the new proxy (We opt not to add keyUsage)
    # For RFC proxies the effective usage is defined as the intersection
    # of the usage of each cert in the chain. See section 4.2 of RFC 3820.

    # the constants 'oid' and 'value' are gotten from
    # examining output from a call to the open ssl function:
    # X509V3_EXT_conf(NULL, ctx, name, value)
    # ctx set by X509V3_set_nconf(&ctx, NCONF_new(NULL))
    # name = "proxyCertInfo"
    # value = "critical,language:Inherit all"
    oid = x509.ObjectIdentifier("1.3.6.1.5.5.7.1.14")
    value = b"0\x0c0\n\x06\x08+\x06\x01\x05\x05\x07\x15\x01"
    extension = x509.extensions.UnrecognizedExtension(oid, value)
    builder = builder.add_extension(extension, critical=True)

    # sign the new proxy with the issuer's private key
    new_certificate = builder.sign(
        private_key=loaded_private_key,
        algorithm=hashes.SHA256(),
        backend=default_backend(),
    )

    # return the new proxy as a cryptography object
    return new_certificate


def confirm_not_old_proxy(loaded_cert):
    """
    Given a cryptography object for the issuer cert, checks if the cert is
    an "old proxy" and raise an error if so.
    """
    # Examine the last CommonName to see if it looks like an old proxy.
    last_cn = loaded_cert.subject.get_attributes_for_oid(x509.oid.NameOID.COMMON_NAME)[
        -1
    ]
    # if the last CN is 'proxy' or 'limited proxy' we are in an old proxy
    if last_cn.value in ("proxy", "limited proxy"):
        raise ValueError(
            "Proxy certificate is in an outdated format that is no longer supported"
        )


def validate_key_usage(loaded_cert):
    """
    Given a cryptography object for the issuer cert, checks that if
    the keyUsage extension is being used that the digital signature
    bit has been asserted. (As specified in RFC 3820 section 3.1.)
    """
    try:
        key_usage = loaded_cert.extensions.get_extension_for_oid(
            x509.oid.ExtensionOID.KEY_USAGE
        )
        if not key_usage.value.digital_signature:
            raise ValueError(
                "Certificate is using the keyUsage extension, but has "
                "not asserted the Digital Signature bit."
            )
    except x509.ExtensionNotFound:  # keyUsage extension not used
        return


def map_to_globus(url):
    parsed_url = urlparse(url)

    # 'globus' scheme
    if parsed_url.scheme == "globus":
        slash_index = parsed_url.path.find("/")
        src_endpoint = parsed_url.path[0:slash_index]
        src_path = parsed_url.path[slash_index:]
        return src_endpoint, src_path, src_path

    # 'gridftp' scheme
    hostname = parsed_url.netloc
    src_endpoint = None
    src_path = re.sub("/+", "/", parsed_url.path)
    path = src_path
    if hostname in globus_endpoints:
        src_endpoint = globus_endpoints[hostname].name
        path_out = globus_endpoints[hostname].path_out
        path_in = globus_endpoints[hostname].path_in
        if path_out:
            src_path.replace(path_out, "", 1)
        if path_in:
            src_path = path_out + src_path
    sdlog.debug("SDDMGLOB-024", "Mapped url %s to %s%s" % (url, src_endpoint, src_path))
    return src_endpoint, src_path, path


def globus_wait(tc, task_id, src_endpoint):
    """
    A Globus transfer job (task) can be in one of the three states: ACTIVE, SUCCEEDED, FAILED.
    Parsl every 15 seconds polls a status of the transfer job (task) from the Globus Transfer service,
    with 60 second timeout limit. If the task is ACTIVE after time runs out 'task_wait' returns False,
    and True otherwise.
    """
    last_event_time = None
    while not tc.task_wait(task_id, 60, 15):
        task = tc.get_task(task_id)
        # Get the last error Globus event
        events = tc.task_event_list(task_id, num_results=1, filter="is_error:1")
        try:
            event = next(events)
        except StopIteration:
            continue
        # Print the error event to stderr and Parsl file log if it was not yet printed
        if event["time"] != last_event_time:
            last_event_time = event["time"]
            print_stderr("Non-critical Globus Transfer error event for transfer from {}: {} at {}".format(
                src_endpoint, event["description"], event["time"]))
            print_stderr("Globus Transfer error details: {}".format(event["details"]))

    """
    The Globus transfer job (task) has been terminated (is not ACTIVE). Check if the transfer
    SUCCEEDED or FAILED.
    """
    task = tc.get_task(task_id)
    if task["status"] == "SUCCEEDED":
        print_stderr("Globus transfer {} from {} succeeded".format(
            task_id, src_endpoint))
    else:
        print_stderr("Globus Transfer task: {}".format(task_id))
        events = tc.task_event_list(task_id, num_results=1, filter="is_error:1")
        event = next(events)
        print_stderr("Globus transfer {} from {} failed due to error: {}".format(
            task_id, src_endpoint, event["details"]))


def direct(
        files,
        force=False,
        local_path_prefix=sdconfig.sandbox_folder,
        verify_checksum=False,
        network_bandwidth_test=False,
        debug=True,
        verbosity=0):
    """
    Returns:
        a list of files that cannot be transferred by Globus because
        they haven't been published with globus: or gsiftp: access.
        After all Globus transfer jobs are complete, Synda will download
        the files using the HTTP protocol.
    """

    globus_transfers = {}
    """
    globus_transfers = {
        <src_endpoint>: {
            "items": [
                {
                    "src_path": <src_path>,
                    "dst_path": <dst_path>
                }...
            ],
            "task_id": <task_id>
        }
    }
    """
    non_globus_files = []

    for file_ in files:
        if file_.get("attached_parameters").get("protocol") != sdconst.TRANSFER_PROTOCOL_GLOBUS:
            non_globus_files.append(file_)
            continue
        src_endpoint, src_path, path = map_to_globus(file_.get("url"))
        if src_endpoint is None:
            non_globus_files.append(file_)
            continue
        dst_path = os.path.join(dst_directory, file_.get("dataset_path"), file_.get("filename"))
        if src_endpoint not in globus_transfers:
            globus_transfers[src_endpoint] = {"task_id": None, "items": []}
        globus_transfers.get(src_endpoint).get("items").append({
                "src_path": src_path,
                "dst_path": dst_path
        })
        sdlog.info("SDDMGLOB-001", "src_endpoint: %s, src_path: %s, dst_path: %s" % (src_endpoint, src_path, dst_path))

    # create a TransferClient object
    authorizer = get_native_app_authorizer(client_id=client_id)
    tc = globus_sdk.TransferClient(authorizer=authorizer)

    for src_endpoint in globus_transfers:

        # activate the ESGF endpoint
        resp = tc.endpoint_autoactivate(src_endpoint, if_expires_in=36000)
        if resp["code"] == "AutoActivationFailed":
            requirements_data = fill_delegate_proxy_activation_requirements(
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
        except Exception as e:
            raise Exception("Globus transfer from {} to {} failed due to error: {}".format(
                src_endpoint, dst_endpoint, e))

    # monitor the transfer jobs
    threads = []
    for src_endpoint in globus_transfers:
        task_id = globus_transfers.get(src_endpoint).get("task_id")
        thread = threading.Thread(target=globus_wait, args=(tc, task_id, src_endpoint,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return non_globus_files
