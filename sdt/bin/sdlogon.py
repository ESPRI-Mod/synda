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
import sdapp
from sdexception import SDException,CertificateRenewalException
import sdconfig
import sdopenid
import sdutils
import sdlog
from sdtools import print_stderr

def print_certificate():
    import os, sdutils
    certificate_file='%s/.esg/credentials.pem'%os.environ.get('HOME')
    if os.path.isfile(certificate_file):
        (sdget_status,stdout,stderr)=sdutils.get_status_output(['/usr/bin/openssl','x509','-in',certificate_file,'-text'],shell=False)
        print stdout
    else:
        print_stderr("Certificate not found (use 'renew' command to retrieve a new certificate).")

def is_openid_set():
    if openid=='https://esgf-node.ipsl.fr/esgf-idp/openid/foo':
        return False
    else:
        return True

def renew_certificate(force,quiet=True):
    """Renew ESGF certificate."""

    # TODO: move this log into the script so to print only when expired
    #sdlog.info("SYDLOGON-002","Renew certificate..")

    (hostname,port,username)=sdopenid.extract_info_from_openid(openid)

    argv=[sdconfig.logon_script]
    argv.append('-h %s'%hostname)
    argv.append('-p %s'%port)
    argv.append('-u %s'%username)

    if not quiet:
        argv.append('-v')

    if force is True:
        argv.append('-r')

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

# Init.

openid=sdconfig.config.get('esgf_credential','openid')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    renew_certificate(True)
