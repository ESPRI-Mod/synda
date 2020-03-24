#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains security related functions."""

# import commands
import os
import argparse
import textwrap
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import base
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from sdt.bin.commons.utils import sdconfig, sdlog
from sdt.bin.commons import sdopenid
from sdt.bin.commons import sdmyproxy
from sdt.bin.commons.utils.sdprint import print_stderr


def print_certificate():
    """
    Instead of calling openssl command from shell
    this method gives the best approximation of the
    openssl return all while staying in Python.
    The purpose is to facilitate maintenance.
    :return: prints x509 certificate if found.
    """
    if os.path.isfile(sdconfig.esgf_x509_proxy):
        with open(sdconfig.esgf_x509_proxy, 'rb') as pem_file:
            cert = x509.load_pem_x509_certificate(pem_file.read(), backend=default_backend())
            print("Certificate:")
            print("    Data:")
            print("        Version: {}".format(int(cert.version.value)))
            print("        Serial Number: {}".format(cert.serial_number))
            print("    Signature Algorithm: {}".format(cert.signature_hash_algorithm.name))
            print("    Issuer: {}".format(cert.issuer))
            print("    Validity")
            print("        Not Before: {}".format(cert.not_valid_before))
            print("        Not After : {}".format(cert.not_valid_after))
            print("    Subject: {}".format(cert.subject))
            keytype = cert.public_key()
            if isinstance(keytype, RSAPublicKey):
                print('Keytype : RSA')
                modulus = keytype.public_numbers().n
                exponent = keytype.public_numbers().e
                formatted_modulus = "\n                ".join(textwrap.wrap(str(modulus), 45))
                print("            Modulus:")
                print("                {}".format(formatted_modulus))
                print("            Exponent {} (0x{})".format(exponent, exponent))
            print("        X509v3 extensions:")
            print('            {}:{}'.format(cert.extensions._extensions[0].oid.dotted_string,
                                             cert.extensions._extensions[0].value.value.decode('utf-8')))
            print("    Signature Algorithm: {}".format(cert.signature_hash_algorithm.name))
            print("\n                ".join(textwrap.wrap(str(cert.signature), 45)))
            print(cert.public_bytes(base.Encoding.PEM).decode('utf-8'))

    else:
        print_stderr("Certificate file not found."
                     " Check your sdt conf file for the correct certificate file path"
                     " or use the certificate renew command to get a new one")


def renew_certificate(openid, password, force_renew_certificate=False, force_renew_ca_certificates=False):
    """Renew ESGF certificate using sdmyproxy module."""

    # extract info from openid
    try:
        hostname, port, username = sdopenid.extract_info_from_openid(openid)
    except Exception as e:
        sdlog.error("SYDLOGON-800", "Exception occured while processing openid ({})".format(str(e)))
        raise

    try:
        sdmyproxy.run(hostname, port, username, force_renew_certificate, force_renew_ca_certificates, password)
    except Exception as e:
        sdlog.error("SYDLOGON-012",
                    "Error occured while retrieving certificate from myproxy server ({})".format(str(e)))
        raise


# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    renew_certificate(sdconfig.openid, sdconfig.password, force_renew_certificate=True)

    print_stderr("Certificate successfully renewed")
