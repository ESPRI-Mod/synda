#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""Contains cleanup routines."""

import os
import argparse
from synda.sdt import sdlog
from synda.sdt import sdtools
from synda.sdt import sdutils
from synda.sdt.sdexception import SDException

from synda.source.config.file.log.models import Config as Log

from synda.source.config.file.scripts.models import Config as Scripts
from synda.source.config.path.tree.models import Config as TreePath


def ignore(f):
    if f.endswith('.nc'):
        return False
    else:
        return True


def remove_empty_files(path):
    for p in sdtools.walk_backward_without_sibling(path):
        for name in os.listdir(p):
            f = '%s/%s' % (p, name)
            # this is not to remove files at top of the tree,
            # not related with synda (e.g. every hidden file in HOME dir)
            if not ignore(f):
                if os.path.isfile(f):
                    if not os.path.islink(f):
                        if os.path.getsize(f) == 0:
                            try:
                                sdlog.info("SYNCLEAN-090", "Remove empty file (%s)" % (f,))
                                os.remove(f)
                            except Exception as e:
                                sdlog.warning(
                                    "SYNCLEAN-040",
                                    "Error occurs during file deletion ({},{})".format(
                                        f,
                                        e,
                                    ),
                                )


def full_cleanup():
    """Remove empty files and folders."""

    data_folder = TreePath().get("data")

    cleanup_tree_script = Scripts().get("sdcleanup_tree")

    sdlog.info("SYNCLEAN-008", "Starting cleanup in %s." % data_folder)

    argv = [cleanup_tree_script, data_folder]

    status, stdout, stderr = sdutils.get_status_output(argv)
    if status != 0:
        sdtools.trace(
            Log().get("stack_trace"),
            os.path.basename(
                cleanup_tree_script,
            ),
            status,
            stdout,
            stderr,
        )

        raise SDException("SYNCLEAN-001", "Error occurs during tree cleanup")

    sdlog.info("SYNCLEAN-010", "Cleanup done.")


def part_cleanup(paths):
    """Remove empty files and folders."""

    sdlog.info("SYNCLEAN-018", "Cleanup begin")

    # maybe overkill (idea is that reverse order may allow the suppression of empty sibling,
    # but as all paths to be removed will go through a os.removedirs call it should work anyway)
    paths = sorted(paths, reverse=True)

    for p in paths:
        sdlog.info("SYNCLEAN-060", "Check for empty file and directory in %s" % p)

        # remove empty files
        sdlog.debug("SYNCLEAN-120", "Remove empty files (%s)" % (p,))
        remove_empty_files(p)

        # remove empty directories starting from leaves
        sdlog.debug("SYNCLEAN-140", "Remove empty dirs (%s)" % (p,))
        try:
            os.removedirs(p)
        except OSError as e:
            # Neutralize exception (needed as removedirs raise exception at first non empty dir).
            pass

    # as the previous command may also remove 'data' folder (when all data have been removed),
    # we re-create 'data' if missing

    data_folder = TreePath().get("data")

    if not os.path.isdir(data_folder):
        os.makedirs(data_folder)

    sdlog.info("SYNCLEAN-020", "Cleanup done.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    full_cleanup()
