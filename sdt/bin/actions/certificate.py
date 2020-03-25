#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
from sdt.bin.commons.utils import sdconfig, sdlogon


def run(args):
    if args.action is None:
        sdlogon.print_certificate()
        return 0
    else:
        if args.action == "renew":

            # retrieve openid and passwd
            if args.openid and args.password:
                # use credential from CLI

                oid = args.openid
                pwd = args.password
            else:
                # use credential from file

                if sdconfig.is_openid_set():
                    oid = sdconfig.openid
                    pwd = sdconfig.password
                else:
                    sys.stderr.write('Error: OpenID not set in configuration file ({}).'.
                                     format(sdconfig.credential_file))
                    return 1

            # retrieve certificate
            try:
                sdlogon.renew_certificate(oid, pwd, force_renew_certificate=True,
                                          force_renew_ca_certificates=args.force_renew_ca_certificates)
                print('Certificate successfully renewed.')
                return 0
            except Exception as e:
                print('Error occurs while renewing certificate ({})'.format(str(e)))
                return 1
        elif args.action == "info":
            print('ESGF CA certificates location: {}'.format(sdconfig.esgf_x509_cert_dir))
            print('ESGF user certificate location: {}'.format(sdconfig.esgf_x509_proxy))
            return 0
        elif args.action == "print":
            sdlogon.print_certificate()
            return 0
        else:
            print(args.action)
            print('Not implemented yet.')
            return 1
