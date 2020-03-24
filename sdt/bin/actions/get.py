#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright (c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import os
import humanize

from sdt.bin.commons import syndautils
from sdt.bin.commons import sdlogon
from sdt.bin.commons.utils import sdconfig
from sdt.bin.commons.utils import sdconst
from sdt.bin.commons.param import sddeferredafter
from sdt.bin.commons.search import sdearlystreamutils
from sdt.bin.commons.search import sdrfile
from sdt.bin.commons.esgf import sddirectdownload


def run(args):
    # hack
    # see TAG43534FSFS
    if args.quiet:
        args.verbosity = 0

    if args.verify_checksum and args.network_bandwidth_test:
        print_stderr("'verify_checksum' option cannot be set when 'network_bandwidth_test' option is set.")
        return 1

    stream = syndautils.get_stream(subcommand=args.subcommand, parameter=args.parameter,
                                   selection_file=args.selection_file)

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
            print_stderr('Error: OpenID not set in configuration file ({}).'.format(sdconfig.credential_file))

            return 1
    # retrieve certificate
    sdlogon.renew_certificate(oid, pwd, force_renew_certificate=False)

    # local_path
    #
    # 'synda get' subcommand currently force local_path to the following construct:
    # '<dest_folder>/<filename>' (i.e. you can't use DRS tree in-between). This may
    # change in the future.
    #
    if args.dest_folder is None:
        local_path_prefix = os.getcwd()  # current working directory
    else:
        local_path_prefix = args.dest_folder

    # BEWARE
    #
    # when set in CLI parameter, url is usually an ESGF facet, and as so should
    # be sent to the search-api as other facets
    # BUT
    # we want a special behaviour here (i.e. with 'synda get' command) with url:
    # if url is set by user, we DON'T call search-api operator. Instead, we
    # download the url directly.

    urls = sdearlystreamutils.get_facet_values_early(stream, 'url')
    if len(urls) == 0:
        # no url in stream: switch to search-api operator mode

        sddeferredafter.add_default_parameter(stream, 'limit', 5)
        sddeferredafter.add_forced_parameter(stream, 'local_path_format', 'notree')

        # yes: this is the second time we run sdinference filter, but it doesn't hurt as sdinference is idempotent
        files = sdrfile.get_files(stream=stream, post_pipeline_mode='file', dry_run=args.dry_run)

        if not args.dry_run:
            if len(files) > 0:
                # compute metric
                total_size = sum(int(f['size']) for f in files)
                total_size = humanize.naturalsize(total_size, gnu=False)
                print_stderr('{} file(s) will be downloaded for a total size of {}'.format(len(files), total_size))
                status = sddirectdownload.run(files,
                                              args.timeout,
                                              args.force,
                                              local_path_prefix,
                                              verify_checksum=args.verify_checksum,
                                              network_bandwidth_test=args.network_bandwidth_test,
                                              debug=True,
                                              verbosity=args.verbosity,
                                              buffered=False,
                                              hpss=args.hpss)
                if status != 0:
                    return 1
            else:
                print_stderr("File not found")
                return 1
        else:
            for f in files:
                size = humanize.naturalsize(f['size'], gnu=False)
                print('%-12s %s' % (size, f['filename']))

    elif len(urls) > 0:
        # url(s) found in stream: search-api operator not needed (download url directly)
        # TAGDSFDF432F
        if args.verify_checksum:
            print_stderr("To perform checksum verification, ESGF file identifier (e.g. title, id, tracking id..) "
                         "must be used instead of file url.")
            return 1
        # TODO: to improve genericity, maybe merge this block into the previous one
        #  (i.e. url CAN be used as a search key in the search-api (but not irods url))

        files = []
        for url in urls:
            filename = os.path.basename(url)
            local_path = filename
            f = dict(local_path=local_path, url=url)
            files.append(f)
        status = sddirectdownload.run(files,
                                      args.timeout,
                                      args.force,
                                      http_client,
                                      local_path_prefix,
                                      verify_checksum=args.verify_checksum,  # see above at TAGDSFDF432F
                                      network_bandwidth_test=args.network_bandwidth_test,
                                      debug=True,
                                      verbosity=args.verbosity,
                                      buffered=False,
                                      hpss=args.hpss)
        if status != 0:
            return 1
    else:
        assert False
    return 0
