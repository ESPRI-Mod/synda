#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script contains OpenID related functions.

Credit
    https://github.com/stephenpascoe/esgf-pyclient
"""

from xml.etree import ElementTree
import re
import argparse
from synda.sdt import sdlog
from synda.sdt import sdtools
from synda.sdt import sdutils
from synda.sdt.sdexception import OpenIDIncorrectFormatException,OpenIDProcessingException
from synda.sdt import sdnetutils

XRI_NS = 'xri://$xrd*($v*2.0)'
MYPROXY_URN = 'urn:esg:security:myproxy-service'
ESGF_OPENID_REXP = r'https://.*/([^/]+)$'
MYPROXY_URI_REXP = r'socket://([^:]*):?(\d+)?'


def extract_info_from_openid(openid):
    """Retrieve username,host,port informations from ESGF openID."""
    success = False
    hostname = None
    port = None
    # openid check (see #44 for more info)
    for openid_host in invalid_openids:
        if openid_host in openid:
            sdlog.warning("SDOPENID-210","Invalid openid (%s)"%openid)
    try:
        xrds_buf = sdnetutils.http_get_2(openid, timeout=10, verify=False)
        try:
            hostname, port = parse_xrds(xrds_buf)
            success = True
        except Exception as e:
            sdtools.print_stdout("FOLLOWING ERROR captured from ESGF openid Service...\n")
            sdtools.print_stdout(xrds_buf)
    except Exception as e:
        sdtools.print_stdout("FOLLOWING ERROR captured from ESGF openid Service...\n")
        sdtools.print_stdout(e)
    if success:
        try:
            username=parse_openid(openid)
            return success, hostname, port, username
        except Exception as e:
            sdlog.error("SDOPENID-200","Error occured while processing OpenID (%s)"%str(e))
            raise OpenIDProcessingException('SDOPENID-002','Error occured while processing OpenID')
    else:
        return success, "", "", ""


def parse_xrds(xrds_document):
    xml = ElementTree.fromstring(xrds_document)

    hostname = None
    port = None
    username = None

    services = xml.findall('.//{%s}Service' % XRI_NS)
    for service in services:
        try:
            service_type = service.find('{%s}Type' % XRI_NS).text
        except AttributeError:
            continue

        # Detect myproxy hostname and port
        if service_type == MYPROXY_URN:
            myproxy_uri = service.find('{%s}URI' % XRI_NS).text
            m = re.match(MYPROXY_URI_REXP, myproxy_uri)
            if m:
                hostname, port = m.groups()

    return hostname, port


def parse_openid(openid):

    # In standard ESGF pattern, openID contains the username
    m = re.match(ESGF_OPENID_REXP, openid)
    if m:
        username = m.group(1)
    else:
        raise OpenIDIncorrectFormatException('SDOPENID-001','Incorrect format')

    return username

# init.


invalid_openids = ['earthsystemgrid.org']
