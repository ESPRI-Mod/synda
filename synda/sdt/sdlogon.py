#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains security related functions."""

import argparse
from retrying import retry
import sdopenid
import sdlog
import sdmyproxy
from sdtools import print_stderr
import sdexception

from synda.source.config.file.certificate.x509.models import Config as SecurityFile


def print_certificate():
    import os
    import sdutils

    credentials = SecurityFile().get_credentials()

    if os.path.isfile(credentials):
        sdget_status, stdout, stderr = sdutils.get_status_output(
            ['/usr/bin/openssl', 'x509', '-in', credentials, '-text'],
            shell=False,
        )

        print stdout
    else:
        print_stderr("Certificate not found (use 'renew' command to retrieve a new certificate).")


# 50000 => 50 seconds
@retry(wait_fixed=50000, retry_on_exception=lambda e: isinstance(e, sdexception.SDException))
def renew_certificate_with_retry_highfreq(openid, password, force_renew_certificate=False):
    """
    Retry mecanism when ESGF IDP cannot be reached.

    Not used

    Notes
        - Retry when SDException occurs, raise any other errors
        - when the daemon is stopped, this retry is cancelled using SIGTERM
          (seems not working for now as it only stops on 'kill -9' TBC)
    """
    renew_certificate(
        openid,
        password,
        force_renew_certificate=force_renew_certificate,
    )


# 1800000 => 30mn, 86400000 => 24 hours
@retry(
    wait_exponential_multiplier=1800000,
    wait_exponential_max=86400000,
    retry_on_exception=lambda e: isinstance(e, sdexception.SDException),
)
def renew_certificate_with_retry(openid, password, force_renew_certificate=False):
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
    renew_certificate(
        openid,
        password,
        force_renew_certificate=force_renew_certificate,
    )


def renew_certificate(openid, password, force_renew_certificate=False, force_renew_ca_certificates=False):
    """Renew ESGF certificate using sdmyproxy module."""

    # extract info from openid

    success, hostname, port, username = sdopenid.extract_info_from_openid(openid)
    if success:
        try:
            sdmyproxy.run(
                hostname,
                port,
                username,
                force_renew_certificate,
                force_renew_ca_certificates,
                password,
            )

        except Exception, e:
            sdlog.error(
                "SYDLOGON-012",
                "Error occured while retrieving certificate from myproxy server (%s)" % str(e),
            )

            raise

    return success

# init.


if __name__ == '__main__':
    from synda.source.config.file.user.credentials.models import Config as Credentials

    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    credentials_ = Credentials()
    renew_certificate(
        credentials_.openid,
        credentials_.password,
        force_renew_certificate=True,
    )

    print_stderr("Certificate successfully renewed")
