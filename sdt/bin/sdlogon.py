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

import commands
import os
import argparse
from retrying import retry
import sdapp
import sdconfig
import sdopenid
import sdutils
import sdlog
import sdmyproxy
from sdtools import print_stderr
import sdexception

def print_certificate():
    import os, sdutils

    if os.path.isfile(sdconfig.esgf_x509_proxy):
        (sdget_status,stdout,stderr)=sdutils.get_status_output(['/usr/bin/openssl','x509','-in',sdconfig.esgf_x509_proxy,'-text'],shell=False)
        print stdout
    else:
        print_stderr("Certificate not found (use 'renew' command to retrieve a new certificate).")

@retry(wait_fixed=50000,retry_on_exception=lambda e: isinstance(e, sdexception.SDException)) # 50000 => 50 seconds
def renew_certificate_with_retry_highfreq(openid,password,force_renew_certificate=False):
    """
    Retry mecanism when ESGF IDP cannot be reached.

    Not used

    Notes
        - Retry when SDException occurs, raise any other errors
        - when the daemon is stopped, this retry is cancelled using SIGTERM
          (seems not working for now as it only stops on 'kill -9' TBC)
    """
    renew_certificate(openid,password,force_renew_certificate=force_renew_certificate)

@retry(wait_exponential_multiplier=1800000, wait_exponential_max=86400000,retry_on_exception=lambda e: isinstance(e, sdexception.SDException)) # 1800000 => 30mn, 86400000 => 24 hours
def renew_certificate_with_retry(openid,password,force_renew_certificate=False):
    """
    Retry mecanism when ESGF IDP cannot be reached.

    Not used

    Notes
        - IDP is periodically contacted using the following schedule: 
          1h, 2h, 4h, 8h, 16h, 24h, 24h, 24h, 24h...
          (based on 2^x which gives 2, 4, 8, 16, 32, 64, 128..)
        - Retry when SDException occurs, raise any other errors
        - when the daemon is stopped, this retry is cancelled using SIGTERM
          (seems not working for now as it only stops on 'kill -9' TBC)
    """
    renew_certificate(openid,password,force_renew_certificate=force_renew_certificate)

def renew_certificate(openid,password,force_renew_certificate=False,force_renew_ca_certificates=False):
    """Renew ESGF certificate using sdmyproxy module."""

    # extract info from openid
    try:
        (hostname,port,username)=sdopenid.extract_info_from_openid(openid)
    except Exception,e:
        sdlog.error("SYDLOGON-800","Exception occured while processing openid (%s)"%str(e))
        raise

    try:
        sdmyproxy.run(hostname,port,username,force_renew_certificate,force_renew_ca_certificates,password)
    except Exception,e:
        sdlog.error("SYDLOGON-012","Error occured while retrieving certificate from myproxy server (%s)"%str(e))
        raise

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    renew_certificate(sdconfig.openid,sdconfig.password,force_renew_certificate=True)

    print_stderr("Certificate successfully renewed")
