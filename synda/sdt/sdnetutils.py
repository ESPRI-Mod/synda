#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains network functions."""
import urllib3
import urllib.request
import requests
from synda.sdt import sdtypes
from synda.sdt.sdexception import SDException
from synda.sdt.sdtime import SDTimer
from synda.sdt import sdlog
from synda.sdt import sdconfig
import http.client
from synda.sdt import sdtrace
import ssl

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.api.constants import OUTPUT_FORMAT_JSON
from synda.source.config.api.constants import OUTPUT_FORMAT_XML


class HTTPSClientAuthHandler(urllib.request.HTTPSHandler):
    """HTTP handler that transmits an X509 certificate as part of the request."""
    def __init__(self, key, cert):
            urllib.request.HTTPSHandler.__init__(self)
            self.key = key
            self.cert = cert
    def https_open(self, req):
            return self.do_open(self.getConnection, req)
    def getConnection(self, host, timeout=300):
            return http.client.HTTPSConnection(host, key_file=self.key, cert_file=self.cert)


# default is to load list resulting from HTTP call in memory
# (should work on lowmem machine as response should not exceed Preferences().esgf_search_api_chunksize)
def call_web_service(
        url,
        timeout=Preferences().api_esgf_search_http_timeout,
        lowmem=False,
):
    start_time = SDTimer.get_time()
    buf = http_get(url, timeout)
    elapsed_time = SDTimer.get_elapsed_time(start_time)

    buf=fix_encoding(buf)

    try:
        di = search_api_parser.parse_metadata(buf)
    except Exception as e:

        # If we are here, it's likely that they is a problem with the internet connection
        # (e.g. we are behind an HTTP proxy and have no authorization to use it)

        sdlog.info(
            'SDNETUTI-001',
            f'XML parsing error (exception={str(e)}). Most of the time, this error is due to a network error.',
        )

        # debug
        #
        # TODO: maybe always enable this
        #
        sdtrace.log_exception()

        # debug
        #
        # (if the error is not due to a network error (e.g. internet connection
        # problem), raise the original exception below and set the debug mode
        # to see the stacktrace.
        #
        #raise

        # we raise a new exception 'network error' here,
        # because most of the time, 'xml parsing error' is due to an 'network error'.
        raise SDException(
            'SDNETUTI-008',
            'Network error (see log for details)',
        )

    sdlog.debug(
        "SDNETUTI-044",
        "files-count=%d" % len(di.get('files')),
    )

    for difile in di['files']:
        difile['search_url'] = url

    # RAM storage is ok here as one response is limited by Preferences().api_esgf_search_chunksize
    return sdtypes.Response(
        call_duration=elapsed_time,
        lowmem=lowmem,
        **di,
    )


def call_param_web_service(url,timeout):
    buf = http_get(url, timeout)

    buf = fix_encoding(buf)

    try:
        params = search_api_parser.parse_parameters(buf)
    except Exception as e:

        # If we are here, it's likely that they is a problem with the internet connection
        # (e.g. we are behind an HTTP proxy and have no authorization to use it)

        raise SDException('SDNETUTI-003', 'Network error (%s)' % str(e))

    return params


def fix_encoding(buf):

    # HACK
    #
    # This is to prevent fatal error when document contain mixed encodings
    #
    # e.g. http://esgf-data.dkrz.de/esg-search/search?distrib=true&fields=*&type=File&limit=100&title=sftgif_fx_IPSL-CM5A-LR_abrupt4xCO2_r0i0p0.nc&format=application%2Fsolr%2Bxml&offset=0
    #
    if sdconfig.fix_encoding:
        from synda.sdt import sdencoding
        buf=sdencoding.fix_mixed_encoding_ISO8859_UTF8(buf)

    return buf


def http_get_2(url, timeout=20, verify=True):
    """requests impl."""

    buf = None

    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        result = requests.get(url, timeout=timeout, verify=verify)
        buf = result.text
    except Exception as e:
        errmsg = "HTTP query failed (url={},exception={},timeout={})".format(
            url,
            str(e),
            timeout,
        )
        errcode = "SDNETUTI-004"

        raise SDException(errcode, errmsg)

    return buf


def http_get(url, timeout=20):
    """urllib impl."""
    buf = None

    try:
        context = ssl.create_default_context()
        response = urllib.request.urlopen(url, timeout=timeout, context=context)
        buf = response.read()
    except Exception as e:
        errmsg = "HTTP query failed (url={},exception={},timeout={})".format(
            url,
            str(e),
            timeout,
        )
        errcode = "SDNETUTI-002"

        raise SDException(errcode, errmsg)

    return buf


def test_access():
    urlfile = urllib.request.urlopen("http://www.google.com")

    data_list = []
    chunk = 4096
    while 1:
        data = urlfile.read(chunk)
        if not data:
            break
        data_list.append(data)
        #print "Read %s bytes"%len(data)

def get_search_api_parser():
    if sdconfig.searchapi_output_format==OUTPUT_FORMAT_XML:
        assert False
    elif sdconfig.searchapi_output_format==OUTPUT_FORMAT_JSON:
        from synda.sdt import sdjson
        return sdjson
    else:
        assert False

# init.

search_api_parser=get_search_api_parser()


if __name__ == '__main__':
    _url = "http://aims3.llnl.gov/thredds/fileServer/cmip5_css02_data/cmip5/output1/CSIRO-QCCCE/CSIRO-Mk3-6-0/amip/mon/atmos/Amon/r1i1p1/tasmin/1/tasmin_Amon_CSIRO-Mk3-6-0_amip_r1i1p1_197901-200912.nc"
    _context = ssl.create_default_context()
    response = urllib.request.urlopen(_url, timeout=20, context=_context)
    data1 = response.read()
    data2 = http_get(_url, timeout=20)
    assert data1 == data2
