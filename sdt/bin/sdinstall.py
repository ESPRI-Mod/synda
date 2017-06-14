#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains 'synda install' related routines."""

import sys
import argparse
import sdconfig
import sdi18n
import sdexception
import sdlog
from sdtools import print_stderr

def run(args,metadata=None):
    import syndautils

    syndautils.check_daemon()

    if metadata is None:

        # retrieve metadata

        if args.incremental and not args.selection_file:
            print_stderr("ERROR: 'selection_file' option is not set (a selection file must be used when 'incremental' option is set)")
            return (1,0)

        if args.selection_file is not None:
            sdlog.info("SYNDINST-006","Process '%s'"%args.selection_file)

        try:
            metadata=syndautils.file_full_search(args)
        except sdexception.EmptySelectionException, e:
            print_stderr('No dataset will be installed, upgraded, or removed.')
            return (0,0)
        except sdexception.SDException, e:
            sdlog.info("SYNDINST-006","Exception occured during installation ('%s')"%str(e))
            raise

    # in dry-run mode, we stop here
    if args.dry_run:
        return (0,0)

    interactive=not args.yes

    return _install(metadata,interactive,args.timestamp_right_boundary)

def _install(metadata,interactive,timestamp_right_boundary=None):
    import sddaemon


    # Compute total files stat
    count_total=metadata.count()
    size_total=metadata.size

    sdlog.info("SYNDINST-001","'keep new status' process begins")

    # Compute new files stat
    #
    # (yes, block below is a duplicate of what is done inside sdenqueue.run()
    # method, but safer to keep it there too, and should be no harm in term of
    # perfomance)
    #
    import sdsimplefilter, sdconst
    metadata=sdsimplefilter.run(metadata,'status',sdconst.TRANSFER_STATUS_NEW,'keep')
    count_new=metadata.count()
    size_new=metadata.size

    sdlog.info("SYNDINST-024","'keep new status' process ends")

    # what to do if no match
    if count_new<1:

        if count_total>0:
            sdlog.info("SYNDINST-027","Nothing to install (matching files are already installed or waiting in the download queue). To monitor transfers status and progress, use 'synda queue' command.",stderr=interactive)
        else:
            sdlog.info("SYNDINST-028",'Nothing to install (0 file found).',stderr=interactive)

        return (0,0)

    # ask user for confirmation
    if interactive:
        import humanize
        print_stderr('%i file(s) will be added to the download queue.'%count_new)
        print_stderr('Once downloaded, %s of additional disk space will be used.'%humanize.naturalsize(size_new,gnu=False))

        import sdutils
        if sdutils.query_yes_no('Do you want to continue?', default="yes"):
            installation_confirmed=True
        else:
            installation_confirmed=False
    else:
        installation_confirmed=True

    sdlog.info("SYNDINST-002","Store metadata in database..")

    # install
    if installation_confirmed:
        import sdenqueue
        sdenqueue.run(metadata,timestamp_right_boundary)

        if interactive:
            print_stderr("%i file(s) enqueued"%count_new)
            print_stderr("You can follow the download using 'synda watch' and 'synda queue' commands")

            if not sddaemon.is_running():
                msg=sdi18n.m0025 if sdconfig.system_pkg_install else sdi18n.m0026
                print_stderr("The daemon is not running. To start it, use '%s'."%msg)
    else:
        if interactive:
            print_stderr('Abort.')

    sdlog.info("SYNDINST-025","Task complete")

    return (0,count_new)

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
