#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains 'synda install' related routines."""

import argparse
from synda.sdt import sdconfig
from synda.sdt import sdi18n
from synda.sdt import sdexception
from synda.sdt import sdlog
from synda.sdt.sdtools import print_stderr

from synda.source.config.process.download.constants import TRANSFER


def run(args, metadata=None):

    from synda.sdt import syndautils

    syndautils.check_daemon()

    if metadata is None:

        # retrieve metadata

        if args.incremental and not args.selection_file:
            print_stderr(
                "ERROR: 'selection_file' option is not set (a selection file must be used when "
                "'incremental' option is set)",
            )

            return 1, 0

        if args.selection_file is not None:
            sdlog.info("SYNDINST-006", "Process '{}'".format(args.selection_file))

        try:
            metadata = syndautils.file_full_search(args)
        except sdexception.EmptySelectionException as e:
            print_stderr('No dataset will be installed, upgraded, or removed.')
            return 0, 0
        except sdexception.SDException as e:
            sdlog.info("SYNDINST-006", "Exception occured during installation ('{}')".format(e))
            raise

    # in dry-run mode, we stop here
    if args.dry_run:
        return 0, 0

    interactive = not args.yes

    return _install(metadata, interactive, args.config_manager, args.timestamp_right_boundary)


def _install(metadata, interactive, config_manager, timestamp_right_boundary=None):

    # Compute total files stat
    count_total = metadata.count()

    sdlog.info("SYNDINST-001", "'keep new status' process begins")

    # Compute new files stat
    #
    # (yes, block below is a duplicate of what is done inside sdenqueue.run()
    # method, but safer to keep it there too, and should be no harm in term of
    # perfomance)
    #
    from synda.sdt import sdsimplefilter
    from synda.sdt import sdconst

    metadata = sdsimplefilter.run(metadata, 'status', TRANSFER["status"]['new'], 'keep')
    metadata = sdsimplefilter.run(metadata, 'url', "//None", 'remove_substr')
    count_new = metadata.count()
    size_new = metadata.size

    sdlog.info("SYNDINST-024", "'keep new status' process ends")

    # what to do if no match
    if count_new < 1:

        if count_total > 0:
            sdlog.info(
                "SYNDINST-027",
                "Nothing to install (matching files are already installed or waiting in the download queue)."
                " To monitor transfers status and progress, use 'synda queue' command.",
                stderr=interactive,
            )
        else:
            sdlog.info("SYNDINST-028", 'Nothing to install (0 file found).', stderr=interactive)

        return 0, 0

    # ask user for confirmation
    if interactive:

        import humanize

        print_stderr(
            '{} file(s) will be added to the download queue.'.format(count_new),
        )

        print_stderr(
            'Once downloaded, {} of additional disk space will be used.'.format(
                humanize.naturalsize(
                    size_new,
                    gnu=False,
                ),
            ),
        )

        from synda.sdt import sdutils
        if sdutils.query_yes_no('Do you want to continue?', default="yes"):
            installation_confirmed = True
        else:
            installation_confirmed = False
    else:
        installation_confirmed = True

    sdlog.info("SYNDINST-002", "Store metadata in database..")

    # install
    if installation_confirmed:

        from synda.sdt import sdenqueue
        sdenqueue.run(metadata, config_manager, timestamp_right_boundary)

        if interactive:
            print_stderr(
                "{} file(s) enqueued".format(count_new),
            )
            print_stderr(
                "You can follow the download using 'synda watch' and 'synda queue' commands",
            )
            from synda.sdt import sddaemon
            if not sddaemon.is_running():
                msg = sdi18n.m0026
                print_stderr(
                    "The daemon is not running. To start it, use '{}'.".format(msg),
                )
    else:
        if interactive:
            print_stderr('Abort.')

    sdlog.info("SYNDINST-025", "Task complete")

    return 0, count_new

# init.


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
