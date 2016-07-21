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
from sdtools import print_stderr
import sdexception

def run(args,metadata=None):
    import syndautils

    syndautils.check_daemon()

    if metadata is None:

        # retrieve metadata

        if args.incremental and not args.selection_file:
            print_stderr("ERROR: 'selection_file' option is not set (a selection file must be used when 'incremental' option is set)")
            return (1,0)

        try:
            metadata=syndautils.file_full_search(args)
        except sdexception.EmptySelectionException, e:
            print_stderr('No packages will be installed, upgraded, or removed.')
            return (0,0)

    # in dry-run mode, we stop here
    if args.dry_run:
        return (0,0)

    interactive=not args.yes

    return install(metadata.files,interactive)

def install(files,interactive):
    import sddaemon


    # Compute total files stat
    count_total=len(files)
    size_total=sum(int(f['size']) for f in files)


    # Compute new files stat
    #
    # (yes, block below is a duplicate of what is done inside sdenqueue.run()
    # method, but safer to keep it there too, and should be no harm in term of
    # perfomance)
    #
    import sdsimplefilter, sdconst
    files=sdsimplefilter.run(files,'status',sdconst.TRANSFER_STATUS_NEW,'keep')
    count_new=len(files)
    size_new=sum(int(f['size']) for f in files)


    # what to do if no match
    if count_new<1:

        if interactive:
            if count_total>0:
                print_stderr("Nothing to install (matching files are already installed or waiting in the download queue). To monitor transfers status and progress, use 'synda queue' command.")
            else:
                print_stderr('Nothing to install (0 file found).')

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


    # install
    if installation_confirmed:
        import sdenqueue
        sdenqueue.run(files)

        if interactive:
            print_stderr("%i file(s) enqueued"%count_new)
            print_stderr("You can follow the download using 'synda watch' and 'synda queue' commands")

            if not sddaemon.is_running():
                print_stderr("The daemon is not running. To start it, use 'sudo service synda start'.")
    else:
        if interactive:
            print_stderr('Abort.')

    return (0,count_new)

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
