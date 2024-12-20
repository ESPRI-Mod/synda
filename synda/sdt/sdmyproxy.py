#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module retrieves a X509 certificate from ESGF 'Myproxy' server.

Notes
    - Myproxy library used in this script is 'myproxyclient' from NDG stack
    - informations about myproxyclient are available here
        - http://ndg-security.ceda.ac.uk/wiki/MyProxyClient)
        - https://pythonhosted.org/MyProxyClient/myproxy.client.MyProxyClient-class.html
"""

import os
import shutil
import argparse
from synda.sdt import sdlog
from synda.sdt import sdutils

from myproxy.client import MyProxyClient
from OpenSSL import SSL
MyProxyClient.SSL_METHOD = SSL.TLSv1_2_METHOD

from synda.sdt import sdexception

from synda.source.config.path.tree.certificate.x509.models import Config as SecurityPath
from synda.source.config.file.certificate.x509.models import Config as SecurityFile
from synda.source.config.path.tree.models import Config as TreePath

esgf_x509_proxy = SecurityFile().get_credentials()
esgf_x509_cert_dir = SecurityPath().get_certificates()

conf_folder = TreePath().get("conf")


def get_passwd_from_passwd_file():
    passwd = None
    passwd_filename = ".sdpass"
    passwd_file = os.path.join(conf_folder, passwd_filename)

    if os.path.isfile(passwd_file):
        with open(passwd_file, 'r') as fh:
            buf = fh.read().rstrip(os.linesep)
            if len(buf) > 0:
                passwd = buf

    return passwd


def run(
        host,
        port,
        username,
        force_renew_certificate=False,
        force_renew_ca_certificates=False,
        password=None,
):

    # use passwd from passwd file if exists
    passwd = get_passwd_from_passwd_file()
    if passwd is not None:
        password = passwd

    # check password
    if password == "pwd":
        sdlog.error("SDMYPROX-019", "ESGF password not set")
        raise sdexception.PasswordNotSetException()

    # check username
    if username is None:
        sdlog.error("SDMYPROX-020", "ESGF username not set")
        raise sdexception.UsernameNotSetException()

    if force_renew_certificate:
        if os.path.isfile(esgf_x509_proxy):
            os.unlink(esgf_x509_proxy)

    if force_renew_ca_certificates:
        if os.path.isdir(esgf_x509_cert_dir):
            shutil.rmtree(esgf_x509_cert_dir)

    if certificate_exists():
        if certificate_is_valid():
            # sdlog.error("SDMYPROX-006","Certificate is valid, nothing to do")
            pass
        else:
            renew_certificate(host, port, username, password)
    else:
        renew_certificate(host, port, username, password)

    # check (second pass => if it fails again, then fatal error)
    if not certificate_exists():
        sdlog.error("SDMYPROX-009", "Error occured while retrieving certificate")
        raise sdexception.MissingCertificateException()


def certificate_exists():

    if os.path.isfile(esgf_x509_proxy):
        return True
    else:
        return False


def certificate_is_valid():
    """Checks whether the cert expires in the next 500 seconds."""

    li = ['/usr/bin/openssl', 'x509', '-checkend', '500', '-noout', '-in', esgf_x509_proxy]

    status, stdout, stderr = sdutils.get_status_output(li, shell=False)

    if status == 0:
        return True
    else:
        return False


def renew_certificate(host, port, username, password):

    sdlog.info("SDMYPROX-002", "Renew certificate..")

    # we need a mkdir here to prevent 'No such file or directory' myproxyclient error (see TAGFERE5435 for more info)
    sd = SecurityPath().get_security()
    if not os.path.isdir(sd):
        os.makedirs(sd)

    # currently, we set bootstrap option everytime
    #
    # TODO: change this to set only the first time (i.e. if .esg/certificates is empty)
    #
    bootstrap = True

    # currently, we set trustroots option everytime
    updateTrustRoots = True
    authnGetTrustRootsCall = False

    # TODO: maybe add option in 'synda certificate' to use specify another path for cadir (for debugging purpose)
    # ROOT_TRUSTROOT_DIR = '/etc/grid-security/certificates'

    # set env.

    os.environ['ESGF_CREDENTIAL'] = esgf_x509_proxy
    os.environ['ESGF_CERT_DIR'] = esgf_x509_cert_dir
    os.environ['X509_CERT_DIR'] = esgf_x509_cert_dir

    if 'X509_USER_PROXY' in os.environ: 
        del os.environ['X509_USER_PROXY']

    # if 'GLOBUS_LOCATION' in os.environ:
    #    del os.environ['GLOBUS_LOCATION']

    # main

    myproxy_clnt = MyProxyClient(
        hostname=host,
        port=port,
        caCertDir=esgf_x509_cert_dir,
        # 12 hours
        proxyCertLifetime=43200,
    )

    # credname=credname
    creds = myproxy_clnt.logon(
        username,
        password,
        bootstrap=bootstrap,
        updateTrustRoots=updateTrustRoots,
        authnGetTrustRootsCall=authnGetTrustRootsCall,
    )

    # store cert on disk

    fout = open(esgf_x509_proxy, 'wb')
    for cred in creds:
        fout.write(cred)
    fout.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--host', '-h', default='pcmdi9.llnl.gov')
    parser.add_argument('--port', '-p', type=int, default=7512)
    parser.add_argument(
        '--force_renew_certificate',
        '-r',
        action='store_true',
        help='Force renew certificate even if valid',
    )
    parser.add_argument('--username', '-u', required=True)
    parser.add_argument(
        '--force_renew_ca_certificates',
        '-x',
        action='store_true',
        help='Force renew CA certificates',
    )

    args = parser.parse_args()

    run(
        args.hostname,
        args.port,
        args.username,
        args.force_renew_certificate,
        args.force_renew_ca_certificates,
    )
