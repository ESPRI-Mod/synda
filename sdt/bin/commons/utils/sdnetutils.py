#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright œ(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains network functions."""

import requests
import ssl
from sdt.bin.models import sdtypes
from sdt.bin.commons.utils import sdconfig, sdtrace
from sdt.bin.commons.utils import sdlog
from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.utils import sdtime
from sdt.bin.commons.utils import sdxml
from sdt.bin.commons.utils import sdjson
from sdt.bin.commons.utils.sdexception import SDException


def call_web_service(url, timeout=sdconst.SEARCH_API_HTTP_TIMEOUT, lowmem=False):
    """
    default is to load list resulting from HTTP call in memory. This should work on low memory machines as response
    should not exceed SEARCH_API_CHUNKSIZE.
    :param url: request url
    :param timeout: timeout value
    :param lowmem: boolean for low memory case.
    :return: request response
    """
    start_time = sdtime.SDTimer.get_time()
    buf = HTTP_GET(url, timeout)
    elapsed_time = sdtime.SDTimer.get_elapsed_time(start_time)
    buf = fix_encoding(buf)

    try:
        di = search_api_parser.parse_metadata(buf)
    except Exception as e:

        # If we are here, it's likely that they is a problem with the internet connection
        # (e.g. we are behind an HTTP proxy and have no authorization to use it)

        sdlog.info('SDNETUTI-001', 'XML parsing error (exception={}). Most of the time,'
                                   ' this error is due to a network error.'.format(str(e)))

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
        # raise

        raise SDException('SDNETUTI-008',
                          'Network error (see log for details)')  # we raise a new exception 'network error' here, because most of the time, 'xml parsing error' is due to an 'network error'.

    sdlog.debug("SDNETUTI-044", "files-count={}".format(len(di.get('files'))))

    # RAM storage is ok here as one response is limited by SEARCH_API_CHUNKSIZE
    return sdtypes.Response(call_duration=elapsed_time, lowmem=lowmem, **di)


def call_param_web_service(url, timeout):
    buf = HTTP_GET(url, timeout)

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
        pass
    return buf


def HTTP_GET(url, timeout=20, verify=True):
    """
    simple http get via requests. buffer is cast into ascii string.
    :param url:
    :param timeout:
    :param verify:
    :return:
    """

    buf = None

    try:
        result = requests.get(url, timeout=timeout, verify=verify)
        buf = result.text.encode('ascii', 'ignore')
    except Exception as e:
        errmsg = "HTTP query failed (url={},exception={},timeout=)".format(url, str(e), timeout)
        errcode = "SDNETUTI-004"
        raise SDException(errcode, errmsg)

    return buf


def get_search_api_parser():
    if sdconfig.searchapi_output_format == sdconst.SEARCH_API_OUTPUT_FORMAT_XML:
        return sdxml
    elif sdconfig.searchapi_output_format == sdconst.SEARCH_API_OUTPUT_FORMAT_JSON:
        return sdjson
    else:
        assert False


def allow_self_signed_certificate():
    """Handle target environment that doesn't support HTTPS verification.

    This is needed for example to allow SDT<=>SDP communication over
    JSONRPC/HTTPS using a self_signed_certificate (in a Python 2.7+ context).

    For more information, see https://www.python.org/dev/peps/pep-0476
    """

    try:
        _create_unverified_https_context = ssl._create_unverified_context
        ssl._create_default_https_context = _create_unverified_https_context
    except AttributeError:
        # legacy Python that doesn't verify HTTPS certificates by default

        pass


# init.

search_api_parser = get_search_api_parser()
