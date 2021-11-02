# -*- coding: utf-8 -*-
##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright "(c)2009 Centre National de la Recherche Scientifique CNRS.
#                             All Rights Reserved"
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################
import humanize
from pprint import pprint

from synda.sdt import sdlog
from synda.sdt import sdexception
from synda.sdt.sdtools import print_stderr, print_stdout
from synda.sdt import syndautils
from synda.sdt import sdsimplefilter

from synda.source.config.process.download.constants import TRANSFER

from synda.source.process.subcommand.required.env.models import Process as Base
from synda.source.process.authority.models import Authority


def get_metadata(args):
    metadata = None
    # retrieve metadata

    # if not args.selection_file:
    #     print_stderr(
    #         "ERROR: 'selection_file' option is not set (a selection file must be used when "
    #         "'incremental' option is set)",
    #     )
    #
    #     return metadata

    if args.selection_file is not None:
        sdlog.info("SYNDINST-006", "Process '{}'".format(args.selection_file))

    try:
        metadata = syndautils.file_full_search(args)
    except sdexception.EmptySelectionException as e:
        print_stderr('No dataset will be installed, upgraded, or removed.')
    except sdexception.SDException as e:
        sdlog.info("SYNDINST-006", "Exception occured during installation ('{}')".format(e))

    return metadata


def _print(info):
    print_stdout(info)


def getinfo_filesize(metadata):
    # Compute total files stat
    count_total = metadata.count()
    metadata = sdsimplefilter.run(metadata, 'status', TRANSFER["status"]['new'], 'keep')
    metadata = sdsimplefilter.run(metadata, 'url', "//None", 'remove_substr')
    count_new = metadata.count()
    size_new = metadata.size
    formatted_value = humanize.naturalsize(
        size_new,
        gnu=False,
    )
    return f'FileSize = {formatted_value} [{count_new} file(s)]'


class Process(Base):

    def __init__(self):
        super(Process, self).__init__(name="getinfo", authority=Authority())

    def run(self, args):
        args.dry_run = False
        args.no_default = True
        args.selection_file = None
        metadata = get_metadata(args)
        if metadata:
            info = None
            if args.filesize:
                info = getinfo_filesize(metadata)
            else:
                print_stderr(
                    f'error occured, unknown argument for getinfo subcommand',
                )
            if info:
                _print(info)
        else:
            print_stderr(
                f'error occured, unknown argument for getinfo subcommand',
            )
