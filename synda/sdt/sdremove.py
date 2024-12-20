#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains 'synda remove' related routines."""

import os
import argparse
from synda.sdt.sdtools import print_stderr, print_stdout
from synda.sdt import sdexception
from synda.sdt import sdmdcommon
from synda.sdt import sddelete
from synda.sdt import sddeletefile
from synda.sdt import sddeletedataset
from synda.sdt import sdcleanup
from synda.sdt import sdtypes
from synda.sdt import syndautils
from synda.sdt import sdearlystreamutils
from synda.sdt import sdlog

from synda.source.config.process.download.constants import TRANSFER


def run(args, stream):
    if is_local(stream):
        run_local(args, stream)
    else:
        run_remote(args, stream)


def is_local(stream):
    if (sdearlystreamutils.exists_facet_value_early(stream, 'status')
            or sdearlystreamutils.exists_facet_value_early(stream, 'insertion_group_id')
            or sdearlystreamutils.exists_facet_value_early(stream, 'sdget_status')):
        return True
    else:
        return False


def run_local(args, stream):
    from synda.sdt import sdlfile

    syndautils.check_daemon()

    try:
        files = sdlfile.get_files(
            stream=stream,
            dry_run=args.dry_run,
        )

        if len(files) == 0:
            raise sdexception.EmptySelectionException()

        if args.verbose:
            for f in files:
                buf = "file_id=%d, status=%s, local_path=%s, url=%s" % \
                      (f.file_id, f.status, f.get_full_local_path(), f.url)
                print_stdout(buf)

        # transform object to dict (needed as remove_helper() expect list of dict, not list of File)
        files = [f.__dict__ for f in files]

        metadata = sdtypes.Metadata(files=files)
    except sdexception.EmptySelectionException:
        print_stderr('No packages will be installed, upgraded, or removed.')
        return 0

    if not args.dry_run:
        remove_helper(args, metadata)


def run_remote(args, stream):

    syndautils.check_daemon()

    try:
        metadata = syndautils.file_full_search(args, stream)
    except sdexception.EmptySelectionException:
        print_stderr('No packages will be installed, upgraded, or removed.')
        return 0

    if not args.dry_run:
        remove_helper(args, metadata)


def remove_helper(args, metadata):
    import humanize
    from synda.sdt import sdsimplefilter
    from synda.sdt import sdutils

    sdlog.info("SDREMOVE-001", "Remove operation running..")

    # filtering

    metadata = sdsimplefilter.run(
        metadata,
        'status',
        TRANSFER["status"]['new'],
        'remove',
    )
    # maybe not needed as we now do immediate delete
    metadata = sdsimplefilter.run(
        metadata,
        'status',
        TRANSFER["status"]['delete'],
        'remove',
    )

    count_delete = metadata.count()

    metadata_done = sdsimplefilter.run(metadata.copy(), 'status', TRANSFER["status"]['done'], 'keep')
    size_delete = metadata_done.size

    if count_delete > 0:

        print_stderr('%i file(s) will be removed.' % count_delete)
        print_stderr(
            'After this operation, %s of disk space will be freed.' % humanize.naturalsize(size_delete, gnu=False),
        )

        # ask user for confirmation
        interactive = not args.yes
        if interactive:
            if sdutils.query_yes_no('Do you want to continue?', default="no"):
                suppression_confirmed = True
            else:
                print_stderr('Abort.')
                return 1
        else:
            suppression_confirmed = True

        # perform deletion
        if suppression_confirmed:
            remove(metadata, (not args.keep_data))
            return 0

    else:
        print_stderr('Nothing to delete.')
        return 0


def remove(metadata, remove_all=True):

    # First step, change the files status from 'done' to 'delete' (METADATA).
    #
    # Note
    #     This is a deferred delete.
    #
    nbr = sddelete.run(metadata)
    print_stderr("%i file(s) removed" % nbr)

    # Second step, do the deletion (DATA and METADATA) (to do a deferred
    # deletion (i.e. by the daemon), comment line below and enable
    # corresponding line in sdtask. Note that a code review is needed if both
    # are enabled simultaneously (e.g. see TAGKRE45343J54K5JK))
    #
    sddeletefile.delete_transfers_lowmem(remove_all)

    if remove_all:
        print_stderr("Remove empty folders and files.. (may take some time)")

    # Third step is to remove orphan dataset (METADATA)
    sddeletedataset.purge_orphan_datasets()

    # Fourth step is to remove orphan folder (DATA)
    if remove_all:

        # part
        # retrieve paths
        paths = sdmdcommon.get_attributes(metadata, 'local_path')
        # remove filenames
        paths = [os.path.dirname(p) for p in paths]
        # switch to full path
        paths = [sdtypes.build_full_local_path(p) for p in paths]
        # follow symlink
        paths = [os.path.realpath(p) for p in paths]
        # remove paths
        sdcleanup.part_cleanup(paths)
        # full
        # sdcleanup.full_cleanup()

# init.


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
