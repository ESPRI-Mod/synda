#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains data file download routines.

Notes
    - This module provides 3 ways to download data file
        - urllib.request (pure python)
        - wget (external script)
        - gridftp (external script)
    - This module is mainly used as module, but can also be used as script for basic
      url download test.
"""

import argparse
import os
import sys
import json
from synda.sdt import sdconfig
from synda.sdt import sdutils
from synda.sdt import sdget_urllib
from synda.sdt.sdtools import print_stderr

from synda.source.config.file.scripts.models import Config as Scripts
from synda.source.config.path.tree.certificate.x509.models import Config as SecurityPath

from synda.source.config.path.tree.models import Config as TreePath

from synda.source.config.file.user.preferences.models import Config as Preferences

from synda.source.config.process.download.constants import get_http_clients
from synda.source.config.process.download.constants import get_transfer_protocols

def download(
        url,
        full_local_path,
        debug=False,
        http_client=sdconfig.http_client,
        timeout=Preferences().download_async_http_timeout,
        verbosity=0,
        buffered=True,
        hpss=False,
):
    killed = False
    script_stderr = None

    transfer_protocol = sdutils.get_transfer_protocol(url)

    if transfer_protocol == get_transfer_protocols()['http']:

        if http_client == get_http_clients()["urllib"]:

            status = sdget_urllib.download_file(
                url,
                full_local_path,
                timeout,
            )

        elif http_client == get_http_clients()["wget"]:

            data_download_script_http = Scripts().get("sdget")

            li = prepare_args(
                url,
                full_local_path,
                data_download_script_http,
                debug,
                timeout,
                verbosity,
                hpss,
            )

            status, script_stderr = run_download_script(li, buffered)

            killed = is_killed(transfer_protocol, status)

        else:
            assert False

    elif transfer_protocol == get_transfer_protocols()['gridftp']:

        gridftp_opt = Preferences().download_gridftp_opt

        if len(gridftp_opt) > 0:
            os.environ["GRIDFTP_OPT"] = gridftp_opt

        data_download_script_gridftp = Scripts().get("sdgetg")

        li = prepare_args(
            url,
            full_local_path,
            data_download_script_gridftp,
            debug,
            timeout,
            verbosity,
            hpss,
        )

        status, script_stderr = run_download_script(li, buffered)

        killed = is_killed(transfer_protocol, status)

    else:

        assert False

    return status, killed, script_stderr


def run_download_script(li, buffered):
    if buffered:
        return run_download_script_BUFSTDXXX(li)
    else:
        return run_download_script_RTSTDXXX(li)


def run_download_script_RTSTDXXX(li):

    # start a new process (fork is blocking here, so thread will wait until child is done)
    status = sdutils.get_status(li, shell=False)

    return status, None


def run_download_script_BUFSTDXXX(li):

    # start a new process (fork is blocking here, so thread will wait until child is done)
    #
    # note
    #  in the child shell script, stderr for error message
    #
    status, stdout, stderr = sdutils.get_status_output(li, shell=False)

    # download scripts may
    #   - return error message on stderr, one line terminated by EOL
    #   - return error message on stderr, multiple lines, each terminated by EOL

    # first, we chomp
    #
    # note
    #     only the last eol is chomped here.
    #
    stderr = stderr.rstrip('\r\n')

    # then we replace all eol from string but the last (which has already been chomped)
    #
    stderr = stderr.replace('\n', '<eol-n>').replace('\r', '<eol-r>')

    # encoding
    #
    # Depending on which encoding is set in the system, scripts can return
    # utf-8, latin1, or something else.
    #
    # As for now, Synda encoding is latin1 (this is enforced by setting
    # 'LANG=C' in external script), we remove any non-latin1 character if any.
    #
    # TODO
    #     In the futur, Synda will move to unicode instead of latin1.
    #     Thus, external scripts output encoding will have to be converted to
    #     unicode before being processed by synda
    #
    #     All synda input should be checked to only accept unicode
    #     (except for specific case where input encoding must be specific, in
    #     which case we make the required explicit conversion to obtain unicode)
    #
    #     samples
    #     stderr=unicode(stderr, encoding='utf-8')
    #     stderr=unicode(stderr, encoding='latin1')
    #
    #
    stderr = str(stderr, errors='ignore').encode('latin1')

    # debug (unexpected errors may be hidden in stdxxx)
    """
    with open(Log().get("stack_trace"),'a') as fh:
        fh.write("BEGIN '%s' script output\n"%os.path.basename(script))
        fh.write("status: %s\n"%status)
        fh.write("stdout:\n")
        fh.write(stdout)
        fh.write("stderr:\n")
        fh.write(stderr)
        fh.write("END '%s' script output\n"%os.path.basename(script))
    """

    return status, stderr


def is_killed(transfer_protocol, status):
    """This func return True if child process has been killed."""

    if transfer_protocol == get_transfer_protocols()['http']:
        if sdconfig.http_client == get_http_clients()["wget"]:
            if status in (7, 29):
                return True
            else:
                return False
        elif sdconfig.http_client == get_http_clients()["urllib"]:
            return False
        else:
            assert False
    elif transfer_protocol == get_transfer_protocols()['gridftp']:
        return False  # TODO
    else:
        assert False


def build_verbosity_option(verbosity):
    """
    sample
        0 => None
        2 => '-vv'
        4 => '-vvvv'
    """

    if verbosity > 0:
        buf = 'v'*verbosity
        buf = '-%s' % buf
        return buf
    else:
        return None


def prepare_args(
        url,
        full_local_path,
        script,
        debug,
        timeout,
        verbosity,
        hpss,
):
    tmp_folder = TreePath().get("tmp")
    log_folder = TreePath().get("log")

    li = [
        script,
        '-l',
        log_folder,
        '-T',
        tmp_folder,
        '-t',
        str(timeout),
        '-c',
        SecurityPath().get_security(),
        url,
        full_local_path,
    ]

    if debug:
        li.insert(1, '-d')

    verbosity_option = build_verbosity_option(verbosity)
    if verbosity_option is not None:
        li.insert(1, verbosity_option)

    if hpss:
        li.insert(1, '-p')
        li.insert(2, '0')

    return li

# init.


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--quiet', action='store_true')
    args = parser.parse_args()

    files = json.load(sys.stdin)

    for f in files:

        assert 'url' in f

        _url = f['url']
        local_path = '/tmp/test.nc'

        if os.path.isfile(local_path):
            os.remove(local_path)

        _status, _killed, _script_stderr = download(_url, local_path, debug=True)

        if _status != 0:
            if not args.quiet:
                print_stderr('Download failed: %s' % _url)

            sys.exit(1)

    if not args.quiet:
        print_stderr('File(s) successfully downloaded')

    sys.exit(0)
