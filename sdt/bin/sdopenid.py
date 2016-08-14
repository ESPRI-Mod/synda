#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

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
import sdlog
import sdutils
from sdexception import OpenIDIncorrectFormatException,OpenIDProcessingException
import sdnetutils

XRI_NS = 'xri://$xrd*($v*2.0)'
MYPROXY_URN = 'urn:esg:security:myproxy-service'
ESGF_OPENID_REXP = r'https://.*/([^/]+)$'
MYPROXY_URI_REXP = r'socket://([^:]*):?(\d+)?'

def extract_info_from_openid(openid):
    """Retrieve username,host,port informations from ESGF openID."""

    # openid check (see #44 for more info)
    for openid_host in invalid_openids:
        if openid_host in openid:
            sdlog.warning("SDOPENID-210","Invalid openid (%s)"%openid)
    

    try:
        xrds_buf=sdnetutils.HTTP_GET_2(openid,timeout=10,verify=False)
        (hostname,port)=parse_XRDS(xrds_buf)
        username=parse_openid(openid)
        return (hostname,port,username)
    except Exception,e:
        sdlog.error("SDOPENID-200","Error occured while processing OpenID (%s)"%str(e))

        raise OpenIDProcessingException('SDOPENID-002','Error occured while processing OpenID')

def parse_XRDS(XRDS_document):
    xml = ElementTree.fromstring(XRDS_document)

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

invalid_openids=['earthsystemgrid.org']

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o','--openid',default="https://esgf-node.ipsl.fr/esgf-idp/openid/foobar")
    args = parser.parse_args()

    (hostname,port,username)=extract_info_from_openid(args.openid)

    print "Username: %s"%username
    print "Myproxy hostname: %s"%hostname
    print "Myproxy port: %s"%port
