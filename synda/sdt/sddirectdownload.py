#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This script download files sequentially in foreground."""

import argparse
import os
import sys
import json
from synda.sdt import sdapp
from synda.sdt import sdutils
from synda.sdt import sdget
from synda.sdt.sdtypes import File
from synda.sdt.sdtools import print_stderr

from synda.source.config.process.download.constants import get_http_clients


def run(files,
        config_manager,
        timeout=0,
        force=False,
        http_client="",
        local_path_prefix="",
        verify_checksum=False,
        network_bandwidth_test=False,
        debug=True,
        verbosity=0,
        buffered=False,
        hpss=False):
    """
    Returns:
        0 if all transfers complete successfully
        1 if one or more transfer(s) didn't complete successfully
    """

    preferences = config_manager.get_user_preferences()

    if not timeout:
        timeout = preferences.download_direct_http_timeout

    if not http_client:
        http_client = get_http_clients()["aiohttp"]

    if not local_path_prefix:
        paths = config_manager.get_paths()
        local_path_prefix = paths.get("sandbox")

    failed_count = 0

    for file_ in files:

        # check

        assert 'url' in file_
        assert 'local_path' in file_

        if verify_checksum:
            if checksum_attrs_ok(file_):
                missing_remote_checksum_attrs = False
            else:
                missing_remote_checksum_attrs = True
        # cast

        f = File(**file_)

        # prepare attributes

        local_path = f.get_full_local_path(prefix=local_path_prefix)

        # check

        if not network_bandwidth_test:

            if os.path.isfile(local_path):

                if force:
                    os.remove(local_path)
                else:
                    print_stderr(
                        'Warning: download cancelled as local file already exists ({})'.format(
                            local_path,
                        ),
                    )

                    failed_count += 1

                    continue

        # special case

        if network_bandwidth_test:
            local_path = '/dev/null'

        # transfer

        status, killed, script_stderr = sdget.download(
            f.url,
            local_path,
            debug,
            timeout,
            verbosity,
            buffered,
            hpss,
        )

        # post-transfer

        if status != 0:
            failed_count += 1

            print_stderr(
                'Download failed ({})'.format(f.url),
            )

            # in non-buffered mode, stderr is already display (because child stderr is binded to parent stderr)

            if buffered:

                # currently, we don't come here but we may need in the futur so we keep this block

                if script_stderr is not None:
                    print_stderr(script_stderr)
        else:

            if network_bandwidth_test:
                return

            if verify_checksum:
                if missing_remote_checksum_attrs:
                    failed_count += 1

                    print_stderr(
                        'Warning: missing remote checksum attributes prevented checksum verification ({})'.format(
                            local_path,
                        ),
                    )
                else:

                    remote_checksum = f.checksum
                    local_checksum = sdutils.compute_checksum(local_path, f.checksum_type)

                    if local_checksum == remote_checksum:
                        print_stderr(
                            'File successfully downloaded, checksum OK ({})'.format(
                                local_path,
                            ),
                        )
                    else:
                        failed_count += 1

                        print_stderr(
                            "Error: local checksum don't match remote checksum ({})".format(
                                local_path,
                            ),
                        )
            else:
                print_stderr(
                    'File successfully downloaded, no checksum verification ({})'.format(
                        local_path,
                    ),
                )

    if failed_count > 0:
        return 1
    else:
        return 0


def checksum_attrs_ok(file_):
    if 'checksum_type' in file_ and 'checksum' in file_:
        return True
    else:
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    files = json.load(sys.stdin)
    status = run(files)

    sys.exit(status)
