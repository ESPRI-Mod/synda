#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################
#  @program        synda
#  @description    climate models data transfer program
#  @copyright      Copyright “(c)2009 Centre National de la Recherche Scientifique CNRS. 
#                             All Rights Reserved”
#  @license        CeCILL (https://raw.githubusercontent.com/Prodiguer/synda/master/sdt/doc/LICENSE)
##################################

"""This module contains startup helper.

Notes
    - In this file, module import directives are moved near the calls, so to improve startup time.
"""

import sys
import os

from synda.source.config.file.user.preferences.models import Config as Preferences
from synda.source.config.api.esgf_search.constants import STRUCTURE as SEARCH_API_STRUCTURE
from synda.source.config.process.history.constants import STRUCTURE as HISTORY_STRUCTURE


def check_daemon():
    from synda.sdt import sdconfig
    if sdconfig.prevent_daemon_and_modification:
        from synda.sdt import sddaemon
        if sddaemon.is_running():
            print('The daemon must be stopped before installing/removing dataset')
            sys.exit(3)


def get_stream(
        subcommand=None,
        parameter=None,
        selection_file=None,
        no_default=True,
        raise_exception_if_empty=False,
):

    """
    TODO: merge me with sdstreamutils.get_stream
    """
    from synda.sdt import sdbuffer
    from synda.sdt import sdparse
    from synda.sdt import sdstream
    from synda.sdt import sdexception

    preferences = Preferences()

    if parameter is None:
        parameter = []

    buffer_ = sdbuffer.get_selection_file_buffer(
        parameter=parameter,
        path=selection_file,
    )

    if len(buffer_.lines) == 0:
        # we come here when user selected nothing (neither from stdin neither from selection file neither from arg)

        if raise_exception_if_empty:
            raise sdexception.EmptySelectionException()

    selection = sdparse.build(
        buffer_,
        load_default=(not no_default),
    )

    stream = selection.to_stream()

    # Set default value for nearest here
    #
    # TODO: make it work with all actions (e.g. search) as it only working for 'install' action for now
    #

    if preferences.is_behaviour_nearest:
        # sddeferredbefore.add_default_parameter(stream,'nearest',True) # TODO: why this one is not working ?
        sdstream.set_scalar(stream, 'nearest', True)

    # progress

    if preferences.is_interface_progress:
        sdstream.set_scalar(stream, 'progress', True)

    # from the synda engine perspective, 'action' is more meaningful than 'subcommand'
    sdstream.set_scalar(stream, 'action', subcommand)

    # aka facets_groups
    return stream


def file_full_search(args, stream=None):
    """This func systematically triggers full search (i.e. limit keyword cannot be used here).

    This func is currently being used in the following modules:
        - sdinstall
        - sdremove
        - sdstat
    """
    from synda.sdt import sdsearch
    from synda.sdt import sdlog
    from synda.sdt import sdhistory
    from synda.sdt import sdstream
    from synda.sdt import sdtime
    from synda.sdt import sdselectionfileutils
    from synda.sdt import sdexception

    if stream is None:
        stream = get_stream(
            subcommand=args.subcommand,
            parameter=args.parameter,
            selection_file=args.selection_file,
            no_default=args.no_default,
            raise_exception_if_empty=True,
        )

    # type is always SA_TYPE_FILE when we are here
    force_type(stream, SEARCH_API_STRUCTURE['type']['file'])

    # incremental mode management

    # prevent incremental mode for 'remove' subcommand
    if args.subcommand in ('install', 'stat'):

        if args.timestamp_left_boundary and args.incremental:
            raise sdexception.SDException(
                'SYNUTILS-003',
                "Incorrect argument: 'timestamp_left_boundary' and 'incremental' are mutually exclusive options",
            )

        # those filters are mainly used to test 'incremental mode' feature
        if args.timestamp_left_boundary is not None:
            sdstream.set_scalar(stream, 'from', args.timestamp_left_boundary)
        if args.timestamp_right_boundary is not None:
            sdstream.set_scalar(stream, 'to', args.timestamp_right_boundary)

        if args.incremental:

            sdlog.info('SYNUTILS-002', 'Starting file discovery (incremental mode enabled)')

            selection_file = sdselectionfileutils.find_selection_file(args.selection_file)

            selection_filename = os.path.basename(selection_file)

            if sdhistory.previous_run_exists(selection_filename, 'add'):
                sdlog.info('SYNUTILS-004', 'Previous run exists')

                if not sdhistory.file_changed_since_last_run(selection_file, HISTORY_STRUCTURE['action']['add']):
                    sdlog.info('SYNUTILS-006', "Selection file hasn't changed since last run")

                    previous_run = sdhistory.get_previous_run(selection_filename, 'add')
                    dt = previous_run['crea_date']

                    # to prevent UTC vs localtime time issue
                    # (history.crea_date is in localtime while search-api timestamp is in UTC time)
                    # we systematically substract 72 hours to the left boundary
                    #
                    dt = sdtime.substract_hour(dt, 72)

                    # convert datetime format
                    search_api_datetime = sdtime.sqlite_datetime_format_to_search_api_datetime_format(dt)

                    # add incremental mode filters
                    #
                    # sample
                    #     from='2015-10-19T22:00:00Z'
                    #
                    # note
                    #     'from' and 'to' filters refer to 'timestamp' attribute
                    #
                    # more info
                    #     https://github.com/ESGF/esgf.github.io/wiki/ESGF_Search_REST_API
                    #
                    sdstream.set_scalar(stream, 'from', search_api_datetime)

                else:
                    sdlog.info('SYNUTILS-007', "Selection file has changed since last run")

            else:
                sdlog.info('SYNUTILS-008', 'No previous run found')

    metadata = sdsearch.run(stream=stream, dry_run=args.dry_run)

    return metadata


def force_type(stream, type_):
    from synda.sdt import sddeferredbefore

    # we 'force' (i.e. we do not just set as 'default') the parameter here, so
    # to prevent user to set it
    sddeferredbefore.add_forced_parameter(stream, 'type', type_)


def strip_dataset_version(dataset_functional_id):
    import re
    return re.sub(r'\.[^.]+$', '', dataset_functional_id)
