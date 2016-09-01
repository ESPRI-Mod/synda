#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains 'synda remove' related routines."""

import sys
import argparse
from sdtools import print_stderr
import sdexception
import sddelete
import sddeletefile
import sddeletedataset
import sdoperation
import sdtypes
import syndautils
import sdearlystreamutils

def run(args,stream):
    if is_local(stream):
        run_local(args,stream)
    else:
        run_remote(args,stream)

def is_local(stream):
    li=sdearlystreamutils.get_facet_values_early(stream,'status')
    if len(li)!=0:
        return True
    else:
        return False

def run_local(args,stream):
    import sdlfile

    syndautils.check_daemon()

    try:
        files=sdlfile.get_files(stream=stream,dry_run=args.dry_run)

        if len(files)==0:
            raise sdexception.EmptySelectionException()

        # transform object to dict (needed as remove_helper() expect list of dict, not list of File)
        files=[f.__dict__ for f in files]

        metadata=sdtypes.Metadata(files=files)
    except sdexception.EmptySelectionException, e:
        print_stderr('No packages will be installed, upgraded, or removed.')
        return 0

    if not args.dry_run:
        remove_helper(args,metadata)

def run_remote(args,stream):

    syndautils.check_daemon()

    try:
        metadata=syndautils.file_full_search(args,stream)
    except sdexception.EmptySelectionException, e:
        print_stderr('No packages will be installed, upgraded, or removed.')
        return 0

    if not args.dry_run:
        remove_helper(args,metadata)

def remove_helper(args,metadata):
    import humanize, sdsimplefilter, sdconst, sdutils

    # filtering

    metadata=sdsimplefilter.run(metadata,'status',sdconst.TRANSFER_STATUS_NEW,'remove')
    metadata=sdsimplefilter.run(metadata,'status',sdconst.TRANSFER_STATUS_DELETE,'remove') # maybe not needed as we now do immediate delete

    count_delete=metadata.count()

    metadata_done=sdsimplefilter.run(metadata.copy(),'status',sdconst.TRANSFER_STATUS_DONE,'keep')
    size_delete=metadata_done.size

    if count_delete>0:

        print_stderr('%i file(s) will be removed.'%count_delete)
        print_stderr('After this operation, %s of disk space will be freed.'%humanize.naturalsize(size_delete,gnu=False))

        # ask user for confirmation
        interactive=not args.yes
        if interactive:
            if sdutils.query_yes_no('Do you want to continue?', default="no"):
                suppression_confirmed=True
            else:
                print_stderr('Abort.')
                return 1
        else:
            suppression_confirmed=True

        # perform deletion
        if suppression_confirmed:
            remove(metadata)
            return 0

    else:
        print_stderr('Nothing to delete.')
        return 0

def remove(metadata):

    # First step, change the files status from 'done' to 'delete' (update metadata).
    #
    # Note
    #     This is a deferred delete.
    #
    nbr=sddelete.run(metadata)
    print_stderr("%i file(s) removed"%nbr)

    # Second step, do the deletion (remove files on filesystem and remove files metadata)
    # (to do a deferred deletion (i.e. by the daemon), comment line below)
    #
    # Note
    #    Use loop for lowmem machine compatibility
    #
    count=sddeletefile.delete_transfers(100)
    while count > 0:
        count=sddeletefile.delete_transfers(100)

    # Third step is to remove orphan dataset in local database
    sddeletedataset.purge_orphan_datasets()

    # Fourth step is to remove orphan folder.
    sdoperation.cleanup_tree()

# init.

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
