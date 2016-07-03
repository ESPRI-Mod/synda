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
from sdexception import SDException,CertificateRenewalException

def print_certificate():
    import os, sdutils

    certdirprefix=sdconfig.tmp_folder if sdconfig.multiuser else os.environ.get('HOME')

    certificate_file='%s/.esg/credentials.pem'%certdirprefix

    if os.path.isfile(certificate_file):
        (sdget_status,stdout,stderr)=sdutils.get_status_output(['/usr/bin/openssl','x509','-in',certificate_file,'-text'],shell=False)
        print stdout
    else:
        print_stderr("Certificate not found (use 'renew' command to retrieve a new certificate).")

@retry(wait_fixed=50000,retry_on_exception=lambda e: isinstance(e, SDException)) # 50000 => 50 seconds
def renew_certificate_with_retry_highfreq():
    """
    Retry mecanism when ESGF IDP cannot be reached.

    Not used

    Notes
        - Retry when SDException occurs, raise any other errors
        - when the daemon is stopped, this retry is cancelled using SIGTERM
          (seems not working for now as it only stops on 'kill -9' TBC)
    """
    renew_certificate(force_renew_certificate=False,quiet=True)

@retry(wait_exponential_multiplier=1800000, wait_exponential_max=86400000,retry_on_exception=lambda e: isinstance(e, SDException)) # 1800000 => 30mn, 86400000 => 24 hours
def renew_certificate_with_retry(force,quiet=True):
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
    renew_certificate(force_renew_certificate=force,quiet=quiet)

def renew_certificate(force_renew_certificate=False,quiet=True,debug=False,force_renew_ca_certificates=False):

    # retrieve openid and password
    openid=sdconfig.config.get('esgf_credential','openid')
    password=sdconfig.config.get('esgf_credential','password')

    # extract info from openid
    (hostname,port,username)=sdopenid.extract_info_from_openid(openid)

    if sdconfig.use_myproxy_module:
        renew_certificate_new(hostname,port,username,password,force_renew_certificate=force_renew_certificate,quiet,debug,force_renew_ca_certificates)
    else:
        renew_certificate_old(hostname,port,username,password,force_renew_certificate=force_renew_certificate,quiet,debug,force_renew_ca_certificates)

def renew_certificate_new(hostname,port,username,password,force_renew_certificate=False,quiet=True,debug=False,force_renew_ca_certificates=False): # TODO: remove quiet and debug argument when removing sdlogon.sh (i.e. only here to keep the same func signature)
    """Renew ESGF certificate using sdmyproxy module."""

    # main
    try:
        sdmyproxy.run(hostname,port,username,force_renew_certificate,force_renew_ca_certificates,password)
    except Exception,e:
        sdlog.error("SDMYPROX-012","Error occured while retrieving certificate from myproxy server (%s)"%str(e))
        raise

def renew_certificate_old(hostname,port,username,password,force_renew_certificate=False,quiet=True,debug=False,force_renew_ca_certificates=False):
    """Renew ESGF certificate using 'sdlogon.sh' script."""

    # TODO: move this log into the script so to print only when expired
    #sdlog.info("SYDLOGON-002","Renew certificate..")

    # note: password is not used in this func: this is normal (it is retrieved by the shell script)

    argv=[sdconfig.logon_script,'-h',hostname,'-p',port,'-s',sdconfig.security_dir,'-u',username]

    if not quiet:
        argv.append('-v')

    if force_renew_certificate:
        argv.append('-r')

    if force_renew_ca_certificates:
        argv.append('-x')

    (status,stdout,stderr)=sdutils.get_status_output(argv)
    if status!=0:

        # print script stdxxx output (useful to debug certificate problem)
        if quiet:
            with open(sdconfig.stacktrace_log_file,'a') as fh:
                fh.write("'%s' script returned an error\n"%os.path.basename(sdconfig.logon_script))
                fh.write('status=%s\nstdout=%s\nstderr=%s\n'%(status,stdout.rstrip(os.linesep),stderr.rstrip(os.linesep)))
        else:
            print_stderr("'%s' script returned an error\n"%os.path.basename(sdconfig.logon_script))
            print_stderr('status=%s\nstdout=%s\nstderr=%s\n'%(status,stdout.rstrip(os.linesep),stderr.rstrip(os.linesep)))

        sdlog.error("SYDLOGON-040","Exception occured while retrieving certificate (status=%i)"%status)

        raise CertificateRenewalException("SYDLOGON-001","Cannot retrieve certificate from ESGF (hostname=%s,port=%s)"%(hostname,port))
    else:
        if debug:
            print_stderr("'%s' script stdxxx (debug mode)\n"%os.path.basename(sdconfig.logon_script))
            print_stderr('status=%s\nstdout=%s\nstderr=%s\n'%(status,stdout.rstrip(os.linesep),stderr.rstrip(os.linesep)))

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    renew_certificate(force_renew_certificate=True,quiet=False,debug=True)

    print_stderr("Certificate successfully renewed")
